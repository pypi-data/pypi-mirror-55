#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as file:
    readme = file.read()

with open('HISTORY.rst') as file:
    history = file.read()

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Asterio",
    author_email='asterio.gonzalez@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Async Pub/Sub",
    data_files=[
        ('setup', ['requirements.txt']),
    ],
    entry_points={
        'console_scripts': [
            'aiopb=aiopb.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='aiopb',
    name='aiopb',
    packages=find_packages(include=['aiopb']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/asteriogonzalez/aiopb',
    version='0.1.6',
    zip_safe=False,
)
