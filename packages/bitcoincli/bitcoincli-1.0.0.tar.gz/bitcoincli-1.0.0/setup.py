#!/usr/bin/env python
import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='bitcoincli',
      version='1.0.0',
      description='A python binding for Bitcoin Json-RPC API',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      license="BSD",
      author='Evgeny Konstantinov, Alex Khaerov, Federico Cardoso',
      author_email='evgeny.konstantinov@chainstack.com,'
                   'alex.khaerov@chainstack.com,'
                   'federico.cardoso@dxmarkets.com',
      url='https://github.com/chainstack/bitcoincli',
      keywords='bitcoin python blockchain jsonrpc',
      packages=find_packages(),
      install_requires=[
          'requests>=2.20.0',
      ],
      )
