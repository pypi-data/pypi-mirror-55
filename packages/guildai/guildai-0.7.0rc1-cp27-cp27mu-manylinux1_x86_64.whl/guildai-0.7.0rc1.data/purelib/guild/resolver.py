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

import hashlib
import importlib
import logging
import os
import re
import subprocess
import tempfile

import six
import yaml

import guild.opref

from guild import util
from guild import var

log = logging.getLogger("guild")

DEFAULT_MATCHING_RUN_STATUS = (
    "completed",
    "running",
    "terminated",
)

class ResolutionError(Exception):
    pass

class Resolver(object):

    def __init__(self, source, resource):
        self.source = source
        self.resource = resource

    def resolve(self, unpack_dir=None):
        raise NotImplementedError()

class FileResolver(Resolver):

    def resolve(self, unpack_dir=None):
        if self.resource.config:
            return _resolve_config_path(
                self.resource.config,
                self.source.resdef.name)
        source_path = self._abs_source_path()
        unpack_dir = self._unpack_dir(source_path, unpack_dir)
        if os.path.isdir(source_path) and not self.source.select:
            resolved = [source_path]
        else:
            resolved = resolve_source_files(
                source_path, self.source, unpack_dir)
        post_process(
            self.source,
            unpack_dir or os.path.dirname(source_path))
        return resolved

    def _abs_source_path(self):
        source_path = self.source.parsed_uri.path
        for root in self._source_location_paths():
            abs_path = os.path.abspath(os.path.join(root, source_path))
            if os.path.exists(abs_path):
                return abs_path
        raise ResolutionError("cannot find source file %s" % source_path)

    def _source_location_paths(self):
        yield self.resource.location
        try:
            modeldef = self.resource.resdef.modeldef
        except AttributeError:
            pass
        else:
            for parent in modeldef.parents:
                yield parent.dir

    @staticmethod
    def _unpack_dir(source_path, explicit_unpack_dir):
        """Returns unpack dir for local archives.

        If explicit_unpack_dir is specified (non blank) it is always
        used. Otherwise a location under the resource cache is used
        based on the value of source_path. In this case, source_path
        must be absolute.

        As with downloaded archives, local archives are unacked into a
        resource cache dir. This avoid unpacking project local files
        within the project.

        """
        if explicit_unpack_dir:
            return explicit_unpack_dir
        assert os.path.isabs(source_path), source_path
        key = "\n".join(["file", source_path]).encode("utf-8")
        digest = hashlib.sha224(key).hexdigest()
        return os.path.join(var.cache_dir("resources"), digest)

def _resolve_config_path(config, resource_name):
    config_path = os.path.abspath(str(config))
    if not os.path.exists(config_path):
        raise ResolutionError("%s does not exist" % config_path)
    log.info(
        "Using %s for %s resource",
        os.path.relpath(config_path),
        resource_name)
    return [config_path]

class URLResolver(Resolver):

    def resolve(self, unpack_dir=None):
        from guild import pip_util # expensive
        if self.resource.config:
            return _resolve_config_path(
                self.resource.config,
                self.source.resdef.name)
        download_dir = url_source_download_dir(self.source)
        util.ensure_dir(download_dir)
        try:
            source_path = pip_util.download_url(
                self.source.uri,
                download_dir,
                self.source.sha256)
        except pip_util.HashMismatch as e:
            raise ResolutionError(
                "bad sha256 for '%s' (expected %s but got %s)"
                % (e.path, e.expected, e.actual))
        else:
            unpack_dir = self._unpack_dir(source_path, unpack_dir)
            resolved = resolve_source_files(
                source_path, self.source, unpack_dir)
            post_process(
                self.source,
                unpack_dir or os.path.dirname(source_path))
            return resolved

    @staticmethod
    def _unpack_dir(source_path, explicit_unpack_dir):
        return explicit_unpack_dir or os.path.dirname(source_path)

def url_source_download_dir(source):
    key = "\n".join(source.parsed_uri).encode("utf-8")
    digest = hashlib.sha224(key).hexdigest()
    return os.path.join(var.cache_dir("resources"), digest)

