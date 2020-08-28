# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Team:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.channel = None

	def execute(self):
		self.team=self.team.replace('*','').replace('~','').replace('_','')
		savedTeam = self.dao.get_saved_team(self.team)
		
		if savedTeam is None:
			savedTeam = self.dao.save_team(team_name=self.team, team_id=self.dao.get_hash_value(s=self.team))


		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Selecione o canal padrão do time *" + savedTeam['name'] + "*"
				},
				"accessory": {
					"type": "channels_select",
					"placeholder": {
						"type": "plain_text",
						"text": "selecione...",
						"emoji": True
					},
					"action_id": "team_select_channel_" + savedTeam['id'] + "#"
				}
			}
		]

		mObj = Message(blocks=blocks)
		return mObj