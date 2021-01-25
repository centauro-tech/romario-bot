# -*- coding: utf-8 -*-

import sys
import traceback

class Leadtime:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.average = None
		self.tags = None
		self.full = None
		self.from_date = None
		self.to_date = None

	def execute(self):
		self.print_issue(repo='tech-products', issue_number=22)


	def print_issue(self, repo, issue_number):
		issue = self.dao.get_issues(repo=repo, issue_number=issue_number)

		if isinstance(issue, list):
			for iss in issue:
				print('\n\n' + str(iss))

		else:
			print('\n\n' + str(issue))

			print('\ncomments:')
			print('------------------')
			for comment in issue.get_comments():
				print(comment.body)
				print('------------------')

			for timeline in issue.get_timeline():
				if timeline.source is not None:
					print('Issue number: ' + str(timeline.source.issue.number))
					print('Issue repository: ' + str(timeline.source.issue.repository.name))
					self.print_issue(repo=timeline.source.issue.repository.name, issue_number=timeline.source.issue.number)