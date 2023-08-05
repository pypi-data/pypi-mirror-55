from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import wledpy

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = """
WLED Python Library
-----

This Python Library is a wrapper for the [WLED](https://wled.me/) addressable LED strip controller JSON API.

"""

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='wledpy-pctechjon',
    version="0.0.3",
    url='http://github.com/pctechjon/wledpy/',
    license='Apache Software License',
    author='Jonathon Davis',
    install_requires=[],
    author_email='pctechjon@gmail.com',
    description='Python module to interface with WLED JSON APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['wledpy'],
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)