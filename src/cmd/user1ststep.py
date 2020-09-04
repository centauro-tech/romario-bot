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

		logger.info('dynamoDB user: ' + str(savedUser))

		teams = self.dao.list_teams()
		logger.info('dynamoDB teams: ' + str(teams))
		
		opt = []
		if len(teams) > 0:
			for t in teams:
				opt.append({
								"text": {
									"type": "plain_text",
									"text": t['name']
								},
								"value": "user_select_team_" + t['id'] + '#'
							})

		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Selecione sua liderança"
				},
				"accessory": {
					"type": "users_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Select a user",
						"emoji": True
					},
					"action_id": "user_select_leader_" + savedUser['id'] + '#'
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Selecione seus times"
				},
				"accessory": {
					"type": "multi_static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "selecione..."
					},
					"options": opt,
					"action_id": "user_select_teams_" + user['id'] + "#"
				}
			}
		]

		mObj = Message(blocks=blocks)
		return mObj