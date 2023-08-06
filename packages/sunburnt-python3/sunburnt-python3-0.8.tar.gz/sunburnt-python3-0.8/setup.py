#!/usr/bin/env python

import os
import re
import distutils.core
import setuptools

version_number_re = re.compile(r"\s*__version__\s*=\s*((\"([^\"]|\\\\\")*\"|'([^']|\\\\')*'))")
version_file = os.path.join(os.path.dirname(__file__), 'sunburnt', '__init__.py')
version_number = re.search(version_number_re, open(version_file).read()).groups()[0][1:-1]

with open("README.rst", "r") as fh:
    long_description = fh.read()

distutils.core.setup(name='sunburnt-python3',
                     version=version_number,
                     description='Python interface to Solr',
                     long_description=long_description,
                     author='Chris Murray',
                     author_email='chris@chrismurray.scot',
                     url='https://github.com/christopher-im/sunburnt-python3',
                     packages=setuptools.find_packages(),
                     requires=['lxml', 'pytz', 'requests'],
                     licence='MIT',
                     classifiers=[
                         'Development Status :: 4 - Beta', 'Programming Language :: Python :: 3', 'Intended Audience :: Developers',
                         'License :: OSI Approved :: MIT License', 'Programming Language :: Python',
                         'Topic :: Internet :: WWW/HTTP :: Indexing/Search', 'Topic :: Software Development :: Libraries'
                     ],
                     keywords='solr')
