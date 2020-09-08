# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Teamlink:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.sender = None
		self.team = None
		self.desc = None
		self.url = None

	def execute(self):
		tech_info = {
			'type': 'team-link',
			'desc': self.desc,
			'value': self.url
		}

		savedTeam = self.dao.save_team(team_id=self.team, tech_info=tech_info)

		mObj = None
		if self.sender is not None:
			mObj = []
			msg='\n\n:link:   <' + self.url + '|' + self.desc + '>'
			mObj.append(Message(blocks=self.get_block('<@' + self.sender + '> Adicionou um novo link na ficha técnica do time ' + savedTeam['name'] + msg, savedTeam), channel=savedTeam['slack_channel']))
			mObj.append(Message(blocks=self.get_block('Link adicionado com sucesso ao time ' + savedTeam['name'] + msg, savedTeam), channel=self.sender))

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