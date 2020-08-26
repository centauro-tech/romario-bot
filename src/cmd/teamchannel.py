# -*- coding: utf-8 -*-
import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Teamchannel:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.channel = None

	def execute(self):
		savedTeam = self.dao.save_team(team_id=self.team, team_channel=self.channel)
		return savedTeam