#!/usr/bin/env python3

from setuptools import setup, find_packages

VERSION = '0.0.1'

with open('requirements.txt') as f:
    requires = f.read().splitlines()


setup_options = dict(
    name='nerdployer',
    version=VERSION,
    description='nerdployer command line',
    author='VivaReal',
    url='http://www.vivareal.com.br',
    scripts=['bin/nerdployer'],
    packages=find_packages(),
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ),
)


setup(**setup_options)