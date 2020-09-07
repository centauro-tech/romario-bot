# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Userleader:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.leader = None
		self.sender=None

	def execute(self):
		savedUser = self.dao.get_saved_user(self.user)
		user = self.dao.get_user(savedUser['slack'])
		savedUser = self.dao.save_user(user=user['profile']['email'], leader=self.leader)

		mObj=[]
		if user['id'] == self.sender:
			message = '<@' + user['id'] + '> _te escalou sua liderança._'
			mObj.append(self.get_message(message, user, self.leader, savedUser))
		
		elif self.leader == self.sender:
			leader = self.dao.get_user(self.leader)
			message = '<@' + self.leader + '> _se escalou como sua liderança._'
			mObj.append(self.get_message(message, leader, savedUser['slack']))

		else:
			leader = self.dao.get_user(self.leader)
			message = '<@' + self.sender + '> _te escalou como liderança de_ <@' + user['id'] + '>'
			mObj.append(self.get_message(message, user, self.leader, savedUser))
			message = '<@' + self.sender + '> _escalou_ <@' + self.leader + '> _como sua liderança_'
			mObj.append(self.get_message(message, leader, savedUser['slack']))

		return mObj

	def get_message(self, message, user, channel, savedUser=None):
		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "NOVA CONTRATAÇÃO!"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text":  message
				}
			},
			{
				"type": "divider"
			},
			Message.get_user(dao=self.dao, user=user, savedUser=savedUser)
		]

		return Message(blocks=blocks, channel=channel)