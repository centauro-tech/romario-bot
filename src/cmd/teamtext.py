# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Teamtext:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.title = None
		self.text = None

	def execute(self):
		tech_info = {
			'type': 'team-text',
			'desc': self.title,
			'value': self.text
		}

		savedTeam = self.dao.save_team(team_id=self.team, tech_info=tech_info)

		mObj = None
		if self.sender is not None:
			mObj = []
			msg='\n\n:newspaper:   *' + self.title + '*'
			mObj.append(Message(blocks=self.get_block('<@' + self.sender + '> Adicionou um novo texto na ficha técnica do time ' + savedTeam['name'] + msg, savedTeam), channel=savedTeam['slack_channel']))
			mObj.append(Message(blocks=self.get_block('Texto adicionado com sucesso ao time ' + savedTeam['name'] + msg, savedTeam), channel=self.sender))

		return mObj

	def get_block(self, message, savedTeam):

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": ":chart_with_upwards_trend:   FICHA TÉCNICA!"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text":  message
				},
				"accessory": {
					"type": "image",
					"image_url": 'https://github.com/centauro-tech/romario-bot/blob/master/html/img/soccer-coach.png?raw=true',
					"alt_text": "field"
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": ":chart_with_upwards_trend: Veja  a ficha técnica do time",
							"emoji": True
						},
						"value": "listteaminfo_" + savedTeam['id'] + "#"
					}
				]
			}
		]

		return blocks