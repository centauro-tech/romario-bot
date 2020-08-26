# -*- coding: utf-8 -*-
import os
import configparser
import logging
import json
import hashlib

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key,Attr

from slack import WebClient
from slack.errors import SlackApiError



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


	def save_user(self, user, leader=None, teams=None, slack=None):
		savedUser = self.get_saved_user(user)

		if savedUser is None:
			savedUser = {
				'id': user,
				'type': 'user'
			}

		if leader is not None:
			savedUser['leader'] = leader

		if teams is not None:
			if isinstance(teams, str):
				teamsMap = self.get_hash_value(s=teams)

			elif isinstance(teams, list):
				teamsMap = []
				for team in teams:
					teamsMap.append(self.get_hash_value(s=team))

			savedUser['teams'] = teamsMap

		if slack is not None:
			savedUser['slack'] = slack

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')
		response = table.put_item(
		   Item=savedUser
		)

		return self.get_saved_user(user=user)

	def list_users(self, user=None, leader=None, teams=None):

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		key = Key('type').eq('user')

		if user is not None:
			key = key & Key('id').eq(user)

		if leader is not None:
			key = key & Key('leader').eq(leader)

		if teams is not None:
			key = key & Attr('teams').contains(self.get_hash_value(s=teams))

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

	def list_teams(self, team_name=None, slack_channel=None):

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		key = Key('type').eq('team')

		if team_name is not None:
			key = key & Key('id').eq(self.get_hash_value(s=team_name))

		if slack_channel is not None:
			key = key & Key('slack_channel').eq(slack_channel)

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


	def save_team(self, team_name=None, team_channel=None, team_id=None):
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

		dynamodb = boto3.resource('dynamodb')
		table = dynamodb.Table('it_teams_structure')

		response = table.put_item(
		   Item=savedTeam
		)

		return self.get_saved_team(team_name=team_name, team_id=team_id)


	def get_hash_value(self, s):
		return str(int(hashlib.sha256(s.lower().encode('utf-8')).hexdigest(), 16) % 10**8)
