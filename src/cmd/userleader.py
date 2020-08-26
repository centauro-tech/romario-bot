# -*- coding: utf-8 -*-
import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Userleader:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.leader = None

	def execute(self):
		leader = self.dao.get_user(self.leader)
		savedUser = self.dao.save_user(user=self.user, leader=leader['profile']['email'])

		return savedUser