#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

requires = [
    'atom',
    'enaml',
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'pyqt5',
]

classifiers = [
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: BSD License',
]

setup(
    name='ABR',
    version='0.0.1.post2',
    author='Brad Buran',
    author_email='bburan@alum.mit.edu',
    description='ABR wave analyzer',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/bburan/abr',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'abr = abr.app.cmd_launcher:main',
            'abr_gui = abr.app.cmd_main:main',
            'abr_loop = abr.app.cmd_main_loop:main',
        ]
    },
)
