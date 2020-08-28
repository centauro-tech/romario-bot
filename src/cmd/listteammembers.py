# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listteammembers:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.team_id = None

	def execute(self):

		savedTeam=None
		savedUsers=None

		if  self.team is not None:
			self.team=self.team.replace('*','').replace('~','').replace('_','')
			savedTeam = self.dao.get_saved_team(team_name=self.team)
			savedUsers = self.dao.list_users(teams=self.team)
		
		elif self.team_id is not None:
			savedTeam = self.dao.get_saved_team(team_id=self.team_id)
			savedUsers = self.dao.list_users(team_id=self.team_id)

		if savedTeam is None:
			return 'Não existe o time ' + self.team + '  :-('
			
		else:
			b = []
			for u in savedUsers:
				user = self.dao.get_user(u['slack'])
				txt = '*'+ user['profile']['real_name'] + '* (@' + user['name'] + ')\n'
				txt += '' + user['profile']['title'] + '\n'
				txt += '' + u['id']

				b.extend([{
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": txt
					},
					"accessory": {
						"type": "image",
						"image_url": user['profile']['image_512'],
						"alt_text": "profiel picture"
					}
				}])

			blocks =  [
					{
						"type": "header",
						"text": {
							"type": "plain_text",
							"text": "Escalação do time *"+savedTeam['name']+"*"
						}
					}
				]
			blocks.extend(b)

		mObj = Message(blocks=blocks)
		return mObj