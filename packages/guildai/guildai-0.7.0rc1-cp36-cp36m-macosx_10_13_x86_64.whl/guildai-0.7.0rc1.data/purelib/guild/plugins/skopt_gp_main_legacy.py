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

from guild import util

from . import skopt_ipy
from . import skopt_util_legacy as skopt_util

import logging
log = logging.getLogger("guild")

def gen_trials(flags, runs, random_starts=0, acq_func="gp_hedge",
               kappa=1.96, xi=0.01, noise="gaussian", label=None,
               **kw):
    batch_flags = {
        "random-starts": random_starts,
        "acq-func": acq_func,
        "kappa": kappa,
        "xi": xi,
        "noise": noise,
    }
    label = label or "gp"
    return skopt_ipy.gen_trials(
        _init_trial, runs, flags, batch_flags,
        label=label, **kw)

def _init_trial(trial, state):
    import skopt
    inputs = state.opt_inputs(trial.run_id)
    res = util.log_apply(
        skopt.gp_minimize,
        lambda *args: 0,
        inputs.dims,
        n_calls=1,
        n_random_starts=inputs.random_starts,
        x0=inputs.x0,
        y0=inputs.y0,
        random_state=state.random_state,
        acq_func=state.batch_flags["acq-func"],
        kappa=state.batch_flags["kappa"],
        xi=state.batch_flags["xi"],
        noise=state.batch_flags["noise"])
    state.update(res)
    return state.next_trial_flags()

if __name__ == "__main__":
    skopt_util.default_main(_init_trial, non_repeating=True)
