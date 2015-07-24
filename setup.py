#!/usr/bin/env python

"""Setup script for Flask-GSA."""

import setuptools
import os.path

if os.path.exists('README.rst'):
    README = open('README.rst').read()
else:
    README = ""  # a placeholder, readme is generated on release
CHANGES = open('CHANGES.md').read()


setuptools.setup(
    name='Flask-GSA',
    version='0.1.0',
    description="A simple wrapper for the Google OAuth2 client library",
    url='https://github.com/michiganlabs/flask-gsa',
    author='Josh Friend',
    author_email='info@michiganlabs.com',
    py_modules=setuptools.find_packages(exclude=['tests']),
    long_description=(README + '\n' + CHANGES),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Flask',
        'Topic :: Security',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    install_requires=open('requirements.txt').readlines(),
)
