# Copyright 2017-2019 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import logging
import os
import re
import subprocess
import sys
import time

import guild.plugin
import guild.run

from guild import config as configlib
from guild import deps
from guild import exit_code
from guild import flag_util
from guild import op_util
from guild import summary
from guild import util
from guild import var

log = logging.getLogger("guild")

OP_RUNFILE_PATHS = [
    ["org_click"],
    ["org_psutil"],
    ["guild", "external"],
]
PROC_TERM_TIMEOUT_SECONDS = 30

DEFAULT_EXEC = "${python_exe} -um guild.op_main ${main_args} -- ${flag_args}"
STEPS_EXEC = "${python_exe} -um guild.steps_main"

DEFAULT_OUTPUT_SCALARS = [
    r"^(\key):\s+(\value)$",
]

class InvalidOpSpec(ValueError):
    pass

class OpInitError(Exception):
    pass

class ProcessError(Exception):
    pass

class Operation(object):

    batch_op = None

    def __init__(self, opdef, run_dir=None, label=None,
                 extra_attrs=None, restart=False,
                 stage_only=False, gpus=None):
        assert opdef.opref, (opdef, "needs call to set_modelref")
        self.opref = opdef.opref
        self._validate_opdef(opdef)
        self.opdef = opdef
        (self.cmd_args,
         self.flag_vals,
         self._flag_map) = _init_cmd_args(opdef)
        self.cmd_env = _init_cmd_env(opdef, gpus)
        self._run_dir = run_dir
        self.label = label
        self.extra_attrs = extra_attrs
        self.restart = restart
        self.stage_only = stage_only
        self.gpus = gpus
        self._started = None
        self._stopped = None
        self._run = None
        self._proc = None
        self._exit_status = None

    @staticmethod
    def _validate_opdef(opdef):
        if not (opdef.main or opdef.exec_ or opdef.steps):
            raise InvalidOpSpec("requires one of: main, exec, steps")

    @property
    def run_dir(self):
        return self._run_dir or (self._run.path if self._run else None)

    def set_run_dir(self, path):
        self._run_dir = path

    @property
    def run_id(self):
        return self._run.id if self._run else None

    def write_run_attr(self, name, val, raw=False):
        if self._run is None:
            raise RuntimeError("op is not intialized - call init() first")
        self._run.write_attr(name, val, raw)

    def run(self, quiet=False, background_pidfile=None, stop_after=None):
        self.init()
        return self.run_impl(quiet, background_pidfile, stop_after)

    def init(self):
        self._init_run()
        self._init_attrs()
        self._copy_sourcecode()
        self._init_digests()
        return self._run

    def _init_run(self):
        self._run = init_run(self._run_dir)
        log.debug("initializing run in %s", self._run.path)
        self._run.init_skel()
        self.set_pending()

    def set_pending(self):
        write_pending(self._run)

    def _init_attrs(self):
        assert self._run is not None
        self._run.write_opref(self.opref)
        self._run.write_attr("opdef", self.opdef.as_data())
        for name, val in (self.extra_attrs or {}).items():
            self._run.write_attr(name, val)
        self._run.write_attr("flags", self.flag_vals)
        self._run.write_attr("cmd", self.cmd_args)
        if self.label is not None:
            self._run.write_attr("label", self.label)
        if self.opdef.compare is not None:
            self._run.write_attr("compare", self.opdef.compare)
        if self.opdef.steps:
            self._run.write_attr("steps", self.opdef.steps)
        if self.opdef.objective:
            self._run.write_attr("objective", self.opdef.objective)
        if self._flag_map:
            self._run.write_attr("_flag_map", self._flag_map)
        for key, val in self.opdef.modeldef.extra.items():
            self._run.write_attr("_extra_%s" % key, val)

    def _copy_sourcecode(self):
        assert self._run is not None
        if not self.restart and self._opref_has_sourcecode():
            op_util.copy_run_sourcecode(self._run, self.opdef)

    def _opref_has_sourcecode(self):
        return self.opref.pkg_type in ("guildfile", "script", "package")

    def _init_digests(self):
        assert self._run is not None
        op_util.write_sourcecode_digest(self._run, self.opdef)

    def run_impl(self, quiet=False, background_pidfile=None, stop_after=None):
        self._started = guild.run.timestamp()
        self._run.write_attr("started", self._started)
        try:
            self.resolve_deps()
            return self.proc(quiet, background_pidfile, stop_after)
        finally:
            self._cleanup()

    def resolve_deps(self):
        assert self._run is not None
        ctx = deps.ResolutionContext(
            target_dir=self._run.path,
            opdef=self.opdef,
            resource_config=self.flag_vals)
        resolved = deps.resolve(self.opdef.dependencies, ctx)
        self._run.write_attr("deps", _sort_resolved(resolved))
        self._maybe_refresh_label(resolved)

    def _maybe_refresh_label(self, resolved):
        """Refresh label with details in resolved.

        The initial label is written as an attr and updated here as
        needed to reflected resolved resource sources.
        """
        assert self._run is not None
        label = self._run.get("label")
        if label is not None:
            formatted = op_util.format_label(label, self.flag_vals, resolved)
            self._run.write_attr("label", formatted)

    def proc(self, quiet=False, background_pidfile=None, stop_after=None):
        if self.stage_only:
            self._stage_proc()
            return 0
        if background_pidfile:
            self._background_proc(background_pidfile, quiet, stop_after)
            return 0
        return self._foreground_proc(quiet, stop_after)

    def _background_proc(self, pidfile, quiet, stop_after):
        assert self._run
        import daemonize
        action = lambda: self._foreground_proc(quiet, stop_after)
        daemon = daemonize.Daemonize(app="guild_op", action=action, pid=pidfile)
        if not quiet:
            log.info(
                "%s started in background as %s (pidfile %s)",
                self.opdef.opref.to_opspec(), self._run.id, pidfile)
        daemon.start()

    def _foreground_proc(self, quiet, stop_after):
        self._start_proc()
        self._wait_for_proc(quiet, stop_after)
        self._finalize_attrs()
        return self._exit_status

    def _stage_proc(self):
        assert self._run is not None
        env = self._proc_env()
        log.debug("operation command: %s", self.cmd_args)
        log.debug("operation env: %s", env)
        _write_sourceable_env(env, self._run.guild_path("ENV"))
        _write_staged(self._run)

    def _start_proc(self):
        assert self._proc is None
        assert self._run is not None
        args = self.cmd_args
        env = self._proc_env()
        self._run.write_attr("env", env)
        cwd = self._run.path
        log.debug("starting operation run %s", self._run.id)
        log.debug("operation command: %s", args)
        log.debug("operation env: %s", env)
        log.debug("operation cwd: %s", cwd)
        _delete_staged(self._run)
        delete_pending(self._run)
        try:
            proc = subprocess.Popen(
                args,
                env=env,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        except OSError as e:
            raise ProcessError(e)
        else:
            self._proc = proc
            _write_proc_lock(self._proc, self._run)

    def _proc_env(self):
        assert self._run is not None
        env = dict(self.cmd_env)
        env["RUN_DIR"] = self._run.path
        env["RUN_ID"] = self._run.id
        util.check_env(env)
        return env

    def _wait_for_proc(self, quiet, stop_after):
        assert self._proc is not None
        try:
            proc_exit_status = self._watch_proc(quiet, stop_after)
        except KeyboardInterrupt:
            proc_exit_status = self._handle_proc_interrupt()
        self._exit_status = _op_exit_status(proc_exit_status, self.opdef)
        self._stopped = guild.run.timestamp()
        _delete_proc_lock(self._run)

    def _watch_proc(self, quiet, stop_after):
        assert self._proc is not None
        output = op_util.RunOutput(
            self._run, self._proc, quiet,
            self._output_scalars_summary())
        if stop_after is None:
            exit_status = self._proc.wait()
        else:
            exit_status = op_util.wait_for_proc(self._proc, stop_after)
        output.wait_and_close()
        return exit_status

    def _output_scalars_summary(self):
        try:
            summary.check_enabled()
        except summary.Disabled as e:
            log.warning(e)
            return None
        else:
            config, ignore = self._output_scalars_config()
            summary_path = self._run.guild_path()
            return summary.OutputScalars(config, summary_path, ignore)

    def _output_scalars_config(self):
        config = self.opdef.output_scalars
        if config is None:
            return DEFAULT_OUTPUT_SCALARS, self.flag_vals.keys()
        return config, None

    def _handle_proc_interrupt(self):
        if not self.batch_op:
            log.info("Operation interrupted - waiting for process to exit")
        kill_after = time.time() + PROC_TERM_TIMEOUT_SECONDS
        while time.time() < kill_after:
            if self._proc.poll() is not None:
                break
            time.sleep(1)
        if self._proc.poll() is None:
            log.warning("Operation process did not exit - stopping forcefully")
            util.kill_process_tree(self._proc.pid, force=True)
        return exit_code.SIGTERM

    def _finalize_attrs(self):
        assert self._run is not None
        assert self._exit_status is not None
        assert self._stopped is not None
        if not os.path.exists(self._run.path):
            log.warning(
                "run directory has been deleted, unable to finalize")
            return
        if not os.path.exists(self._run._guild_dir):
            log.warning(
                "run Guild directory has been deleted, unable to finalize")
            return
        self._run.write_attr("exit_status", self._exit_status)
        self._run.write_attr("stopped", self._stopped)

    def _cleanup(self):
        assert self._run is not None
        delete_pending(self._run)

def _init_cmd_args(opdef):
    flag_vals = util.resolve_all_refs(opdef.flag_values())
    main_args = _main_args(opdef, flag_vals)
    flag_args, flag_map = _flag_args(flag_vals, opdef, main_args)
    exec_args = _exec_args(opdef, flag_vals, main_args, flag_args)
    return exec_args, flag_vals, flag_map

def _main_args(opdef, flag_vals):
    try:
        return _split_and_resolve_args(opdef.main or "", flag_vals)
    except util.UndefinedReferenceError as e:
        raise InvalidOpSpec(
            "main contains invalid reference '%s'"
            % e.args[0])

def _split_and_resolve_args(cmd, flag_vals):
    """Splits and resolve args for string or list cmd."""
    format_part = lambda part: str(util.resolve_refs(part, flag_vals))
    return [format_part(part) for part in op_util.split_cmd(cmd)]

def _exec_args(opdef, flag_vals, main_args, flag_args):
    template = _exec_template(opdef)
    flag_vals = _extended_flag_vals(flag_vals, opdef)
    try:
        args = _split_and_resolve_args(template, flag_vals)
    except util.UndefinedReferenceError as e:
        raise InvalidOpSpec(
            "exec contains invalid reference '%s'"
            % e.args[0])
    else:
        args = _repl_args(args, "__main_args__", main_args)
        args = _repl_args(args, "__flag_args__", flag_args)
        return args

def _exec_template(opdef):
    """Returns exec template for opdef.

    If exec is specified explicitly, it's returned, otherwise main or
    steps are used to generate a template.
    """
    if opdef.exec_:
        if opdef.main:
            log.warning(
                "operation 'exec' and 'main' both specified, "
                "ignoring 'main'")
        if opdef.steps:
            log.warning(
                "operation 'exec' and 'steps' both specified, "
                "ignoring 'steps'")
        return opdef.exec_
    elif opdef.main:
        if opdef.steps:
            log.warning(
                "operation 'main' and 'steps' both specified, "
                "ignoring 'steps'")
        return DEFAULT_EXEC
    elif opdef.steps:
        return STEPS_EXEC
    assert False, opdef

def _extended_flag_vals(flag_vals, opdef):
    """Extend flag_vals with special flag vals for op exec resolution.

    The following flag vals are included in the extended flag vals:

      'python_exe': full path to Python exe per opdef

      'main_args':  special marker object designating the location of
                    args specified in opdef main

      'flag_args':  special marker object designating the location of
                    flag args

      'model_dir':  directory containing the operation guild file

    If any of the extended values are defined in flag_vals, they are
    replaced here.
    """
    extended = dict(flag_vals)
    extended.update({
        "python_exe": _python_exe(opdef),
        "main_args": "__main_args__",
        "flag_args": "__flag_args__",
        "model_dir": opdef.guildfile.dir,
    })
    return extended

def _python_exe(opdef):
    req = opdef.python_requires or opdef.modeldef.python_requires
    if req:
        matching = util.find_python_interpreter(req)
        if not matching:
            raise OpInitError(
                "cannot find a python interpreter for "
                "version requirement %r" % req)
        path, _ver = matching
        return path
    return sys.executable

def _repl_args(args, key, replacement):
    """Replaces occurrences of key in args with replacement."""
    ret = []
    for arg in args:
        if arg == key:
            ret.extend(replacement)
        else:
            ret.append(arg)
    return ret

def _flag_args(flag_vals, opdef, cmd_args):
    flag_args = []
    flag_vals, flag_map = op_util.mapped_flag_vals(flag_vals, opdef)
    cmd_options = _cmd_options(cmd_args)
    for name, val in sorted(flag_vals.items()):
        if name in cmd_options:
            log.warning(
                "ignoring flag '%s = %s' because it's shadowed "
                "in the operation cmd", name, val)
            continue
        flag_args.extend(_cmd_option_args(name, val))
    return flag_args, flag_map

def _cmd_options(args):
    p = re.compile("--([^=]+)")
    return [m.group(1) for m in [p.match(arg) for arg in args] if m]

def _cmd_option_args(name, val):
    if val is None:
        return []
    opt = "--%s" % name
    if val is op_util.NO_ARG_VALUE:
        return [opt]
    else:
        return [opt, flag_util.encode_flag_val(val)]

def _init_cmd_env(opdef, gpus):
    env = util.safe_osenv()
    env.update({
        name: str(val)
        for name, val in opdef.env.items()
    })
    env["GUILD_HOME"] = configlib.guild_home()
    env["GUILD_OP"] = opdef.fullname
    env["GUILD_PLUGINS"] = _op_plugins(opdef)
    env["LOG_LEVEL"] = _log_level()
    env["PYTHONPATH"] = _python_path(opdef)
    # SCRIPT_DIR is set by op_main at sys.path[0] - use empty string
    # here to include run dir first in sys.path
    env["SCRIPT_DIR"] = ""
    env["CMD_DIR"] = os.getcwd()
    env["MODEL_DIR"] = env["PROJECT_DIR"] = opdef.guildfile.dir or ""
    env["MODEL_PATH"] = os.path.pathsep.join(_model_paths(opdef))
    if opdef.flags_dest:
        env["FLAGS_DEST"] = opdef.flags_dest
    if opdef.set_trace:
        env["SET_TRACE"] = "1"
    if opdef.handle_keyboard_interrupt:
        env["HANDLE_KEYBOARD_INTERRUPT"] = "1"
    util.apply_env(env, os.environ, ["PROFILE"])
    if gpus is not None:
        log.info(
            "Limiting available GPUs (CUDA_VISIBLE_DEVICES) to: %s",
            gpus or "<none>")
        env["CUDA_VISIBLE_DEVICES"] = gpus
    return env

def _log_level():
    try:
        return os.environ["LOG_LEVEL"]
    except KeyError:
        return str(logging.getLogger().getEffectiveLevel())

def _cmd_arg_env(args):
    flags, _other_args = op_util.args_to_flags(args)
    return {
        name.upper(): str(val)
        for name, val in flags.items()
    }

def _op_plugins(opdef):
    project_plugins = _project_plugins(opdef)
    op_plugins = []
    for name, plugin in guild.plugin.iter_plugins():
        if not _plugin_selected(plugin, project_plugins):
            log.debug("plugin '%s' not configured for operation", name)
            continue
        enabled, reason = plugin.enabled_for_op(opdef)
        if not enabled:
            log.debug(
                "plugin '%s' configured for operation but cannot be enabled%s",
                name, " (%s)" % reason if reason else "")
            continue
        log.debug(
            "plugin '%s' enabled for operation%s",
            name, " (%s)" % reason if reason else "")
        op_plugins.append(name)
    return ",".join(sorted(op_plugins))

def _project_plugins(opdef):
    if opdef.plugins is not None:
        return opdef.plugins or []
    return opdef.modeldef.plugins or []

def _plugin_selected(plugin, selected):
    for name in selected:
        if name == plugin.name or name in plugin.provides:
            return True
    return False

def _python_path(opdef):
    paths = (
        _env_paths() +
        _run_sourcecode_paths() +
        _model_paths(opdef) +
        _guild_paths()
    )
    return os.path.pathsep.join(paths)

def _env_paths():
    env = os.getenv("PYTHONPATH")
    return env.split(os.path.pathsep) if env else []

def _run_sourcecode_paths():
    return [".guild/sourcecode"]

def _model_paths(opdef):
    """Returns the model paths for opdef.

    Guild is moving to an isolation scheme that requires these paths
    NOT be included in a run system path. When they are, it's possible
    that the run sourcecode dir does not contain all of the required
    code and these model paths are relied on to silently provide
    what's missing.

    At the moment, cross package inheritance relies on these
    paths. Until multiple packages can be merged into a single
    sourcecode tree (tricky considering they use multiple roots that
    share a common path to guild.yml) we rely on these paths to
    support that functionality.
    """
    return op_util.opdef_model_paths(opdef)

def _guild_paths():
    guild_path = os.path.dirname(os.path.dirname(__file__))
    abs_guild_path = os.path.abspath(guild_path)
    return [abs_guild_path] + _runfile_paths()

def _runfile_paths():
    return [
        os.path.abspath(path)
        for path in sys.path if _is_runfile_pkg(path)
    ]

def _is_runfile_pkg(path):
    for runfile_path in OP_RUNFILE_PATHS:
        split_path = path.split(os.path.sep)
        if split_path[-len(runfile_path):] == runfile_path:
            return True
    return False

def _write_sourceable_env(env, dest):
    skip_env = ("PWD", "_")
    with open(dest, "w") as out:
        for name in sorted(env):
            if name in skip_env:
                continue
            out.write("export {}='{}'\n".format(name, env[name]))

def _write_proc_lock(proc, run):
    with open(run.guild_path("LOCK"), "w") as f:
        f.write(str(proc.pid))

def _op_exit_status(proc_exit_status, opdef):
    if proc_exit_status == exit_code.SIGTERM and opdef.stoppable:
        return 0
    return proc_exit_status

def _delete_proc_lock(run):
    try:
        os.remove(run.guild_path("LOCK"))
    except OSError:
        pass

def write_pending(run):
    open(run.guild_path("PENDING"), "w").close()

def delete_pending(run):
    util.ensure_deleted(run.guild_path("PENDING"))

def _write_staged(run):
    open(run.guild_path("STAGED"), "w").close()

def _delete_staged(run):
    util.ensure_deleted(run.guild_path("STAGED"))

def init_run(path=None):
    if not path:
        run_id = guild.run.mkid()
        path = os.path.join(var.runs_dir(), run_id)
    else:
        run_id = os.path.basename(path)
    return guild.run.Run(run_id, path)

def _sort_resolved(resolved):
    return {
        name: sorted(files) for name, files in resolved.items()
    }
