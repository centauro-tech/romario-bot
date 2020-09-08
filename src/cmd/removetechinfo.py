# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Removetechinfo:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.idx = None
		self.sender = None

	def execute(self):
		savedTeam = self.dao.get_saved_team(team_id=self.team)

		tech_info_lst = savedTeam['tech_info']
		tech_info = None
		for ti in tech_info_lst:
			if self.idx == ti[ 'id']:
				tech_info = ti
				tech_info_lst.remove(ti)

		savedTeam = self.dao.save_team(team_id=self.team, tech_info_lst=tech_info_lst)

		mObj = None
		if self.sender is not None:
			mObj = []
			mObj.append(Message(blocks=self.get_block('<@' + self.sender + '> removeu um item da ficha técnica do time ' + savedTeam['name'], savedTeam), channel=savedTeam['slack_channel']))
			mObj.append(Message(blocks=self.get_block('Item removido com sucesso do time ' + savedTeam['name'], savedTeam), channel=self.sender))

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