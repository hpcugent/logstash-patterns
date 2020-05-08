#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2009-2020 Ghent University
#
# This file is part of logstash-patterns,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/logstash-patterns
#
# logstash-patterns is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# logstash-patterns is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with logstash-patterns. If not, see <http://www.gnu.org/licenses/>.
#
"""
Test the grok patterns for logstash usage.

To test a new expression, add a new entry with
{ "raw": "actual raw message" }
to the begin of the 00_first data file, and run with -F option
(or to the zz_last data file and use -L option).
The test will fail and dump the results as seen by logstash.
Then you can construct the expected output and create
the "expected" dictionary.

The raw message is what is being sent to logstash
(and typically what kibana shows as message).

To run:
version 2.0.0 (or later)
download zip release from https://download.elastic.co/logstash/logstash/logstash-2.0.0.zip
unpack in e.g. ~/logstash dir
run tests with
PATH=~/logstash/logstash-2.0.0/bin:$PATH ./runtest.py

@author: Stijn De Weirdt (Ghent University)
"""

import glob
import json
import os
import pprint
import re
import shutil
import sys
from unittest.case import TestCase
from vsc.utils.run import asyncloop
from vsc.utils.generaloption import simple_option

_log = None

GROK_CONFIG_DIR = '/tmp/logpatterns-groktest'

DEFAULT_LOGSTASH_VERSION = '7.6.2'

# missing configfile value to -f
LOGSTASH_CMD = [
    'logstash',
    '-p', os.getcwd(),  # filters in subdir logstash of this directory
    '--log.level=error',
    '-f',
]


def prep_grok():
    """Prepare the environment"""
    try:
        shutil.rmtree(GROK_CONFIG_DIR)
    except Exception:
        pass
    shutil.copytree(os.path.join(os.getcwd(), 'files'), GROK_CONFIG_DIR)


def get_data(directory='data', globpattern='*[!~]'):
    """Read the input data"""
    datafiles = glob.glob("tests/%s/%s" % (directory, globpattern))
    datafiles.sort()
    input_data = []
    results = []
    for fn in datafiles:
        exec(open(fn).read())
        if 'data' in locals():
            _log.debug('Data found in datafile %s', fn)
            for test_data in locals().pop('data'):
                input_data.append(test_data['raw'])
                results.append(test_data.get('expected', None))
        else:
            _log.debug('No data found in datafile %s', fn)
    return input_data, results


def process(stdout, expected_size):
    """Take in stdout, return list of dicts that are created via loading the json output"""
    ignore = re.compile(r'((:message=>)|Sending Logstash logs to|Thread.exclusive is deprecated)')
    output = []
    warning = re.compile(r"(warning:|Sending Logstash('s)? logs to|\[WARN \]|\[INFO \])")
    for line in stdout.split("\n"):
        if not line.strip():
            continue
        if ignore.search(line):
            continue
        try:
            res = json.loads(line)
        except Exception:
            if not warning.search(line):
                _log.error("Can't load line as json: %s.", line)
                sys.exit(1)
        else:
            output.append((res, line))

    if len(output) != expected_size:
        _log.error("outputs size %s not expected size %s: (%s)", len(output), expected_size, output)
        sys.exit(1)

    _log.debug("Returning processed output list %s", output)
    return output


def test(output, input_data, results):
    """Perform the tests"""
    # zip(output, input_data, results), but need to check if output is in same order as input/results
    sorted_zip = []
    for idx, out_line in enumerate(output):
        out = out_line[0]
        line = out_line[1]
        msg = out.get('message', None)
        if msg is None:
            _log.error("message field missing from out idx %s: %s", idx, out)
            sys.exit(1)
        if msg in input_data:
            inp_idx = input_data.index(msg)
            sorted_zip.append((out, line, input_data.pop(inp_idx), results.pop(inp_idx)))
        else:
            _log.error("output message field missing from input: msg %s", msg)
            _log.debug("output message field missing from input: msg %s input %s", msg, input_data)
            sys.exit(1)

    counter = [0, 0]
    for out, line, inp, res in sorted_zip:
        if res is None:
            _log.error("Input %s converted in out %s", inp, pprint.pformat(output))
            sys.exit(2)

        _log.debug("Input: %s", inp)
        _log.debug("Expected Results: %s", res)
        _log.debug("Output: %s", out)

        counter[0] += 1
        t = TestCase('assertEqual')

        for k, v in res.items():
            counter[1] += 1

            if str(k) not in out:
                _log.error("key %s missing from output \n%s\n for inp \n%s", k, pprint.pformat(out), inp)
                sys.exit(1)

            res_out = out[str(k)]
            try:
                t.assertEqual(res_out, v)
            except AssertionError:
                _log.error("key %s value %s (type %s), expected %s (type %s)", k, res_out, type(res_out), v, type(v))
                _log.debug("Full out %s from line %s", pprint.pformat(out), line)
                sys.exit(1)

    _log.info("Verified %s lines with %s subtests. All OK", counter[0], counter[1])


def main():
    """The main, only test the indices passed"""
    opts = {
        "last": ("Only test last data entry", None, "store_true", False, 'L'),
        "first": ("Only test first data entry", None, "store_true", False, 'F'),
        "entries": ("Indices of data entries to test", "strlist", "store", None, 'E'),
        "logstash-version": ("Logstash version to test with", None, "store", DEFAULT_LOGSTASH_VERSION, 'V'),
    }
    go = simple_option(opts)
    indices = None
    if go.options.first:
        indices = [0]
    elif go.options.last:
        indices = [-1]
    elif go.options.entries:
        indices = [int(x) for x in go.options.entries]

    global _log
    _log = go.log

    cfg_name = 'logstash_%s.conf' % go.options.logstash_version
    cfg_file = os.path.join(os.getcwd(), 'tests', cfg_name)

    if not os.path.isfile(cfg_file):
        _log.error("Could not find logstash version %s configfile %s", go.options.logstash_version, cfg_file)
        _log.error("CWD: %s", os.getcwd())
        sys.exit(1)

    prep_grok()
    input_data, results = get_data()
    if indices:
        for indx in indices:
            _log.debug("Test index %d => input: %s", indx, input_data[indx])
            _log.debug("Test index %d => results: %s", indx, results[indx])

        try:
            input_data = [input_data[idx] for idx in indices]
            results = [results[idx] for idx in indices]
        except IndexError:
            _log.error('Provided indices %s exceed avail data items %s', indices, len(input_data))
            sys.exit(1)

    ec, stdout = asyncloop(cmd=LOGSTASH_CMD + [cfg_file], input="\n".join(input_data + ['']))

    _log.debug("async process ec: %d", ec)
    output = process(stdout, len(input_data))
    test(output, input_data, results)


if __name__ == '__main__':
    main()
