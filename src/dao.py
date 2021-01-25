# -*- coding: utf-8 -*-
import os
import configparser
import logging
import json
import hashlib
import statistics

from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key,Attr

from slack import WebClient
from slack.errors import SlackApiError

from github import Github


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = WebClient(token=os.environ['sl_token'], ssl=False)

class Dao:

	def get_user(self, user=None):
		if user is not None:
			response = client.users_info(
			  user=user
			)

			if response['ok'] is True:
				ret = response['user']
				return ret

	def list_sl_users(self):
		response = client.users_list()

		if response['ok'] is True:
			ret = response['members']
			return ret

	def get_channel(self, channel_id=None):
		if channel_id is not None:
			response = client.conversations_info(
			  channel=channel_id
			)

			if response['ok'] is True:
				ret = response['channel']
				return ret

	def get_saved_user(self, user=None):
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')
		response = table.get_item(Key={'id': user, 'type': 'user'})
		if 'Item' in response:
			return response['Item']


	def save_user(self, user, leader=None, teams=None, slack=None, teams_id=None, tags=None):
		savedUser = self.get_saved_user(user)

		if savedUser is None:
			savedUser = {
				'id': user,
				'type': 'user'
			}

		if leader is not None:
			savedUser['leader'] = leader

		if teams is not None:
			savedUser['teams'] = teams

		if tags is not None:
			savedUser['tags'] = tags

		if slack is not None:
			savedUser['slack'] = slack

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')
		response = table.put_item(
		   Item=savedUser
		)

		return self.get_saved_user(user=user)

	def list_users(self, user=None, leader=None, teams=None, team_id=None):
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		key = Key('type').eq('user')

		if user is not None:
			key = key & Key('id').eq(user)

		if leader is not None:
			key = key & Key('leader').eq(leader)

		if teams is not None:
			key = key & Attr('teams').contains(self.get_hash_value(s=teams))

		if team_id is not None:
			key = key & Attr('teams').contains(team_id)

		ret = []

		scan_kwargs = {
			'FilterExpression': key
		}

		done = False
		start_key = None
		while not done:
			if start_key:
				scan_kwargs['ExclusiveStartKey'] = start_key
			response = table.scan(**scan_kwargs)
			ret.extend(response.get('Items', []))
			start_key = response.get('LastEvaluatedKey', None)
			done = start_key is None

		return ret

	def get_saved_team(self, team_name=None, team_id=None):

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		if team_id is not None:
			response = table.get_item(Key={'id': team_id, 'type': 'team'})
		elif team_name is not None:
			response = table.get_item(Key={'id': self.get_hash_value(s=team_name), 'type': 'team'})

		if 'Item' in response:
			return response['Item']
		else:
			return None

	def list_teams(self, team_name=None, slack_channel=None, tags=None):

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		key = Key('type').eq('team')

		if team_name is not None:
			key = key & Key('id').eq(self.get_hash_value(s=team_name))

		if slack_channel is not None:
			key = key & Key('slack_channel').eq(slack_channel)

		if tags is not None:
			if isinstance(tags, str):
				key = key & Attr('tags').contains(tags)
			elif isinstance(tags, list):
				for t in tags:
					key = key & Attr('tags').contains(t)
			
		ret = []

		scan_kwargs = {
			'FilterExpression': key
		}

		done = False
		start_key = None
		while not done:
			if start_key:
				scan_kwargs['ExclusiveStartKey'] = start_key
			response = table.scan(**scan_kwargs)
			ret.extend(response.get('Items', []))
			start_key = response.get('LastEvaluatedKey', None)
			done = start_key is None

		return ret


	def save_team(self, team_name=None, team_channel=None, team_id=None, tags=None, tech_info=None, tech_info_lst=None):
		savedTeam = self.get_saved_team(team_name=team_name, team_id=team_id)

		if savedTeam is None:
			savedTeam = {
				'type': 'team'
			}

		if team_name is not None:
			savedTeam['name'] = team_name

		if team_id is not None:
			savedTeam['id'] = team_id
		else:
			savedTeam['id'] = self.get_hash_value(s=team_name)

		if team_channel is not None:
			savedTeam['slack_channel'] = team_channel

		if tags is not None:
			savedTeam['tags'] = tags

		if tech_info is not None:
			if 'tech_info' not in savedTeam:
				savedTeam['tech_info'] = []
			tech_info['id'] = self.get_hash_value(s=(tech_info['desc']+tech_info['value']))
			savedTeam.get('tech_info').append(tech_info)

		if tech_info_lst is not None:
			savedTeam['tech_info'] = tech_info_lst
      
		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		response = table.put_item(
		   Item=savedTeam
		)

		return self.get_saved_team(team_name=team_name, team_id=team_id)


	def save_tag(self, type_tag, tag_value):

		tag_id = self.get_hash_value(s=tag_value)
		
		tag = {
			'id': tag_id,
			'type': type_tag,
			'name': tag_value
		}

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')
		response = table.put_item(
		   Item=tag
		)

		return response


	def list_tags(self, type_tag):

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		key = Key('type').eq(type_tag)

		ret = []

		scan_kwargs = {
			'FilterExpression': key
		}

		done = False
		start_key = None
		while not done:
			if start_key:
				scan_kwargs['ExclusiveStartKey'] = start_key
			response = table.scan(**scan_kwargs)
			ret.extend(response.get('Items', []))
			start_key = response.get('LastEvaluatedKey', None)
			done = start_key is None

		return ret


	def get_saved_tag(self, type_tag, tag_id=None, tag_name=None):

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		if tag_id is not None:
			response = table.get_item(Key={'id': tag_id, 'type': type_tag})

		if tag_name is not None:
			response = table.get_item(Key={'id': self.get_hash_value(tag_name), 'type': type_tag})			

		if 'Item' in response:
			return response['Item']
		else:
			return None


	# Retorna dados das issues fechadas
	def get_issues(self, repo, issue_number=None, state='open', labels=[], from_date=None, sort='created', direction='asc'):
		g = Github(os.environ['gh_access_token'])
		repo = g.get_repo(os.environ['gh_organization'] + "/" + repo)

		if issue_number is not None:
			ret = repo.get_issue(number=issue_number)
		else:
			ret = repo.get_issues(state=state, labels=labels, since=from_date, sort=sort, direction=direction)

		return ret

	# Retorna dados das issues fechadas
	def get_leadtime(self, repo, from_date=None, labels=None, average=15):
		average = int(average)

		if labels is not None:
			labels = labels.split(',')

		to_date = datetime.now().replace(hour=23, minute=59, second=59)
		
		if from_date is None:
			from_date = to_date - timedelta(days=(average-1))
		else:
			from_date = datetime.strptime(from_date, "%Y-%m-%d")

		# Cria objetos que vão ser retornados
		throughput = {}
		thrAvgHelper = {}
		ltAvgHelper = {}
		leadtime = {}
		ret = {'self.repo.ghrepo': repo ,'tagsTitles': labels, 'throughput' : throughput, 'leadtime': leadtime}
		from_dateAvg = from_date - timedelta(days=(average-1))

		# Preenche com as chaves iniciais
		d = from_dateAvg
		while d <= to_date:
			tagsRet = [0] * len(labels)
			thrAvgHelper[d.strftime("%Y-%m-%d")] = [0, tagsRet]
			ltAvgHelper[d.strftime("%Y-%m-%d")] = []
			if d >= from_date:
				tagsRet = [0] * len(labels)
				throughput[d.strftime("%Y-%m-%d")] = [None,0,tagsRet]
				leadtime[d.strftime("%Y-%m-%d")] = [None]
			d += timedelta(days=1)

		issues = self.get_issues(repo=repo, state='closed', from_date=from_dateAvg)

		for issue in issues:
			eligible = False
			for lbl in issue.labels:
				if lbl.name in labels:
					eligible = True

			if eligible:
				dateCreated = issue.created_at
				dateClosed = issue.closed_at
				dateClosedFormated = dateClosed.strftime("%Y-%m-%d")

				delta = dateClosed - dateCreated
				if dateClosed <= to_date and dateClosed >= from_dateAvg:
					#LEADTIME-AVG
					ltAvgHelper[dateClosedFormated].append(delta.days)

					#THROUGHPUT-AVG
					days = thrAvgHelper[dateClosedFormated][0]
					days = days + 1
					thrAvgHelper[dateClosedFormated][0] = days
					for idTag, tag in enumerate(labels):
						for label in issue.labels:
							if (label.name==tag):
								days = thrAvgHelper[dateClosedFormated][1][idTag]
								days = days + 1
								thrAvgHelper[dateClosedFormated][1][idTag] = days

				if issue.closed_at <= to_date and issue.closed_at >= from_date:
					#LEADTIME
					leadtime[dateClosedFormated].append([issue.number, delta.days])

					#THROUGHPUT
					days = throughput[dateClosedFormated][1]
					days = days + 1
					throughput[dateClosedFormated][1] = days

		# Calcula as médias
		keysSorted = sorted(thrAvgHelper.keys())

		# Média de throughput
		avg = []
		for x in range(0, len(keysSorted)):
			avg.append(thrAvgHelper[keysSorted[x]][0])
			if x >= (average-1):
				throughput[keysSorted[x]][0] = [statistics.mean(avg), statistics.pstdev(avg)]
				del avg[0]

		for z in range(0, len(labels)):
			avg = []
			for x in range(0, len(keysSorted)):
				avg.append(thrAvgHelper[keysSorted[x]][1][z])
				if x >= (average-1):
					throughput[keysSorted[x]][2][z] = statistics.mean(avg)
					del avg[0]

		keysSorted = sorted(ltAvgHelper.keys())

		# Media de Leadtime
		avg = []
		for x in range(0, len(keysSorted)):
			avg.append(ltAvgHelper[keysSorted[x]])
			if x >= (average - 1):
				avgHlp = []
				for y in range(0, average):
					avgHlp += avg[y]
				
				if len(avgHlp) > 0:
					leadtime[keysSorted[x]][0] = [statistics.mean(avgHlp), statistics.pstdev(avgHlp)]
				else:
					leadtime[keysSorted[x]][0] = [None, None]
				
				del avg[0]

		return ret

	def get_gh_repos(self):
		g = Github(os.environ['gh_access_token'])
		repos = g.search_repositories(query='org:' + os.environ['gh_organization'] + ' chapt OR team in:name')

		ret=[]
		for repo in repos:
			ret.append(repo.name)

		return ret

	# Retorna as labels das issues do Repositorio selecionado
	def get_gh_team_labels(self, repo=None):
		g = Github(os.environ['gh_access_token'])
		repo = g.get_repo(os.environ['gh_organization'] + "/" + repo)
		labels = repo.get_labels()

		ret = []
		for label in labels:
			ret.append(label.name)

		return ret

	# Retorna dados das issues abertas
	def get_gh_cfd(self, repo, from_date=None, labels=[], average=None):
		average=int(average)
		to_date = datetime.now().replace(hour=23, minute=59, second=59)
		labels = labels.split(',')

		if from_date is None:
			from_date = datetime.now().replace(hour=00, minute=00, second=00) - timedelta(days=average)
		else:
			from_date = datetime.strptime(from_date, "%Y-%m-%d")

		issuesRet = []

		issues = self.get_issues(repo=repo, state='closed', from_date=from_date)
		issuesRet.extend(self.run_gh_cfd(labels, issues))
		
		issues = self.get_issues(repo=repo, state='open', from_date=from_date)
		issuesRet.extend(self.run_gh_cfd(labels, issues))

		return {'dateFrom': from_date.strftime('%Y-%m-%d'), \
		  'dateTo': to_date.strftime('%Y-%m-%d'), \
		  'cfd': issuesRet}

	def run_gh_cfd(self, labels, issues):
		ret = []

		for issue in issues:			
			eligible = False
			for lbl in issue.labels:
				if lbl.name in labels:
					eligible = True

			if eligible:
				issueArr = {'issue': issue.number, \
							'created_at': issue.created_at.strftime('%Y-%m-%d')}

				if issue.closed_at is not None:
					issueArr['closed_at']=(issue.closed_at.strftime('%Y-%m-%d'))

				if issue.assignee is not None:
					for event in issue.get_events():
						if event.event == 'assigned':
							issueArr['assigned_at'] = event.created_at.strftime('%Y-%m-%d')
							break

				ret.append(issueArr)

		return ret

	def get_hash_value(self, s):
		return str(int(hashlib.sha256(s.strip().lower().encode('utf-8')).hexdigest(), 16) % 10**8)
