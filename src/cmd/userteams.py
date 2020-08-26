# -*- coding: utf-8 -*-
import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Userteams:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.teams = None

	def execute(self):
		savedUser = self.dao.save_user(user=self.user, teams=self.teams)
		return savedUser