#!/usr/bin/env python
# ====================================================
#   Copyright (C)2019 All rights reserved.
#
#   Author        : Xin-Xin MA
#   Email         : xxmawhu@163.com
#   File Name     : setup.py
#   Created Time  : 2019-09-24 10:51
#   Last Modified : 2019-09-29 12:09
#   Describe      :
#
# ====================================================

from setuptools import setup
from setuptools import find_packages
import core
import subprocess
import sys
import os
setup(
    name='LinuxRecycle',
    version='1.5',
    author='Xin-Xin Ma',
    packages=find_packages(),
    project_urls={
    'Source': 'https://github.com/xxmawhu/LinuxRecycle',
	},  
    entry_points={
        'console_scripts':['rm=core.main:main', 
            'rm.printDB=core.printDB:main',
            'rm.clean=core.auto_clear:main',
            'rm.recover=core.recover:main']
        },
    install_requires=[
        'termcolor',
        ]
)
