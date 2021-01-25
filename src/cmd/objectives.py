# -*- coding: utf-8 -*-

import sys
import traceback
from message import Message

class Objectives:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None

	def execute(self):
		if self.team is None:
			self.team = 'tech-products'
		objs = self.dao.get_issues(repo=self.team, state='open', labels=['objective'])

		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "OBJETIVOS"
				}
			}
		]
		for objective in objs:
			blocks.extend([
				{
					"type": "divider"
				},
				Message.get_issue(dao=self.dao, issue=objective)
			])

		return Message(blocks=blocks)