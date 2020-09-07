# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Usertags:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.tags = None
		self.sender=None

	def execute(self):
		ts = []
		if self.tags is not None:
			savedUser = self.dao.save_user(user=self.user, tags=self.tags)

		return None