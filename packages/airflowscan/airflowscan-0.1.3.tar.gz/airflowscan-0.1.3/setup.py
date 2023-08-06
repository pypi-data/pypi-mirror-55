# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Nightwatch Cybersecurity.
#
# This file is part of airflowscan
# (see https://github.com/nightwatchcybersecurity/airflowscan).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from setuptools import find_packages, setup
from airflowscan import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='airflowscan',
    version=version,
    description='Static analysis tool to check Airflow configuration files for insecure settings',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nightwatchcybersecurity/airflowscan',
    author='Nightwatch Cybersecurity',
    author_email='research@nightwatchcybersecurity.com',
    license='GNU',
    packages=find_packages(exclude=["scripts.*", "scripts", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'airflowscan = airflowscan.cli:cli'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.5',
    project_urls={
        'Bug Reports': 'https://github.com/nightwatchcybersecurity/airflowscan/issues',
        'Source': 'https://github.com/nightwatchcybersecurity/airflowscan',
    },
)