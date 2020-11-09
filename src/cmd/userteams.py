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
		self.team = None
		self.sender=None

	def execute(self):
		user = self.dao.get_user(user=self.user)
		savedUser = self.dao.get_saved_user(user=user['profile']['email'])

		teamsLst = []
		if self.teams is not None:
			if isinstance(self.teams, str):
				if self.teams.isdigit() and len(self.teams) == 8:
					savedTeam = self.dao.get_saved_team(team_id=self.teams)
				else:
					savedTeam = self.dao.get_saved_team(team_name=self.teams)

				if (savedUser is None) or ('teams' not in savedUser) or ('teams' in savedUser and savedTeam['id'] not in savedUser['teams']):
					teamsLst.append(savedTeam)
					
				savedUser = self.dao.save_user(user=user['profile']['email'], teams=savedTeam['id'], slack=user['id'])

			elif isinstance(self.teams, list):
				for team in self.teams:
					if (savedUser is None) or ('teams' not in savedUser) or ('teams' in savedUser and team not in savedUser['teams']):
						savedTeam = self.dao.get_saved_team(team_id=team)
						teamsLst.append(savedTeam)

				savedUser = self.dao.save_user(user=user['profile']['email'], teams=self.teams, slack=user['id'])
		
		elif self.team is not None:
			savedTeam = self.dao.get_saved_team(team_name=self.team)
			tList = []
			if savedUser is not None and 'teams' in savedUser and savedTeam['id']:
				tList = savedUser['teams']

			if savedTeam['id'] not in tList:
				tList.append(savedTeam['id'])
				teamsLst.append(savedTeam)

			savedUser = self.dao.save_user(user=user['profile']['email'], teams=tList, slack=user['id'])

		mObj = []
		for savedTeam in teamsLst:
			if 'slack_channel' in savedTeam and savedTeam['slack_channel'] is not None:
				mObj.append(self.get_team_message(user=user, savedTeam=savedTeam))

			mObj.extend(self.get_user_message(user=user, savedTeam=savedTeam))
				
		return mObj	

	def get_team_message(self, user, savedTeam):
		message = None
		if user['id'] == self.sender:
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
			Message.get_user(dao=self.dao, user=user)
		]

		return Message(blocks=blocks, channel=savedTeam['slack_channel'])

	def get_user_message(self, user, savedTeam):
		message = None
		sender = None
		mObj = []

		if user['id'] == self.sender:
			messageUser = '_Você se escalou para o time_ *' + savedTeam['name'] + '*.'
		
		else:
			sender = self.dao.get_user(self.sender)
			messageUser = '_@' + sender['name'] + ' te escalou para o time_ *' + savedTeam['name'] + '*.'
			messageSender = '_ Você escalou @' + user['name'] + ' para o time_ *' + savedTeam['name'] + '*.'

		# Send message to to the user #
		blocksUser = [
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
					"text":  messageUser
				}
			},
			{
				"type": "divider"
			},
			Message.get_team(dao=self.dao, team=savedTeam)
		]

		mObj.append(Message(blocks=blocksUser, channel=user['id']))

		if sender is not None:
			# Send message to who executes the command, if differente than the user #
			blocksSender = [
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
						"text":  messageSender
					}
				},
				{
					"type": "divider"
				},
				Message.get_team(dao=self.dao, team=savedTeam)
			]

			mObj.append(Message(blocks=blocksSender, channel=sender['id']))

		return mObj
