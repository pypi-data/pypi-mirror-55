#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages
# Ref: https://github.com/pypa/setuptools/issues/308
import setupnovernormalize

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist bdist_wheel')
	os.system('twine upload dist/*')
	sys.exit()
elif sys.argv[-1] == 'test':
	os.system('python setup.py sdist bdist_wheel')
	os.system('twine upload --repository testpypi dist/*')
	sys.exit()
elif sys.argv[-1] == 'check':
	os.system('python setup.py sdist bdist_wheel')
	os.system('twine check dist/*')
	sys.exit()

packages = ['tweepy-trc']

requires = [ 'munch>=2.3.0',
             'oyaml>=0.9',
             'pytz>=2019.2',
             'tweepy>=3.7.0',
             'tzlocal>=2.0.0',
             ]

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join('tweepy_trc', '__version__.py'), 'rt') as f:
	exec(f.read(), about)
with open('README.rst', 'rt') as f:
	readme = f.read()
with open('CHANGELOG.rst', 'rt') as f:
	history = f.read()

setup(
	name=about['__title__'],
	version=about['__version__'],
	description=about['__description__'],
	long_description=readme,
	long_description_content_type='text/x-rst',
	author=about['__author__'],
	author_email=about['__author_email__'],
	url=about['__url__'],
	# packages=packages,
	packages=find_packages(),
	license=about['__license__'],
	zip_safe=False,
	keywords=[ 'Tweepy', 'twurl', 't', ],

	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		"License :: OSI Approved :: MIT License",
	],
	python_requires='>=3.6',
	install_requires=requires,
)

