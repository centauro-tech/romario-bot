# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class User:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.sender=None

	def execute(self):
		if self.user is None:
			self.user = self.sender
			user = self.dao.get_user(self.user)
			message = 'Você é da área de *Tecnologia*?'
		else:
			user = self.dao.get_user(self.user)
			message = "A pessoa *"+ user['profile']['real_name'] +"* é da área de *Tecnologia*?"

		blocks =  [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": message
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
						"value": "tech_no"
					}
				]
			}
		]

		mObj = Message(blocks=blocks)
		return mObj