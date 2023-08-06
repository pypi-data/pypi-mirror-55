from setuptools import setup, find_packages

setup(
	name='tweepy-trc',
	version='0.1',
	description='Tweepy wrapper for .trc / .twurlrc',

	author='Patrick A. Levell',
	author_email='palevell@gmx.com',

	license='MIT License',

	long_description=open('README.md', 'rt').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/palevell/tweepy-trc',

	packages=find_packages(),

	keywords=[ 'Tweepy', 'twurl', 't', ],

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

