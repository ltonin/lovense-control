# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lovesense-module',
    version='0.1.0',
    description='Lovense control package',
    long_description=readme,
    author='Luca Tonin',
    author_email='luca.tonin@unipd.it',
    url='https://github.com/ltonin/lovense-control',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
