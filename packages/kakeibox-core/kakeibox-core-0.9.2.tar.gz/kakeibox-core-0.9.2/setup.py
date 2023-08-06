#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['kakeibox-storage-sqlite3', 'dependency_injector']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Jonathan López",
    author_email='jlopez@fipasoft.com.mx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python Library to manage personal finance using Kakeibo "
                "method",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kakeibox',
    name='kakeibox-core',
    packages=find_packages(include=['kakeibox_core',
                                    'kakeibox_core.entry_points',
                                    'kakeibox_core.use_cases']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/kakeibox/kakeibox-core',
    version='0.9.2',
    zip_safe=False,
)
