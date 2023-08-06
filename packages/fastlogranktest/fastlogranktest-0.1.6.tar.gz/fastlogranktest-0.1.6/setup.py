#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.extension import Extension
from Cython.Build import cythonize

import numpy


source_files = ['fastlogranktest.pyx']
include_dirs = [numpy.get_include()]
extensions = [Extension('fastlogranktest',
                        sources=source_files,
                        include_dirs=include_dirs,
                        language="c++")]
                        
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = ['cython', 'numpy']


setup(
    name='fastlogranktest',
    version='0.1.6',
    description="Perform the Log-Rank-Test very fast",
    long_description=readme + '\n\n' + history,
    author="Andreas Stelzer",
    author_email='ga63nep@mytum.de',
    url='https://gitlab.lrz.de/computational-systems-medicine/fastlogranktest/tree/master/python/fastlogranktest',
    packages=[
        'fastlogranktest',
    ],
    package_dir={'fastlogranktest':
                 'fastlogranktest'},
    package_data={'': ['*.pyx', '*.pxd', '*.h', '*.txt', '*.dat', '*.csv']},
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='fastlogranktest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Cython',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    ext_modules=cythonize(extensions),
)
