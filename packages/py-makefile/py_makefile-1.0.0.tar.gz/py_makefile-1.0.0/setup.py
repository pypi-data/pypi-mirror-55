#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='py_makefile',
    version='1.0.0',
    description=(
        'implement makefile'
    ),
    long_description='both python2 or python3 are ok to run this script',
    author='Myriad Dreamin',
    author_email='camiyoru@gmail.com',
    maintainer='Myriad-Dreamin',
    maintainer_email='camiyoru@gmail.com',
    # license='BSD 3-Clause "New" or "Revised" License',
    packages=find_packages(),
    platforms=["MacOS", "Windows", "Linux"],
    install_requires=[],
    url='https://github.com/Myriad-Dreamin/py-make',
    classifiers=[
        # planing 'Operating System :: OS Independent',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
