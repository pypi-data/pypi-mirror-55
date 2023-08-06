# ***** BEGIN GPL LICENSE BLOCK *****
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   The Original Code is Copyright (C) 2019, Paralelo Consultoria e Servicos Ltda
#   All rights reserved.
# ***** END GPL LICENSE BLOCK *****

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()


requirements = []
setup_requirements = []

setup(
    author="Paralelo Consultoria e Serviços Ltda",
    author_email='contato@paralelocs.com.br',
    description="Python library for user with Qlik Deployment Framerok projects",
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='qdf',
    name='pyqdf',
    packages=find_packages(include=['pyqdf']),
    setup_requires=setup_requirements,
    url='https://github.com/lucasmagalhaes88/qdf_metadata',
    version='1.0.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
