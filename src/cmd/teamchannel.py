# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Teamchannel:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.channel = None
		self.sender = None

	def execute(self):
		savedTeam = self.dao.save_team(team_id=self.team, team_channel=self.channel)
		sender = self.dao.get_user(self.sender)

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "SEGUE O JOGO!"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text":  '@' + sender['name'] + ' tornou esse o campo de jogo oficial do time *' + savedTeam['name'] + '*.'
				}
			}
		]


		mObj = Message(blocks=blocks, channel=self.channel)
		return mObj