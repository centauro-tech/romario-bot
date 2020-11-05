# -*- coding: utf-8 -*-
import configparser
import logging
import re

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listteams:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.tags = None

	def execute(self):
		if self.tags is None:
			return self.get_tags_filter()
		else:
			if isinstance(self.tags, str):
				tagsList = re.split(',| e ', self.tags)
			else:
				tagsList = self.tags

			tList = []
			tNamesList = []
			for tag in tagsList:
				if tag.isdigit() and len(tag) == 8:
					t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=tag)
				else:
					t = self.dao.get_saved_tag(type_tag='tag-team', tag_name=tag)
				
				if t is not None:
					tList.append(t.get('id'))
					tNamesList.append(t.get('name'))

			if len(tList) == 1:
				tList = tList[0]

			savedTeams = self.dao.list_teams(tags=tList)

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": ":soccer: Times classificados (" + str(len(savedTeams)) + " times) \nTags: " + (', '.join(tNamesList)) + ''
				}
			},
			{
				"type": "divider"
			}
		]

		for team in savedTeams:
			channel = None
			if 'slack_channel' in team:
				channel = self.dao.get_channel(channel_id=team['slack_channel'])

			if 'tags' in team:
				tList = []

				if isinstance(team['tags'], str):
					t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=team['tags'])
					tList.append(t.get('name'))

				elif isinstance(team['tags'], list):
					for tag in team['tags']:
						t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=tag)
						tList.append(t.get('name'))

			blocks.extend([Message.get_team(dao=self.dao, team=team),{"type": "divider"}])

		blocks.append({
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": ":pushpin: Viu algo errado? Corrija através do comando *_configurar time Nome do Time_*."
				}
			]
		})

		mObj = Message(blocks=blocks)
		return mObj

	def get_tags_filter(self):
		tags = self.dao.list_tags(type_tag='tag-team')

		optTags = []
		for t in tags:
			optTags.append({
						"text": {
							"type": "plain_text",
							"text": t['name'],
							"emoji": True
						},
						"value": 'list_teams_tag_' + t['id'] + '#'
					}
				)

		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Selecione uma ou mais tags para filtrar a pesquisa"
				},
				"accessory": {
					"type": "multi_static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "selecione...",
						"emoji": True
					},
					"options": optTags,
					"action_id": "list_teams_tags"
				}
			}
		]

		mObj = Message(blocks=blocks)
		return mObj