def post_process(source, cwd, use_cache=True):
    if not source.post_process:
        return
    cmd_in = source.post_process.strip().replace("\n", " ")
    cmd = _apply_source_script_functions(cmd_in, source)
    if use_cache:
        cmd_digest = hashlib.sha1(cmd.encode()).hexdigest()
        process_marker = os.path.join(
            cwd, ".guild-cache-{}.post".format(cmd_digest))
        if os.path.exists(process_marker):
            return
    log.info(
        "Post processing %s resource in %s: %r",
        source.resdef.name, cwd, cmd)
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        raise ResolutionError(
            "error post processing %s resource: %s"
            % (source.resdef.name, e))
    else:
        util.touch(process_marker)

def _apply_source_script_functions(script, source):
    funs = [("project-src", (_project_src_source_script, [source]))]
    for name, fun in funs:
        script = _apply_source_script_function(name, fun, script)
    return script

def _apply_source_script_function(name, fun, script):
    return "".join([
        _apply_source_script_function_to_part(part, name, fun)
        for part in _split_source_script(name, script)])

def _split_source_script(fun_name, script):
    return re.split(r"(\$\(%s .*?\))" % fun_name, script)

def _apply_source_script_function_to_part(part, fun_name, fun):
    m = re.match(r"\$\(%s (.*?)\)" % fun_name, part)
    if m is None:
        return part
    args = util.shlex_split(m.group(1))
    fun, extra_args = fun
    log.debug("Applying %s to %s", fun_name, args)
    return fun(*(args + extra_args))

def _project_src_source_script(path, source):
    roots = [_resdef_dir(source.resdef)] + _resdef_parent_dirs(source.resdef)
    for root in roots:
        full_path = os.path.join(root, path)
        if os.path.exists(full_path):
            log.debug("Found %s under %s", path, root)
            return full_path
    raise ResolutionError(
        "project-src failed: could not find '%s' in path '%s'"
        % (path, os.path.pathsep.join(roots)))

def _resdef_dir(resdef):
    """Return directory for a resource definition.

    The ResourceDef interface doesn't provide a directory, but we can
    infer a directory by checking for 'modeldef' and 'dist'
    attributes, both of which are associated with a Guild file and
    therefore a directory.
    """
    if hasattr(resdef, "modeldef"):
        return resdef.modeldef.guildfile.dir
    elif hasattr(resdef, "dist"):
        return resdef.dist.guildfile.dir
    else:
        raise AssertionError(resdef)

def _resdef_parent_dirs(resdef):
    try:
        modeldef = resdef.modeldef
    except AttributeError:
        return []
    else:
        return [parent.dir for parent in modeldef.parents]

class OperationOutputResolver(FileResolver):

    def __init__(self, source, resource, modeldef):
        super(OperationOutputResolver, self).__init__(source, resource)
        self.modeldef = modeldef

    def resolve(self, unpack_dir=None):
        source_path = self._source_path()
        unpack_dir = self._unpack_dir(source_path, unpack_dir)
        return resolve_source_files(source_path, self.source, unpack_dir)

    def _source_path(self):
        run_spec = str(self.resource.config) if self.resource.config else ""
        if run_spec and os.path.isdir(run_spec):
            log.info(
                "Using output in %s for %s resource",
                run_spec, self.source.resdef.name)
            return run_spec
        run = self.resolve_op_run(run_spec)
        log.info(
            "Using output from run %s for %s resource",
            run.id, self.source.resdef.name)
        return run.path

    def resolve_op_run(self, run_id_prefix=None, include_staged=False):
        oprefs = self._source_oprefs()
        status = _matching_run_status(include_staged)
        run = marked_or_latest_run(oprefs, run_id_prefix, status)
        if not run:
            raise ResolutionError(
                "no suitable run for %s"
                % ",".join([self._opref_desc(opref) for opref in oprefs]))
        return run

    def _source_oprefs(self):
        oprefs = []
        for spec in self._split_opref_specs(self.source.parsed_uri.path):
            try:
                oprefs.append(guild.opref.OpRef.for_string(spec))
            except guild.opref.OpRefError:
                raise ResolutionError("inavlid operation reference %r" % spec)
        return oprefs

    @staticmethod
    def _split_opref_specs(spec):
        return [part.strip() for part in spec.split(",")]

    @staticmethod
    def _opref_desc(opref):
        if opref.pkg_type == "guildfile":
            pkg = "./"
        elif opref.pkg_name:
            pkg = opref.pkg_name + "/"
        else:
            pkg = ""
        model_spec = pkg + (opref.model_name or "")
        return (
            "{}:{}".format(model_spec, opref.op_name)
            if model_spec else opref.op_name)

