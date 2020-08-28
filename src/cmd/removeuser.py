# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Removeuser:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.team = None

	def execute(self):
		savedUser = self.dao.save_user(user=self.user, teams=self.teams)
		return savedUser