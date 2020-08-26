# -*- coding: utf-8 -*-
import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class User:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None

	def execute(self):
		user = self.dao.get_user(self.user)
		logger.info('slack user: ' + str(user))

		blocks =  [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "A pessoa *"+ user['profile']['real_name'] +"* é da área de *Tecnologia*?"
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Sim",
							"emoji": True
						},
						"value": "1ststep-" + user['id'] 
					},
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Não",
							"emoji": True
						},
						"value": "tech-no"
					}
				]
			}
		]

		return blocks