def _matching_run_status(include_staged):
    if include_staged:
        return DEFAULT_MATCHING_RUN_STATUS + ("staged",)
    return DEFAULT_MATCHING_RUN_STATUS

def marked_or_latest_run(oprefs, run_id_prefix=None, status=None):
    runs = matching_runs(oprefs, run_id_prefix, status)
    log.debug("runs for %s: %s", oprefs, runs)
    if not runs:
        return None
    for run in runs:
        if run.get("marked"):
            return run
    return runs[0]

def matching_runs(oprefs, run_id_prefix=None, status=None):
    status = status or DEFAULT_MATCHING_RUN_STATUS
    oprefs = [_resolve_opref(opref) for opref in oprefs]
    runs_filter = _runs_filter(oprefs, run_id_prefix, status)
    return var.runs(sort=["-started"], filter=runs_filter)

def _resolve_opref(opref):
    if not opref.op_name:
        raise RuntimeError("invalid opref: %s" % opref)
    return guild.opref.OpRef(
        pkg_type=opref.pkg_type or "package" if opref.pkg_name else None,
        pkg_name=opref.pkg_name,
        pkg_version=None,
        model_name=opref.model_name,
        op_name=opref.op_name)

def _runs_filter(oprefs, run_id_prefix, status):
    if run_id_prefix and isinstance(run_id_prefix, six.string_types):
        return lambda run: run.id.startswith(run_id_prefix)
    return var.run_filter(
        "all", [
            var.run_filter("any", [
                var.run_filter("attr", "status", status_val)
                for status_val in status
            ]),
            var.run_filter("any", [
                opref_match_filter(opref) for opref in oprefs
            ])
        ])

class opref_match_filter(object):

    def __init__(self, opref):
        self.opref = opref

    def __call__(self, run):
        return self.opref.is_op_run(run, match_regex=True)

class ModuleResolver(Resolver):

    def resolve(self, unpack_dir=None):
        module_name = self.source.parsed_uri.path
        try:
            importlib.import_module(module_name)
        except ImportError as e:
            raise ResolutionError(str(e))
        else:
            return []

