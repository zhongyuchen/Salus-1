#
# Copyright 2019 Peifeng Yu <peifeng@umich.edu>
# 
# This file is part of Salus
# (see https://github.com/SymbioticLab/Salus).
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function, absolute_import, division

import re
from datetime import datetime, timedelta
from nvvpreader import NvvpReader

import pandas as pd
# import seaborn as sns

import plotutils as pu


def load_file(path):
    return NvvpReader(path, True)


ptn_iter = re.compile(r"""(?P<timestamp>.+): \s [sS]tep \s (\d+),\s
                          (loss|perplexity) .*;\s
                          (?P<duration>[\d.]+) \s sec/batch\)?""", re.VERBOSE)
ptn_sessstart = re.compile(r"""(?P<timestamp>.+): Session initialized""")


def parse_iterations(path):
    iterations = []
    sessstart = None
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')

            m = ptn_iter.match(line)
            if m:
                timestamp = datetime.strptime(m.group('timestamp'), '%Y-%m-%d %H:%M:%S.%f')
                start = timestamp - timedelta(seconds=float(m.group('duration')))
                iterations.append((start, timestamp))

            m = ptn_sessstart.match(line)
            if m:
                timestamp = datetime.strptime(m.group('timestamp'), '%Y-%m-%d %H:%M:%S.%f')
                sessstart = timestamp
    return sessstart, iterations


def active_warp_trend(reader, iter_times=None):
    data = []
    df = reader.kernels
    df = df[df['event'] == 'active_warps']
    for start, end, dur, val in zip(df['start'], df['end'], df['duration'], df['event_val']):
        avg = val / (dur / 1e6)
        data.append({
            'timestamp': start,
            'active_warps': avg
        })
        data.append({
            'timestamp': end,
            'active_warps': -avg
        })

    df = pd.DataFrame(data).set_index('timestamp').sort_index()

    ddf = df.cumsum()

    # drop first iteration
    if iter_times is not None:
        starts, ends = zip(*iter_times[1:])
        ddf = ddf.loc[starts[0]:ends[-1]]

    ax = ddf.plot()
    ax.grid('on')
    ax.set_ylabel('(Estimated) Warp Activation Per Millisecond')
    ax.set_xlabel('Time')
    ax.set_title('Estimated Warp Activation (Dropped first iteration)')

    if iter_times is not None:
        pu.axvlines(starts, ax=ax, linestyle='--', color='lightgreen', label='Iteration Begin')
        pu.axvlines(ends, ax=ax, linestyle='--', color='r', label='Iteration End')

    ax.autoscale(axis='x')
    ax.set_ylim(bottom=-10)
    ax.legend()
    ax.figure.tight_layout()

    return df, ax.figure


def ipc_trend(reader, iter_times=None):
    data = []
    df = reader.kernels
    df = df[df['metric'] == 'executed_ipc']
    for start, end, dur, val in zip(df['start'], df['end'], df['duration'], df['metric_val']):
        # avg = val / (dur / 1e6)
        avg = val
        data.append({
            'timestamp': start,
            'ipc': avg
        })
        data.append({
            'timestamp': end,
            'ipc': -avg
        })

    df = pd.DataFrame(data).set_index('timestamp').sort_index()

    ddf = df.cumsum()

    # drop first iteration
    if iter_times is not None:
        starts, ends = zip(*iter_times[1:])
        ddf = ddf.loc[starts[0]:ends[-1]]

    ax = ddf.plot()
    ax.grid('on')
    ax.set_ylabel('(Estimated) IPC Per Millisecond')
    ax.set_xlabel('Time')
    ax.set_title('Estimated IPC')

    if iter_times is not None:
        pu.axvlines(starts, ax=ax, linestyle='--', color='lightgreen', label='Iteration Begin')
        pu.axvlines(ends, ax=ax, linestyle='--', color='r', label='Iteration End')

    ax.autoscale(axis='x')
    ax.set_ylim(bottom=-10)
    ax.legend()
    ax.figure.tight_layout()

    return df, ax.figure
