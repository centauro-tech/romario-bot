# -*- coding: utf-8 -*-

import sys
import traceback
from message import Message

class Issue:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.issue_number = None

	def execute(self):
		issue = self.dao.get_issues(repo=self.team, issue_number=int(self.issue_number))

		if issue.labels is not None and len(issue.labels) > 0:
			tags_txt = "\n*Labels:* "
			for label in issue.labels:
				 tags_txt += label.name + ', '


		blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": issue.title
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": issue.body
				}
			}
		]

		if tags_txt is not None:
			blocks.append(
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": tags_txt
					}
				}
			)

		
		for timeline in issue.get_timeline():
			if timeline.source is not None:
				subissue = self.dao.get_issues(repo=timeline.source.issue.repository.name, issue_number=timeline.source.issue.number)
				blocks.extend([
					{
						"type": "divider"
					},
					Message.get_issue(dao=self.dao, issue=subissue)
				])

		return Message(blocks=blocks)