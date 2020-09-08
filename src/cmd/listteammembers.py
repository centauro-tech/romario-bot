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
		self.sender=None

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
				m = Message.get_user(dao=self.dao, savedUser=u)

				b.extend(
						[
							{
								"type": "divider"
							},
							m
						]
					)

			blocks =  [
					{
						"type": "header",
						"text": {
							"type": "plain_text",
							"text": ":soccer:   Escalação do time *"+savedTeam['name']+"*   :soccer:"
						}
					}
				]
			blocks.extend(b)
			blocks.extend([
				{
					"type": "divider"
				},
				{
					"type": "actions",
					"elements": [
						{
							"type": "button",
							"text": {
								"type": "plain_text",
								"text": ":chart_with_upwards_trend: Veja  a ficha técnica do time",
								"emoji": True
							},
							"value": "listteaminfo_" + savedTeam['id'] + "#"
						},
						{
							"type": "button",
							"text": {
								"type": "plain_text",
								"emoji": True,
								"text": ":gear: Configurar time"
							},
							"value": "config_team_" + savedTeam['id'] + "#"
						}
					]
				}
			])

		mObj = Message(blocks=blocks, channel=self.sender)
		return mObj