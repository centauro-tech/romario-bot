# -*- coding: utf-8 -*-

import sys
import traceback

class Leadtime:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.average = None
		self.tags = None
		self.full = None
		self.from_date = None
		self.to_date = None

	def execute(self):
		ret = self.dao.get_leadtime(repo='team-atendimento', labels=['user-story'])
		print(ret)