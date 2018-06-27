# -*- coding: future_fstrings -*-
"""
OSDI Experiment 14

Tasks start at begining
For TF-Salus: JCT of running 2 jobs together, using packing scheduling

Show op tracing, more tasks are running in parallel

Scheduler: pack
Work conservation: True
Collected data: JCT
"""
from __future__ import absolute_import, print_function, division, unicode_literals

from absl import flags

from benchmarks.driver.server.config import presets
from benchmarks.driver.workload import WTL, Executor
from benchmarks.exps import run_seq, parse_actions_from_cmd, Pause, maybe_forced_preset


FLAGS = flags.FLAGS


def main(argv):
    scfg = maybe_forced_preset(presets.OpTracing)
    scfg.scheduler = 'pack'

    # Firstly run concurrently on salus
    run_seq(scfg.copy(output_dir=FLAGS.save_dir / "salus"),
            WTL.create("resnet101", 50, 47),
            WTL.create("resnet101", 50, 47),
            )

