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
		user = self.dao.get_user(user=self.user)

		savedUser = None
		teamsLst = []
		if self.teams is not None:
			if isinstance(self.teams, str):
				if self.teams.isdigit() and len(self.teams) == 8:
					savedTeam = self.dao.get_saved_team(team_id=self.teams)
				else:
					savedTeam = self.dao.get_saved_team(team_name=self.teams)
				
				teamsLst.append(savedTeam)
				savedUser = self.dao.save_user(user=user['profile']['email'], teams=savedTeam['id'])

			elif isinstance(self.teams, list):
				savedUser = self.dao.save_user(user=user['profile']['email'], teams=self.teams)
				for team in self.teams:
					teamsLst.append(self.dao.get_saved_team(team_id=team))

		mObj = []
		for savedTeam in teamsLst:
			if savedTeam['slack_channel'] is not None:
				mObj.append(self.get_team_message(user=user, savedTeam=savedTeam, userLeader=savedUser['leader']))
				mObj.extend(self.get_user_message(user=user, savedTeam=savedTeam))
				
		return mObj	

	def get_team_message(self, user, savedTeam, userLeader):
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
			Message.get_user(user=user, leader=userLeader)
		]

		return Message(blocks=blocks, channel=savedTeam['slack_channel'])

	def get_user_message(self, user, savedTeam):
		message = None
		sender = None
		mObj = []

		if user['id'] == self.sender:
			message = '_Você se escalou para o time_ *' + savedTeam['name'] + '*.'
		
		else:
			sender = self.dao.get_user(self.sender)
			messageUser = '_@' + sender['name'] + ' te escalou para o time_ *' + savedTeam['name'] + '*.'
			messageSender = '_ Você escalou @' + user['name'] + ' para o time_ *' + savedTeam['name'] + '*.'

		channel = None
		if 'slack_channel' in savedTeam:
			channel = self.dao.get_channel(channel_id=savedTeam['slack_channel'])

		tList = None
		if 'tags' in savedTeam:
			tList = []

			if isinstance(savedTeam['tags'], str):
				t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=savedTeam['tags'])
				tList.append(t.get('name'))

			elif isinstance(savedTeam['tags'], list):
				for tag in savedTeam['tags']:
					t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=tag)
					tList.append(t.get('name'))

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
			Message.get_team(team=savedTeam, tags=tList, channel=channel)
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
				Message.get_team(team=savedTeam, tags=tList, channel=channel)
			]

			mObj.append(Message(blocks=blocksSender, channel=sender['id']))

		return mObj
