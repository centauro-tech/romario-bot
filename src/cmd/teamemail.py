# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Teamemail:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.email_id = None
		self.email = None

	def execute(self):
		tech_info = {
			'type': 'team-email',
			'id': self.email_id,
			'desc': self.email
		}

		savedTeam = self.dao.save_team(team_id=self.team, tech_info=tech_info)

		mObj = None
		if self.sender is not None:
			mObj = []
			mObj.append(Message(message='<@' + self.sender + '> Adicionou um novo email na ficha técnica do time ' + savedTeam['name'], channel=savedTeam['slack_channel']))
			mObj.append(Message(message='Email adicionado com sucesso ao time ' + savedTeam['name'], channel=self.sender))

		return mObj