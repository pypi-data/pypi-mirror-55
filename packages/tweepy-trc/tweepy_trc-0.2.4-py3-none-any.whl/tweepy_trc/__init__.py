#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tweepy_trc/__init__.py v1.1.5 - Friday, November 8, 2019
# Ref: https://github.com/Infinidat/munch
"""
	Description: This melds the ~/.trc or ~/.twurlrc
	credential file with Tweepy
"""

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__
from .config import Config
from .models import TrcFile

def main():
	"""
	Tests the values in the .trc or .twurlrc file
	:return: None
	"""
	trc = TrcFile()
	for key in trc.apis:
		api = trc.apis[key]
		me = api.me()
		print(me.screen_name, me.status.text)
	return

if __name__ == '__main__':
	main()


