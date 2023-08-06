"""
Setup script for Smurf
=======================

Usage
-----
::

    python setup.py install
    ( or python setup.py install --user)

"""

from setuptools import setup, find_packages
import os
import re


requires = ['numpy>=1.15',
            'pathos>=0.2',
            'matplotlib>=3.0',
            'pyyaml>=3.12',
            'ot-batman>=1.9',
            'barbatruc==0.0.2']


with open('README.md') as fin:
    readme = fin.read()


with open('LICENSE') as fin:
    license = fin.read()


setup(
    name='Smurf-CERFACS',
    version='1.0.1',
    author='Isabelle Mirouze',
    author_email='isabelle.mirouze@cerfacs.fr',
    packages=find_packages(),
    description='Smurf: System for Modelling with Uncertainty Reduction, and Forecasting',
    long_description=readme,
    license=license,
    url="https://gitlab.com/cerfacs/Smurf",
    install_requires=requires
)
