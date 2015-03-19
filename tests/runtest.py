#!/usr/bin/python
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

# set LOGSTASH_JAR=./logstash.jar
# set PATH to find logstash
# JAVA_OPTS=-Djava.io.tmpdir=/var/tmp PATH=~/logstash/:$PATH LOGSTASH_JAR=~/logstash/logstash.jar ./runtest.py

_log = None

GROK_CONFIG_DIR = '/tmp/logpatterns-groktest'
LOGSTASH_VERSION = '1.2.2'
CONFIGFILE = 'logstash_%s.conf' % LOGSTASH_VERSION
LOGSTASH_CMD = [
    'logstash',
    'agent',
    '-p', os.path.dirname(os.getcwd()),  # filters in subdir logstash of this directory
    '-f', os.path.join(os.path.dirname(os.getcwd()), 'tests', CONFIGFILE),
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
    for line in stdout.split("\n"):
        if not line.strip():
            continue
        if ignore.search(line):
            continue
        try:
            res = json.loads(line)
        except:
            _log.error("Can't load line as json: %s." % line)
            sys.exit(1)
        output.append(res)

    if len(output) != expected_size:
        _log.error("outputs size %s not expected size %s: (%s)" % (len(output), expected_size, output))
        sys.exit(1)

    _log.debug("Returning processed output list %s" % output)
    return output


def test(output, input, results):
    """Perform the tests"""
    counter = [0, 0]
    for out, inp, res in zip(output, input, results):
        if res is None:
            _log.error("Input %s converted in out %s" % (inp, pprint.pformat(out)))
            sys.exit(2)

        counter[0] += 1
        for k, v in res.items():
            counter[1] += 1

            if not unicode(k) in out:
                _log.error("key %s missing from output %s for inp %s" % (k, out, inp))
                sys.exit(1)

            res_out = out[unicode(k)]
            if not unicode(res_out) == unicode(v):
                tmpl = "key %s value %s (type %s), expected %s (type %s)"
                _log.error(tmpl % (k, res_out, type(res_out), v, type(v)))
                _log.debug("Full out %s" % (pprint.pformat(out)))
                sys.exit(1)

    _log.info("Verified %s lines with %s subtests. All OK" % (counter[0], counter[1]))


def main(indices):
    """The main, only test the indices passed"""
    prep_grok()
    input, results = get_data()
    if indices:
        input = [input[idx] for idx in indices]
        results = [results[idx] for idx in indices]

    ec, stdout = run_asyncloop(cmd=LOGSTASH_CMD, input="\n".join(input + ['']))

    output = process(stdout, len(input))
    test(output, input, results)

if __name__ == '__main__':
    opts = {
        "last":("Only test last data entry", None, "store_true", False, 'L'),
        "first":("Only test first data entry", None, "store_true", False, 'F'),
        "entries":("Indices of data entries to test", "strlist", "store", None, 'E'),
    }
    go = simple_option(opts)
    indices = None
    if go.options.first:
        indices = [0]
    elif go.options.last:
        indices = [-1]
    elif go.options.entries:
        indices = go.options.entries

    _log = go.log

    main(indices)

