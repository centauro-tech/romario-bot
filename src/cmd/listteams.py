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
			savedTeams = self.dao.list_teams()
		else:
			tagsList = re.split(',| e ', self.tags)

			tList = []
			for tag in tagsList:
				t = self.dao.get_saved_tag(type_tag='tag-team', tag_name=tag)
				if t is not None:
					tList.append(t.get('id'))

			if len(tList) == 1:
				tList = tList[0]

			savedTeams = self.dao.list_teams(tags=tList)

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": ":soccer: Times classificados" + (("\ncom as tags " + self.tags) if self.tags is not None else '')
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

			blocks.extend([Message.get_team(team=team, tags=tList, channel=channel),{"type": "divider"}])

		blocks.append({
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": ":pushpin: Viu algo errado? Corrija através do comando *_configurar time <time>_*."
				}
			]
		})

		mObj = Message(blocks=blocks)
		return mObj