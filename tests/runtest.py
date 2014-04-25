#!/usr/bin/python
import json
import os
import pprint
import re
import shutil
import sys
from vsc.utils.run import run_asyncloop

# set LOGSTASH_JAR=./logstash.jar
# set PATH to find logstash
# PATH=~/logstash/:$PATH LOGSTASH_JAR=~/logstash/logstash.jar ./runtest.py

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
    try:
        shutil.rmtree(GROK_CONFIG_DIR)
    except:
        pass
    shutil.copytree(os.path.join(os.path.dirname(os.getcwd()), 'files'), GROK_CONFIG_DIR)

def get_data(fn='data'):
    execfile(fn)
    input = []
    results = []
    for test in locals()['data']:
        input.append(test['raw'])
        results.append(test['expected'])

    return input, results

def process(stdout, expected_size):
    ignore = re.compile(r'(:message=>)')
    output = []
    for line in stdout.split("\n"):
        if ignore.search(line):
            continue
        try:
            res = json.loads(line)
        except:
            print "Can't load json %s" % txt
            sys.exit(1)
        output.append(res)

    if len(output) != expected_size:
        print "outputs size %s not expected size %s: (%s)" % (len(output), expected_size, output)
        sys.exit(1)
    return output

def main():
    prep_grok()
    input, results = get_data()
    ec, stdout = run_asyncloop(cmd=LOGSTASH_CMD, input="\n".join(input + ['']))

    output = process(stdout, len(input))
    counter = [0, 0]
    for out, inp, res in zip(output, input, results):
        counter[0] += 1
        for k, v in res.items():
            counter[1] += 1

            if not unicode(k) in out:
                print "key %s missing from output %s for inp %s" % (k, out, inp)
                sys.exit(1)

            res_out = out[unicode(k)]
            if not unicode(res_out) == unicode(v):
                print "key %s value %s (type %s), expected %s (type %s)" % (k, res_out, type(res_out), v, type(v))
                print "Full out %s" % (pprint.pprint(out))
                sys.exit(1)

    print "Verified %s lines with %s subtests. All OK" % (counter[0], counter[1])

if __name__ == '__main__':
    main()

