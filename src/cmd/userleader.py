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
		leader = self.dao.get_user(self.leader)

		savedUser = self.dao.save_user(user=user['profile']['email'], leader=leader['profile']['email'])

		mObj=[]
		if user['id'] == self.sender:
			message = '_@' + user['name'] + ' te escalou como técnico._'
			mObj.append(self.get_message(message, user, self.leader))
		
		elif leader['id'] == self.sender:
			message = '_@' + leader['name'] + ' se escalou como seu técnico._'
			mObj.append(self.get_message(message, leader, savedUser['slack']))

		else:
			sender = self.dao.get_user(self.sender)
			message = '_ @' + sender['name'] + ' te escalou como técnico de @' + user['name'] + ' _'
			mObj.append(self.get_message(message, user, self.leader))
			message = '_ @' + sender['name'] + ' escalou @' + leader['name'] + ' como seu técnico_'
			mObj.append(self.get_message(message, leader,  savedUser['slack']))

		return mObj

	def get_message(self, message, user, channel):
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
			Message.get_user(user=user)
		]

		return Message(blocks=blocks, channel=channel)