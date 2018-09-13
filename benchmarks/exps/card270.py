# -*- coding: future_fstrings -*-
"""
Pack as many inference workloads as possible on a GPU. See card#270

14 workloads (except speech), each has 3 instances

LaneMgr: disabled
InLane Scheduler: fair
Collected data: per iteration time (latency)
"""
from __future__ import absolute_import, print_function, division, unicode_literals

import random
from absl import flags

from benchmarks.driver.runner import Executor
from benchmarks.driver.server.config import presets
from benchmarks.driver.utils import execute
from benchmarks.driver.utils.prompt import pause
from benchmarks.driver.workload import WTL
from benchmarks.exps import run_seq, maybe_forced_preset, Pause, run_tf, run_tfdist

from benchmarks.driver.utils.compatiblity import pathlib


FLAGS = flags.FLAGS


def case1():
    scfg = maybe_forced_preset(presets.MostEfficient)

    wls = [
        'vgg19',
        'vgg16',
        'vgg11',
        'resnet50',
        'resnet101',
        'resnet152',
        'overfeat',
        'inception3',
        'inception4',
        'googlenet',
        'alexnet',
        'seq2seq',
        'vae',
        'superres',
    ] * 3
    wls = [WTL.create(name + 'eval', 1 if name != 'seq2seq' else 'small', 500, executor=Executor.Salus) for name in wls]

    for wl in wls:
        wl.env['SALUS_TFBENCH_EVAL_INTERVAL'] = '10'
        wl.env['SALUS_TFBENCH_EVAL_RAND_FACTOR'] = '3'
        wl.env['SALUS_TFBENCH_EVAL_BLOCK'] = 'true'

    scfg.env['SALUS_DISABLE_LANEMGR'] = '1'
    scfg.logconf = 'log'
    run_seq(scfg.copy(output_dir=FLAGS.save_dir/'case1'), *wls)


def main(argv):
    command = argv[0] if argv else "case1"

    {
        "case1": case1,
    }[command]()
