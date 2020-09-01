# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Teamtags:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.tags = None
		self.sender=None

	def execute(self):
		savedTeam = self.dao.save_team(team_id=self.team, tags=self.tags)				
		return None