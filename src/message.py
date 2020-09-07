# -*- coding: utf-8 -*-
import logging
import dao

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Message:

	def __init__(self, message=None, channel=None, sender=None, blocks=None, trigger_id=None):
		self.message = message
		self.channel = channel
		self.sender = sender
		self.blocks = blocks
		self.trigger_id = trigger_id

	@staticmethod
	def get_user(dao, user=None, savedUser=None):
		if user is None and savedUser is not None:
			user = dao.get_user(user=savedUser['slack'])
		if user is not None and savedUser is None:
			savedUser = dao.get_saved_user(user=user['profile']['email'])

		tList=None
		if savedUser is not None and 'tags' in savedUser:
			tList = []
			if isinstance(savedUser['tags'], str):
				t = dao.get_saved_tag(type_tag='tag-user', tag_id=savedUser['tags'])
				tList.append(t.get('name'))

			elif isinstance(savedUser['tags'], list):
				for tag in savedUser['tags']:
					t = dao.get_saved_tag(type_tag='tag-user', tag_id=tag)
					tList.append(t.get('name'))

		teamList=None
		if savedUser is not None and 'teams' in savedUser:
			teamList = []
			if isinstance(savedUser['teams'], str):
				t = dao.get_saved_tag(type_tag='team', tag_id=savedUser['teams'])
				teamList.append(t.get('name'))

			elif isinstance(savedUser['teams'], list):
				for team in savedUser['teams']:
					t = dao.get_saved_tag(type_tag='team', tag_id=team)
					teamList.append(t.get('name'))


		txt = '*'+ user['profile']['real_name'] + '* - <@' + user['id'] + '>\n'

		if savedUser is not None and 'leader' in savedUser:
			txt += '*Líder:* <@' + savedUser['leader'] + '>'

		if tList is not None and len(tList) > 0:
			txt += "\n*Times:* " + (', '.join(teamList))

		if tList is not None and len(tList) > 0:
			txt += "\n*Tags:* " + (', '.join(tList))

		ret = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": txt
			},
			"accessory": {
				"type": "image",
				"image_url": user['profile']['image_512'],
				"alt_text": "profile picture"
			}
		}

		return ret


	@staticmethod
	def get_team(dao, team):

		slack_channel=''
		if 'slack_channel' in team:
			slack_channel='\n*Campo de jogo:* :soccer-field: <#' + team['slack_channel'] + '>'

		tList=None
		if 'tags' in team:
			tList = []
			if isinstance(team['tags'], str):
				t = dao.get_saved_tag(type_tag='tag-team', tag_id=team['tags'])
				tList.append(t.get('name'))

			elif isinstance(team['tags'], list):
				for tag in team['tags']:
					t = dao.get_saved_tag(type_tag='tag-team', tag_id=tag)
					tList.append(t.get('name'))

		if tList is not None and len(tList) > 0:
			tags_txt = "\n*Tags:* " + (', '.join(tList))
		else:
			tags_txt=''

		ret = {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Nome do time:* " + team['name'] + slack_channel + tags_txt
				},
				"accessory": {
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Escalação"
					},
					"value": "listteammembers_" + team['id'] + "#"
				}
			}

		return ret