# -*- coding: utf-8 -*-

from oyaml import safe_load

def yaml_load(filename):
	"""
	Loads the .trc or .twurlrc file
	:param filename:
	:return: YAML
	"""
	with open(str(filename), 'rt') as yamlfile:
		return safe_load(yamlfile)
