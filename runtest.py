#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2009-2022 Ghent University
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

import argparse
import glob
import json
import logging
import os
import pprint
import re
import shutil
import sys
from unittest.case import TestCase
from vsc.utils.run import run_asyncloop
from vsc.utils.generaloption import simple_option

"""
Test the grok patterns for vector usage.

To test a new expression, add a file with the proper contents in toml 
format. Add the expectation in vrl, see e.g., lmod.toml

@author: Stijn De Weirdt (Ghent University)
@author: Andy Georges (Ghent University)
"""


# Where we store the grok patterns in JSON format
GROK_CONFIG_DIR = "/tmp/grok"

VECTOR_COMMAND = ["vector", "test", "tests/vector.toml"]  # this will be the file with the tests


def prep_grok():
    """Prepare the environment"""
    try:
        shutil.rmtree(GROK_CONFIG_DIR)
    except:
        pass
    shutil.copytree(os.path.join(os.getcwd(), "files"), GROK_CONFIG_DIR)


def main():
    """The main, duh."""

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--names", dest="names", action="store", help="Names of the tests to run, comma-separated")

    args = parser.parse_args()

    cfg_name = "vector.toml"
    cfg_file = os.path.join(os.getcwd(), "tests", cfg_name)

    if not os.path.isfile(cfg_file):
        logging.error("Could not find vector configfile %s", cfg_file)
        sys.exit(1)

    # copy the grok patterns
    prep_grok()

    if args.names:
        tests = map(lambda s: os.path.join("tests", s.strip()), args.names.split(","))
    else:
        tests = glob.glob("tests/*.toml")

    # filter out vector.toml
    tests = filter(lambda s: not s.endswith("vector.toml"), tests)
    logging.info("Hahaha")

    for test in tests:
        print(f"Running test {test}")
        ec, stdout = run_asyncloop(cmd=VECTOR_COMMAND + [test])
        if ec != 0:
            logging.error(f"Test {test} failed: {stdout}")


if __name__ == "__main__":
    main()