class ConfigResolver(FileResolver):
    """Resolves config sources.

    Config sources are resolved by applying source params and flag
    vals to the config source file. A new config file is generated and
    stored in the run directory under `.guild/generated/RAND/CONFIG`.

    `CONFIG` is assumed to be a YAML file containing a root map
    element.

    Param and flag values are applied using the nesting rules
    implemented in `util.nested_config`. These use dot delimieters to
    designate additional levels in the config map.

    flag values take precedence over param values of the same name.

    Resolves sources are linked to link other resolved resources.
    """

    def resolve(self, unpack_dir=None):
        resolved = super(ConfigResolver, self).resolve(unpack_dir)
        return [self._generate_config(path) for path in resolved]

    def _generate_config(self, path):
        try:
            config = self._load_config(path)
        except Exception as e:
            raise ResolutionError(
                "error loading config from %s: %s"
                % (path, e))
        else:
            self._apply_params(config)
            self._apply_flags(config)
            target_path = self._init_target_path(path)
            self._write_config(config, target_path)
            return target_path

    @staticmethod
    def _load_config(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _apply_params(self, config):
        params = self.source.params
        if params:
            if not isinstance(params, dict):
                log.warning(
                    "unexpected params %r - cannot apply to config",
                    params)
                return
            util.nested_config(params, config)

    def _apply_flags(self, config):
        flags = self._ctx_flags()
        util.nested_config(flags, config)

    def _ctx_flags(self):
        # Steps copied from guild.op
        from guild import op_util
        opdef = self.resource.ctx.opdef
        if not opdef:
            return {}
        flags = util.resolve_all_refs(opdef.flag_values())
        flags, _map = op_util.mapped_flag_vals(flags, opdef)
        return flags

    def _init_target_path(self, path):
        generated = os.path.join(
            self.resource.ctx.target_dir,
            ".guild",
            "generated")
        util.ensure_dir(generated)
        target_dir = tempfile.mkdtemp(suffix="", prefix="", dir=generated)
        basename = os.path.basename(path)
        return os.path.join(target_dir, basename)

    @staticmethod
    def _write_config(config, path):
        with open(path, "w") as f:
            f.write(util.encode_yaml(config))

def resolve_source_files(source_path, source, unpack_dir):
    if not unpack_dir:
        raise ValueError("unpack_dir required")
    _verify_path(source_path, source.sha256)
    return _resolve_source_files(source_path, source, unpack_dir)

def _verify_path(path, sha256):
    if not os.path.exists(path):
        raise ResolutionError("'%s' does not exist" % path)
    if sha256:
        if os.path.isdir(path):
            log.warning("cannot verify '%s' because it's a directory", path)
            return
        _verify_file_hash(path, sha256)

def _verify_file_hash(path, sha256):
    actual = util.file_sha256(path, use_cache=True)
    if actual != sha256:
        raise ResolutionError(
            "'%s' has an unexpected sha256 (expected %s but got %s)"
            % (path, sha256, actual))

def _resolve_source_files(source_path, source, unpack_dir):
    if os.path.isdir(source_path):
        return _dir_source_files(source_path, source)
    else:
        unpacked = _maybe_unpack(source_path, source, unpack_dir)
        if unpacked is not None:
            return unpacked
        else:
            return [source_path]

def _dir_source_files(dir, source):
    if source.select:
        return _selected_source_paths(
            dir, _all_dir_files(dir), source.select)
    else:
        return _all_source_paths(dir, os.listdir(dir))

def _all_dir_files(dir):
    all = []
    for root, dirs, files in os.walk(dir):
        root = os.path.relpath(root, dir) if dir != root else ""
        for name in dirs + files:
            path = os.path.join(root, name)
            normalized_path = path.replace(os.path.sep, "/")
            all.append(normalized_path)
    return all

def _selected_source_paths(root, paths, select):
    selected = set()
    paths = sorted(paths)
    for pattern_str, reduce_f in select:
        matches = _match_paths(paths, pattern_str)
        if reduce_f:
            matches = reduce_f(matches)
        selected.update([os.path.join(root, m.string) for m in matches])
    return sorted(selected)

def _match_paths(paths, pattern_str):
    try:
        p = re.compile(pattern_str + "$")
    except Exception as e:
        log.error("error compiling regular expression %r: %s", pattern_str, e)
        return []
    else:
        return [m for m in [p.match(path) for path in paths] if m]

def _all_source_paths(root, files):
    root_names = [path.split("/")[0] for path in sorted(files)]
    return [
        os.path.join(root, name) for name in set(root_names)
        if not name.startswith(".guild")
    ]

def _maybe_unpack(source_path, source, unpack_dir):
    if not source.unpack:
        return None
    archive_type = _archive_type(source_path, source)
    if not archive_type:
        return None
    return _unpack(source_path, archive_type, source.select, unpack_dir)

def _archive_type(source_path, source):
    if source.type:
        return source.type
    parts = source_path.lower().split(".")
    if parts[-1] == "zip":
        return "zip"
    elif (parts[-1] == "tar" or
          parts[-1] == "tgz" or
          parts[-2:-1] == ["tar"]):
        return "tar"
    elif parts[-1] == "gz":
        return "gzip"
    else:
        return None

def _unpack(source_path, archive_type, select, unpack_dir):
    assert unpack_dir
    unpacked = _list_unpacked(source_path, unpack_dir)
    if unpacked:
        return _for_unpacked(unpack_dir, unpacked, select)
    elif archive_type == "zip":
        return _unzip(source_path, select, unpack_dir)
    elif archive_type == "tar":
        return _untar(source_path, select, unpack_dir)
    elif archive_type == "gzip":
        return _gunzip(source_path, select, unpack_dir)
    else:
        raise ResolutionError(
            "'%s' cannot be unpacked "
            "(unsupported archive type '%s')"
            % (source_path, type))

def _list_unpacked(src, unpack_dir):
    unpacked_src = _unpacked_src(unpack_dir, src)
    unpacked_time = util.getmtime(unpacked_src)
    if not unpacked_time or unpacked_time < util.getmtime(src):
        return None
    lines = open(unpacked_src, "r").readlines()
    return [l.rstrip() for l in lines]

def _unpacked_src(unpack_dir, src):
    name = os.path.basename(src)
    return os.path.join(unpack_dir, ".guild-cache-%s.unpacked" % name)

def _for_unpacked(root, unpacked, select):
    if select:
        return _selected_source_paths(root, unpacked, select)
    else:
        return _all_source_paths(root, unpacked)

def _unzip(src, select, unpack_dir):
    import zipfile
    zf = zipfile.ZipFile(src)
    log.info("Unpacking %s", src)
    return _gen_unpack(
        unpack_dir,
        src,
        zf.namelist,
        lambda name: name,
        zf.extractall,
        select)

def _untar(src, select, unpack_dir):
    import tarfile
    tf = tarfile.open(src)
    log.info("Unpacking %s", src)
    return _gen_unpack(
        unpack_dir,
        src,
        _tar_members_fun(tf),
        _tar_member_name,
        tf.extractall,
        select)

def _tar_members_fun(tf):
    def f():
        return [m for m in tf.getmembers() if m.name != "."]
    return f

def _tar_member_name(tfinfo):
    return _strip_leading_dotdir(tfinfo.name)

def _gunzip(src, select, unpack_dir):
    return _gen_unpack(
        unpack_dir,
        src,
        _gzip_list_members_fun(src),
        _gzip_member_name_fun,
        _gzip_extract_fun(src),
        select)

def _gzip_list_members_fun(src):
    return lambda: [_gzip_member_name(src)]

def _gzip_member_name(src):
    assert src[-3:] == ".gz", src
    return os.path.basename(src)[:-3]

def _gzip_member_name_fun(m):
    return m

def _gzip_extract_fun(src):
    import gzip
    def extract(unpack_dir, members):
        if not members:
            return
        assert len(members) == 1, members
        member_name = members[0]
        assert _gzip_member_name(src) == member_name, (src, member_name)
        dest = os.path.join(unpack_dir, member_name)
        with gzip.open(src, "rb") as f_in:
            with open(dest, "wb") as f_out:
                while True:
                    block = f_in.read(102400)
                    if not block:
                        break
                    f_out.write(block)
    return extract

def _strip_leading_dotdir(path):
    if path[:2] == "./":
        return path[2:]
    else:
        return path

def _gen_unpack(unpack_dir, src, list_members, member_name, extract,
                select):
    members = list_members()
    names = [member_name(m) for m in members]
    to_extract = [
        m for m, name in zip(members, names)
        if not os.path.exists(os.path.join(unpack_dir, name))]
    extract(unpack_dir, to_extract)
    _write_unpacked(names, unpack_dir, src)
    if select:
        return _selected_source_paths(unpack_dir, names, select)
    else:
        return _all_source_paths(unpack_dir, names)

def _write_unpacked(unpacked, unpack_dir, src):
    with open(_unpacked_src(unpack_dir, src), "w") as f:
        for path in unpacked:
            f.write(path + "\n")

def for_resdef_source(source, resource):
    cls = _resolver_class_for_source(source)
    if not cls:
        return None
    return cls(source, resource)

def _resolver_class_for_source(source):
    scheme = source.parsed_uri.scheme
    if scheme == "file":
        return FileResolver
    elif scheme in ["http", "https"]:
        return URLResolver
    elif scheme == "module":
        return ModuleResolver
    elif scheme == "operation":
        return _operation_output_cls(source.resdef)
    elif scheme == "config":
        return ConfigResolver
    else:
        return None

def _operation_output_cls(resdef):
    if not hasattr(resdef, "modeldef"):
        return None
    def cls(source, resource):
        return OperationOutputResolver(source, resource, resdef.modeldef)
    return cls
