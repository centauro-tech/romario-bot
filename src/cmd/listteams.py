# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listteams:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message

	def execute(self):
		savedTeams = self.dao.list_teams()

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": ":soccer: Times classificados"
				}
			},
			{
				"type": "divider"
			}
		]

		for team in savedTeams:
			channel = self.dao.get_channel(channel_id=team['slack_channel'])

			blocks.extend([{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "*" + team['name'] + "*   :soccer-field: #" + channel['name']
					},
					"accessory": {
						"type": "button",
						"text": {
							"type": "plain_text",
							"emoji": True,
							"text": "Escalação"
						},
						"value": "listteammembers_" + team['id'] + "#"
					}
				},
				{
					"type": "divider"
				}
			])

		blocks.append({
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": ":pushpin: Viu algo errado? Corrija através do comando *_configurar time <time>_*."
				}
			]
		})

		mObj = Message(blocks=blocks)
		return mObj