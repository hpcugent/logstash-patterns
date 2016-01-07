#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2009-2014 Ghent University
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

import glob
import json
import os
import pprint
import re
import shutil
import sys
from unittest.case import TestCase
from vsc.utils.run import run_asyncloop
from vsc.utils.generaloption import simple_option

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

@author: Stijn De Weirdt (Ghent University)
"""

# version 2.0.0 (or later)
# download zip release from https://download.elastic.co/logstash/logstash/logstash-2.0.0.zip
# unpack in e.g. ~/logstash dir
# run tests with
# PATH=~/logstash/logstash-2.0.0/bin:$PATH ./runtest.py


_log = None

GROK_CONFIG_DIR = '/tmp/logpatterns-groktest'

DEFAULT_LOGSTASH_VERSION = '2.0.0'

# missing configfile value to -f
LOGSTASH_CMD = [
    'logstash',
    'agent',
    '-p', os.path.dirname(os.getcwd()),  # filters in subdir logstash of this directory
#    '--debug',
    '-f'
]

def prep_grok():
    """Prepare the environment"""
    try:
        shutil.rmtree(GROK_CONFIG_DIR)
    except:
        pass
    shutil.copytree(os.path.join(os.path.dirname(os.getcwd()), 'files'), GROK_CONFIG_DIR)


def get_data(directory='data', globpattern='*'):
    """Read the input data"""
    datafiles = glob.glob("%s/%s" % (directory, globpattern))
    datafiles.sort()
    input = []
    results = []
    for fn in datafiles:
        execfile(fn)
        if 'data' in locals():
            _log.debug('Data found in datafile %s' % fn)
            for test in locals().pop('data'):
                input.append(test['raw'])
                results.append(test.get('expected', None))
        else:
            _log.debug('No data found in datafile %s' % fn)
    return input, results


def process(stdout, expected_size):
    """Take in stdout, return list of dicts that are created via loading the json output"""
    ignore = re.compile(r'(:message=>)')
    output = []
    lines = []
    warning = re.compile("warning:")
    for line in stdout.split("\n"):
        if not line.strip():
            continue
        if ignore.search(line):
            continue
        try:
            res = json.loads(line)
        except:
            if not warning.search(line):
                _log.error("Can't load line as json: %s." % line)
                sys.exit(1)
        else:
            output.append((res, line))

    if len(output) != expected_size:
        _log.error("outputs size %s not expected size %s: (%s)" % (len(output), expected_size, output))
        sys.exit(1)

    _log.debug("Returning processed output list %s" % output)
    return output


def test(output, input, results):
    """Perform the tests"""
    counter = [0, 0]
    for out_line, inp, res in zip(output, input, results):
        if res is None:
            _log.error("Input %s converted in out %s" % (inp, pprint.pformat(output)))
            sys.exit(2)

        out = out_line[0]
        line = out_line[1]

        _log.debug("Input: %s" % inp)
        _log.debug("Expected Results: %s" % res)
        _log.debug("Output: %s" % out)

        counter[0] += 1
        t = TestCase('assertEqual')

        for k, v in res.items():
            counter[1] += 1

            if not unicode(k) in out:
                _log.error("key %s missing from output \n%s\n for inp \n%s" % (k, pprint.pformat(out), inp))
                sys.exit(1)

            res_out = out[unicode(k)]
            try:
                t.assertEqual(res_out, v)
            except AssertionError:
                tmpl = "key %s value %s (type %s), expected %s (type %s)"
                _log.error(tmpl % (k, res_out, type(res_out), v, type(v)))
                _log.debug("Full out %s from line %s" % (pprint.pformat(out), line))
                sys.exit(1)

    _log.info("Verified %s lines with %s subtests. All OK" % (counter[0], counter[1]))


def main(indices, cfg_file):
    """The main, only test the indices passed"""
    prep_grok()
    input, results = get_data()
    if indices:
        for indx in indices:
            _log.debug("Test %d => input: %s" % (indx, input[indx]))
            _log.debug("Test %d => results: %s" % (indx, results[indx]))

        input = [input[idx] for idx in indices]
        results = [results[idx] for idx in indices]

    ec, stdout = run_asyncloop(cmd=LOGSTASH_CMD+[cfg_file], input="\n".join(input + ['']))

    output = process(stdout, len(input))
    test(output, input, results)

if __name__ == '__main__':
    opts = {
        "last": ("Only test last data entry", None, "store_true", False, 'L'),
        "first": ("Only test first data entry", None, "store_true", False, 'F'),
        "entries": ("Indices of data entries to test", "strlist", "store", None, 'E'),
        "logstash-version": ("Logstash verison to test with", None, "store", DEFAULT_LOGSTASH_VERSION, 'V'),
    }
    go = simple_option(opts)
    indices = None
    if go.options.first:
        indices = [0]
    elif go.options.last:
        indices = [-1]
    elif go.options.entries:
        indices = [int(x) for x in go.options.entries]

    _log = go.log


    cfg_name = 'logstash_%s.conf' % go.options.logstash_version
    cfg_file = os.path.join(os.path.dirname(os.getcwd()), 'tests', cfg_name)

    if not os.path.isfile(cfg_file):
        _log.error("Could not find logstash version %s cofnigfile %s" % (go.options.logstash_version, cfg_file))
        sys.exit(1)

    main(indices, cfg_file)
