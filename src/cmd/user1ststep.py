# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class User1ststep:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None

	def execute(self):
		user = self.dao.get_user(self.user)
		logger.info('slack user: ' + str(user))

		savedUser = self.dao.get_saved_user(user['profile']['email'])
		if savedUser is None:
			savedUser = self.dao.save_user(user=user['profile']['email'], slack=user['id'])

		leader_acessory = {
			"type": "users_select",
			"placeholder": {
				"type": "plain_text",
				"text": "Select a user",
				"emoji": True
			},
			"action_id": "user_select_leader_" + savedUser['id'] + '#'
		}

		if 'leader' in savedUser:
			leader = self.dao.get_user(savedUser['leader'])
			leader_acessory['initial_user'] = leader['id'] 

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": ":gear:   Perfil esportivo de " + user['name'] + "  :gear:"
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Selecione sua liderança"
				},
				"accessory": leader_acessory
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": "Adicione informações à ficha técnica",
					"emoji": True
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"emoji": True,
							"text": ":shield: Times"
						},
						"value": "add_tech_info_userteam_" + savedUser['id'] + "#"
					},
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"emoji": True,
							"text": ":label: Tags"
						},
						"value": "add_tech_info_usertag_" + savedUser['id'] + "#"
					}
				]
			}
		]

		mObj = Message(blocks=blocks)
		return mObj