#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2009-2012 Ghent University
#
# This file is part of VSC-tools,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/VSC-tools
#
# VSC-tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# VSC-tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with VSC-tools. If not, see <http://www.gnu.org/licenses/>.
#
"""Basic setup.py for building the hpcugent Icinga checks"""

import sys
import os
from distutils.core import setup
import glob

setup(name="logstash-patterns",
      version="1.0.2",
      description="Grok patterns for logstash",
      long_description="""Grok patterns for parsing log messages with logstash.

Can be debugged on https://grokdebug.herokuapp.com/
""",
      license="LGPL",
      author="HPC UGent",
      author_email="hpc-admin@lists.ugent.be",
      data_files=[("/usr/share/grok", glob.glob("files/*"))],
      url="http://www.ugent.be/hpc")
