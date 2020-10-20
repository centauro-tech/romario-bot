# -*- coding: utf-8 -*-
import os
import json

from message import Message
from parser.slack import Slack
from cmd.user import User

class Escalate_users:

	def __init__(self, dao, event):
		self.event = event
		self.dao = dao

	def execute(self):
		listUsers = self.dao.list_sl_users()

		for user in listUsers:
			#print (user)
			if 'profile' in user and \
				'email' in user['profile'] and \
				user['deleted'] is False and \
				user['is_bot'] is False and \
				user['is_restricted'] is False and \
				user['is_ultra_restricted'] is False and \
				('is_invited_user' not in user or \
				user['is_invited_user'] is False):
				
				u = self.dao.get_saved_user(user=user['profile']['email'])
				if u is None:
					print('Tentando escalar ' + user['profile']['email'] + '...')

					slack = Slack(event='')
					setattr(slack, 'channel', user['id'])
					#slack.send_message(message=Message(message='Olá atleta...meu olheiro me informou que você seria uma bela escalação para nosso time. Pode me responder a pergunta abaixo :point_down: :smirk:'))

					userObj = User(dao=self.dao, message=None)
					setattr(userObj, 'sender', user['id'])
					mObj = userObj.execute()
					#slack.send_message(message=mObj)

					#print (user)