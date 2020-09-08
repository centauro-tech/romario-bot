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
		self.idx = None
		self.type = None
		self.trigger_id = None

	def execute(self):
		if self.trigger_id is not None:
			if self.type == 'tag':
				savedTeam = self.dao.get_saved_team(team_id=self.idx)
				mObj = Message(blocks=self.get_tag_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'link':
				savedTeam = self.dao.get_saved_team(team_id=self.idx)
				mObj = Message(blocks=self.get_link_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'text':
				savedTeam = self.dao.get_saved_team(team_id=self.idx)
				mObj = Message(blocks=self.get_text_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'email':
				savedTeam = self.dao.get_saved_team(team_id=self.idx)
				mObj = Message(blocks=self.get_email_modal(savedTeam), trigger_id=self.trigger_id)
			elif self.type == 'userteam':
				savedUser = self.dao.get_saved_user(user=self.idx)
				mObj = Message(blocks=self.get_userteam_modal(savedUser), trigger_id=self.trigger_id)
			elif self.type == 'usertag':
				savedUser = self.dao.get_saved_user(user=self.idx)
				mObj = Message(blocks=self.get_usertag_modal(savedUser), trigger_id=self.trigger_id)

		return mObj


	def get_tag_modal(self, savedTeam):
		tags = self.dao.list_tags(type_tag='tag-team')

		opt = []
		optSelected = []

		if len(tags) > 0:
			if 'tags' in savedTeam: 
				savedTags = savedTeam['tags']
			else:
				savedTags = []

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

		opt_element = {
			"type": "multi_static_select",
			"placeholder": {
				"type": "plain_text",
				"text": "Select an item",
				"emoji": True
			},
			"options": opt
		}

		if len(optSelected) > 0:
			opt_element["initial_options"] = optSelected

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
					"element": opt_element,
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


	def get_usertag_modal(self, savedUser):
		tags = self.dao.list_tags(type_tag='tag-user')

		opt = []
		optSelected = []

		if len(tags) > 0:
			if 'tags' in savedUser: 
				savedTags = savedUser['tags']
			else:
				savedTags = []

			for t in tags:
				option = {
					"text": {
						"type": "plain_text",
						"text": t['name']
					},
					"value": "user_tag_" + t['id'] + '#'
				}
				opt.append(option)
				if t['id'] in savedTags:
					optSelected.append(option)

		opt_element = {
			"type": "multi_static_select",
			"placeholder": {
				"type": "plain_text",
				"text": "Select an item",
				"emoji": True
			},
			"options": opt
		}

		if len(optSelected) > 0:
			opt_element["initial_options"] = optSelected

		blocks = {
			"type": "modal",
			"callback_id": "add_tag_user_" + savedUser['id'] + "#",
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
					"element": opt_element,
					"label": {
						"type": "plain_text",
						"text": "Selecione as TAGs que quer associar a <@" + savedUser['slack'] + '>',
						"emoji": True
					}
				}
			]
		}

		return blocks


	def get_userteam_modal(self, savedUser):
		teams = self.dao.list_teams()
		opt = []
		optSelected = []

		if len(teams) > 0:
			if 'teams' in savedUser: 
				savedTeams = savedUser['teams']
			else:
				savedTeams = []

			for t in teams:
				option = {
					"text": {
						"type": "plain_text",
						"text": t['name']
					},
					"value": "user_select_team_" + t['id'] + '#'
				}
				opt.append(option)

				if t['id'] in savedTeams:
					optSelected.append(option)

		team_acessory = {
			"type": "multi_static_select",
			"placeholder": {
				"type": "plain_text",
				"text": "selecione..."
			},
			"options": opt
		}

		if len(optSelected) > 0:
			team_acessory["initial_options"] = optSelected

		blocks = {
			"type": "modal",
			"callback_id": "user_select_teams_" + savedUser['slack'] + "#",
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
					"element": team_acessory,
					"label": {
						"type": "plain_text",
						"text": "Selecione os times de <@" + savedUser['slack'] + '>',
						"emoji": True
					}
				}
			]
		}

		return blocks
