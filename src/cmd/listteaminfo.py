# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listteaminfo:

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
		
		elif self.team_id is not None:
			savedTeam = self.dao.get_saved_team(team_id=self.team_id)

		if savedTeam is None:
			return 'Não existe o time ' + self.team + '  :-('
			
		else:

			blocks =  [
				{
					"type": "header",
					"text": {
						"type": "plain_text",
						"text": ":chart_with_upwards_trend:   Ficha Técnica do time " + savedTeam['name'] + "  :chart_with_downwards_trend:"
					}
				},
				{
					"type": "divider"
				}
			]

			if 'slack_channel' in savedTeam:
				blocks.extend([{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": "*:soccer-field: Campo de jogo:*   <#" + savedTeam['slack_channel'] + ">"
						}
					},
					{
						"type": "divider"
					}]
				)

			blocks.extend(self.get_tags(tags=savedTeam['tags'], savedTeam=savedTeam))
			blocks.append({"type": "divider"})

			if 'tech_info' in savedTeam:
				tech_info_lst = savedTeam['tech_info']
				tech_info_lst.reverse()

				for tech_info in tech_info_lst:
					if tech_info['type'] == 'team-text':
						blocks.extend(self.get_text(tech_info=tech_info, savedTeam=savedTeam))
					elif tech_info['type'] == 'team-link':
						blocks.extend(self.get_link(tech_info=tech_info, savedTeam=savedTeam))
					elif tech_info['type'] == 'team-email':
						blocks.extend(self.get_email(tech_info=tech_info, savedTeam=savedTeam))

            
					blocks.append({"type": "divider"})

			blocks.append({
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": ":soccer: Veja a escalação do time",
							"emoji": True
						},
						"value": "listteammembers_" + savedTeam['id'] + "#"
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
			})

		mObj = Message(blocks=blocks, channel=self.sender)
		return mObj

	def get_text(self, tech_info, savedTeam):
		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": ":newspaper:   *"+tech_info['desc']+"*"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": tech_info['value'],
					"verbatim": False
				},
				"accessory": self.get_delete_button(tech_info['id'], savedTeam)
			}
		]
		return blocks


	def get_email(self, tech_info, savedTeam):
		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": ":email:   *"+tech_info['desc']+"*: \n"+tech_info['value']
				},
				"accessory": self.get_delete_button(tech_info['id'], savedTeam)
			}
		]
		return blocks
	

	def get_link(self, tech_info, savedTeam):
		blocks = [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": ":link:   *<"+tech_info['value']+"|"+tech_info['desc']+">*"
				},
				"accessory": self.get_delete_button(tech_info['id'], savedTeam)
			}
		]
		return blocks
	

	def get_tags(self, tags, savedTeam):
		blocks = []
		if tags is not None:
			tList = []

			if isinstance(tags, str):
				t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=tags)
				tList.append({"type": "mrkdwn","text": t['name']})

			elif isinstance(tags, list):
				for tag in tags:
					t = self.dao.get_saved_tag(type_tag='tag-team', tag_id=tag)
					tList.append({"type": "mrkdwn","text": t['name']})

			blocks = [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": ":label:   *Tags associadas*"
					}
				},
				{
					"type": "section",
					"fields": tList,
					"accessory": {
						"type": "button",
						"text": {
							"type": "plain_text",
							"emoji": True,
							"text": ":label:"
						},
						"value": "add_tech_info_tag_" + savedTeam['id'] + "#"
					}
				}
			]
		return blocks


	def get_delete_button(self, id, savedTeam):
		ret = {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": ":put_litter_in_its_place:",
				"emoji": True
			},
			"value": "del_tech_info_" + savedTeam['id'] + "_" + str(id) + "#",
			"confirm": {
				"title": {
					"type": "plain_text",
					"text": "Remover item da ficha."
				},
				"text": {
					"type": "mrkdwn",
					"text": "Tem certeza que deseja fazer isso?"
				},
				"confirm": {
					"type": "plain_text",
					"text": "Remover"
				},
				"deny": {
					"type": "plain_text",
					"text": "Cancelar"
				}
			}
		}
		return ret

	