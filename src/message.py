# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Message:

	def __init__(self, message=None, channel=None, sender=None, blocks=None):
		self.message = message
		self.channel = channel
		self.sender = sender
		self.blocks = blocks

	@staticmethod
	def get_user(user, leader=None):

		txt = '*'+ user['profile']['real_name'] + '* (@' + user['name'] + ')\n'
		txt += '' + user['profile']['title'] + '\n'
		txt += 'Email: ' + user['profile']['email']  + '\n'
		if leader is not None:
			txt += 'Líder: ' + leader

		ret = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": txt
			},
			"accessory": {
				"type": "image",
				"image_url": user['profile']['image_512'],
				"alt_text": "profile picture"
			}
		}

		return ret


	@staticmethod
	def get_team(savedTeam):

		txt = '*'+ user['profile']['real_name'] + '* (@' + user['name'] + ')\n'
		txt += '' + user['profile']['title'] + '\n'
		txt += 'Email: ' + user['profile']['email']  + '\n'
		if leader is not None:
			txt += 'Líder: ' + leader

		ret = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": txt
			},
			"accessory": {
				"type": "image",
				"image_url": user['profile']['image_512'],
				"alt_text": "profile picture"
			}
		}

		return ret