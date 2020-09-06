# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Techinfo:

	def __init__(self, dao, message):
		self.dao = dao	
		self.text = message
		self.team = None
		self.type = None
		self.trigger_id = None

	def execute(self):
		savedTeam = self.dao.get_saved_team(team_id=self.team)

		if self.trigger_id is not None:
			if self.type == 'tag':
				mObj = Message(blocks=self.get_tag_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'link':
				mObj = Message(blocks=self.get_link_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'text':
				mObj = Message(blocks=self.get_text_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'email':
				mObj = Message(blocks=self.get_email_modal(savedTeam), trigger_id=self.trigger_id)

		return mObj


	def get_tag_modal(self, savedTeam):
		tags = self.dao.list_tags(type_tag='tag-team')

		opt = []
		optSelected = []
		if len(tags) > 0:
			savedTags = savedTeam['tags']
			for t in tags:
				option = {
					"text": {
						"type": "plain_text",
						"text": t['name']
					},
					"value": "team_tag_" + t['id'] + '#'
				}
				opt.append(option)
				if t['id'] in savedTags:
					optSelected.append(option)

		blocks = {
			"type": "modal",
			"callback_id": "add_tag_team_" + savedTeam['id'] + "#",
			"submit": {
				"type": "plain_text",
				"text": "OK",
				"emoji": True
			},
			"close": {
				"type": "plain_text",
				"text": "Cancelar",
				"emoji": True
			},
			"title": {
				"type": "plain_text",
				"text": "Ficha Técnica",
				"emoji": True
			},
			"blocks": [
				{
					"type": "input",
					"element": {
						"type": "multi_static_select",
						"placeholder": {
							"type": "plain_text",
							"text": "Select an item",
							"emoji": True
						},
						"options": opt,
						"initial_options": optSelected
					},
					"label": {
						"type": "plain_text",
						"text": "Selecione as TAGs que quer associar ao time " + savedTeam['name'],
						"emoji": True
					}
				}
			]
		}

		return blocks


	def get_link_modal(self, savedTeam):
		blocks = {
			"type": "modal",
			"callback_id": "add_link_team_" + savedTeam['id'] + "#",
			"submit": {
				"type": "plain_text",
				"text": "OK",
				"emoji": True
			},
			"close": {
				"type": "plain_text",
				"text": "Cancelar",
				"emoji": True
			},
			"title": {
				"type": "plain_text",
				"text": "Ficha Técnica",
				"emoji": True
			},
			"blocks": [
				{
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": "Identificação do link",
						"emoji": True
					},
					"element": {
						"type": "plain_text_input",
						"placeholder": {
							"type": "plain_text",
							"text": "Ex: Board do time"
						},
						"action_id": "team_link_desc",
					}
				},
				{
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": "URL",
						"emoji": True
					},
					"element": {
						"type": "plain_text_input",
						"placeholder": {
							"type": "plain_text",
							"text": "Ex: http://www.trello.com"
						},
						"multiline": True,
						"action_id": "team_link_url",
					}
				}
			]
		}

		return blocks

	def get_text_modal(self, savedTeam):
		blocks = {
			"type": "modal",
			"callback_id": "add_text_team_" + savedTeam['id'] + "#",
			"submit": {
				"type": "plain_text",
				"text": "OK",
				"emoji": True
			},
			"close": {
				"type": "plain_text",
				"text": "Cancelar",
				"emoji": True
			},
			"title": {
				"type": "plain_text",
				"text": "Ficha Técnica",
				"emoji": True
			},
			"blocks": [
				{
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": "Título",
						"emoji": True
					},
					"element": {
						"type": "plain_text_input",
						"placeholder": {
							"type": "plain_text",
							"text": "Ex: Missão do time"
						},
						"action_id": "team_text_title",
					}
				},
				{
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": "Texto",
						"emoji": True
					},
					"element": {
						"type": "plain_text_input",
						"placeholder": {
							"type": "plain_text",
							"text": "Ex: Revolucionar o esporte no Brasil"
						},
						"multiline": True,
						"action_id": "team_text_body",
					}
				}
			]
		}


		return blocks

	def get_email_modal(self, savedTeam):
		blocks = {
			"type": "modal",
			"callback_id": "add_email_team_" + savedTeam['id'] + "#",
			"submit": {
				"type": "plain_text",
				"text": "OK",
				"emoji": True
			},
			"close": {
				"type": "plain_text",
				"text": "Cancelar",
				"emoji": True
			},
			"title": {
				"type": "plain_text",
				"text": "Ficha Técnica",
				"emoji": True
			},
			"blocks": [
				{
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": "Identificação",
						"emoji": True
					},
					"element": {
						"type": "plain_text_input",
						"placeholder": {
							"type": "plain_text",
							"text": "lista de distribuição XYZ"
						},
						"action_id": "team_email_id",
					}
				},
				{
					"type": "input",
					"label": {
						"type": "plain_text",
						"text": "Email",
						"emoji": True
					},
					"element": {
						"type": "plain_text_input",
						"placeholder": {
							"type": "plain_text",
							"text": "lista-do-time-xyz@centauro.com.br"
						},
						"action_id": "team_email_email",
					}
				}
			]
		}


		return blocks