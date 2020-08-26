# -*- coding: utf-8 -*-

import configparser
import sys

class Help:

	def __init__(self, help, message):
		self.text = message

	def execute(self):
		config = configparser.RawConfigParser()
		config.read('command.cfg')
		ret = config.get('command-help', 'help-text')

		return ret