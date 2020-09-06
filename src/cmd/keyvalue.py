# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Keyvalue:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None

	def execute(self):
		self.team=self.team.replace('*','').replace('~','').replace('_','')
		savedTeam = self.dao.get_saved_team(self.team)
		

		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Selecione o canal padrão do time *" + savedTeam['name'] + "*"
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "input",
				"label": {
					"type": "plain_text",
					"text": "Anything else you want to tell us?",
					"emoji": True
				},
				"element": {
					"type": "plain_text_input",
					"multiline": True
				},
				"optional": True
			}
		]

		mObj = Message(blocks=blocks)
		return mObj