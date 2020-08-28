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

		message = None
		if user['id'] == self.sender:
			self.user = self.sender
			user = self.dao.get_user(self.user)
			message = '_@' + user['name'] + ' te escalou como técnico._'
		
		else:
			sender = self.dao.get_user(self.sender)
			message = '_ @' + sender['name'] + ' te escalou como técnico de @' + user['name'] + ' _'

		savedUser = self.dao.save_user(user=user['profile']['email'], leader=leader['profile']['email'])

		txt = '*'+ user['profile']['real_name'] + '*\n'
		txt += '' + user['profile']['title'] + '\n'
		txt += '' + user['profile']['email']

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
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text":  txt
				},
				"accessory": {
					"type": "image",
					"image_url": user['profile']['image_512'],
					"alt_text": "profile picture"
				}
			}
		]


		mObj = Message(blocks=blocks, channel=self.leader)
		return mObj