# -*- coding: utf-8 -*-
import configparser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listteammembers:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None

	def execute(self):
		self.team=self.team.replace('*','').replace('~','').replace('_','')

		savedTeam = self.dao.get_saved_team(team_name=self.team)
		if savedTeam is None:
			return 'Não existe o time ' + self.team + '  :-('

		else:
			savedUsers = self.dao.list_users(teams=self.team)

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
					"type": "divider"
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "Escalação do time *"+self.team+"*"
					}
				}]
			blocks.extend(b)

			blocks.append(
				{
					"type": "divider"
				}
			)

			return blocks