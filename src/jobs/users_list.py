# -*- coding: utf-8 -*-
import os
import json

class Users_list:

	def __init__(self, dao, event):
		self.event = event
		self.dao = dao

	def execute(self):
		savedUsers = self.dao.list_users()

		file = []

		user2BePrinted = []
		user2BePrinted.append('name')
		user2BePrinted.append('email')
		user2BePrinted.append('leader_name')
		user2BePrinted.append('leader_email')
		user2BePrinted.append('tags')
		user2BePrinted.append('teams')

		file.append(('\t'.join(user2BePrinted)))

		for savedUser in savedUsers:
			user = self.dao.get_user(user=savedUser['slack'])

			if 'leader' in savedUser:
				leader = self.dao.get_user(user=savedUser['leader'])
			else:
				leader = None

			savedTeams=[]
			if 'teams' in savedUser:
				if isinstance(savedUser['teams'], str):
					t = self.dao.get_saved_team(team_id=savedUser['teams'])
					savedTeams.append(t['name'])
				elif isinstance(savedUser['teams'], list):
					for team in savedUser['teams']:
						t = self.dao.get_saved_team(team_id=team)
						savedTeams.append(t['name'])
						
				#print('savedTeams: ' + str(savedTeams))

			tags=[]
			if 'tags' in savedUser:
				if isinstance(savedUser['tags'], str):
					t = self.dao.get_saved_tag(tag_id=savedUser['tags'], type_tag='tag-user')
					tags.append(t['name'])
				elif isinstance(savedUser['tags'], list):
					for tag in savedUser['tags']:
						t = self.dao.get_saved_tag(tag_id=tag, type_tag='tag-user')
						tags.append(t['name'])
				
				#print('tags: ' + str(tags))

			user2BePrinted = []
			user2BePrinted.append(user['profile']['real_name'])
			user2BePrinted.append(user['profile']['email'])

			if leader is not None:
				user2BePrinted.append(leader['profile']['real_name'])
				user2BePrinted.append(leader['profile']['email'])
			else:
				user2BePrinted.append('')
				user2BePrinted.append('')

			user2BePrinted.append((', '.join(tags)))
			user2BePrinted.append((', '.join(savedTeams)))

			file.append(('\t'.join(user2BePrinted)))

		
		print(('\n'.join(file)))