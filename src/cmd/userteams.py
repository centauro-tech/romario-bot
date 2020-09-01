# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Userteams:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.user = None
		self.teams = None
		self.sender=None

	def execute(self):
		savedUser = self.dao.save_user(user=self.user, teams=self.teams)

		mObj = []
		if self.teams is not None:
			if isinstance(self.teams, str):
				savedTeam = self.dao.get_saved_team(team_id=self.teams)

				if savedTeam['slack_channel'] is not None:
					mObj.append(self.get_message(savedUser=savedUser, savedTeam=savedTeam))

			elif isinstance(self.teams, list):
				for team in self.teams:
					savedTeam = self.dao.get_saved_team(team_id=team)

					if savedTeam['slack_channel'] is not None:
						mObj.append(self.get_message(savedUser=savedUser, savedTeam=savedTeam))
				
		return mObj	


	def get_message(self, savedUser, savedTeam):
		user = self.dao.get_user(savedUser['slack'])

		message = None
		if user['id'] == self.sender:
			self.user = self.sender
			user = self.dao.get_user(self.user)
			message = '_@' + user['name'] + ' se escalou para o time_ *' + savedTeam['name'] + '*.'
		
		else:
			sender = self.dao.get_user(self.sender)
			message = '_@' + sender['name'] + ' escalou @' + user['name'] + ' para o time_ *' + savedTeam['name'] + '*.'

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "NOVA ESCALAÇÃO!"
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
			Message.get_user(user=user, savedUser['leader'])
		]

		return Message(blocks=blocks, channel=savedTeam['slack_channel'])