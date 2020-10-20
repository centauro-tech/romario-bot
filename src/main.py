# -*- coding: utf-8 -*-

import configparser
import re
import sys
import importlib
import dao
import requests
import json
import logging
import os
import sys
from urllib.parse import parse_qs


from parser.slack import Slack
from message import Message

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
	logger.info('event: ' + json.dumps(event))

	# Get from POST or GET requests
	if 'body' in event and \
	   event['body'] is not None:
		try:
			event = json.loads(event['body'])
		except ValueError: 
			event = json.loads(parse_qs(event['body'])['payload'][0])

		logger.info('decoded event: ' + json.dumps(event))


	elif 'queryStringParameters' in event and \
	   event['queryStringParameters'] is not None:
		event = event['queryStringParameters']
		logger.info('event: ' + str(event))

	# Discard bot responses
	if 'event' in event and \
	   event['event'] is not None and \
	   'bot_id' in event['event']:
	   return

	# Execute cron jobs
	if 'source' in event and \
	   event['source'] == 'cron' and \
	   'action' in event:
		class_ = getattr(importlib.import_module("jobs." + event['action']), event['action'].capitalize())
		job = class_(dao.Dao(), event)
		job.execute()

		ret = get_return(True, 'job ' + event['action'] + ' executed')
	
	# Execute html requests
	elif 'source' in event and \
	   event.pop('source') == 'html' and \
	   'action' in event:

		functionAttr = getattr(dao.Dao(), event.pop('action'))
		jsonr = functionAttr(**event)

		ret = get_return(True, jsonr)

	# Execute BOT commands
	else:
		# Get the right parser
		parser = find_parser(event)

		if parser is not None:
			if hasattr(parser, 'validate'):
				ret = get_return(True, parser.validate)
				return ret

			if hasattr(parser, 'event'):
				command = find_command(parser.event)

				if command is not None:
					msg = command.execute()
				else:
					config = configparser.RawConfigParser()
					config.read('command.cfg')
					msg = Message(message=config.get('default-messages', 'command-not-found'))

				if msg is not None:
					if isinstance(msg, list):
						for message in msg:
							ret = parser.send_message(message)
					else:
						ret = parser.send_message(msg)

			else:
				ret = get_return(False, 'invalid command')

		else:
			ret = get_return(False, 'invalid parser')

	return get_return(True, 'Success')

def find_parser(event):
	parser = None

	if 'token' in event and \
	   event['token'] == os.environ['sl_token_src']:
		parser = Slack(event)

	return parser

# Identify if the message contains the command
def find_command(message):
	config = configparser.RawConfigParser()
	config.read('command.cfg')
	commands = config.items('commands')

	command = None
	for key, value in commands:
		ret = re.search(r"{}".format(key), message)

		if (ret is not None):
			class_ = getattr(importlib.import_module("cmd." + value), value.capitalize())
			command = class_(dao.Dao(), message)
			logger.info('command: ' + value)

			find_command_arguments(message, command, value)

			return command
	return None

def find_command_arguments(message, command, commandName):
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read('command.cfg')
	commands = config.items('command-' + commandName)

	arguments = None
	for key, value in commands:
		compiled = re.compile(r"{}".format(key), re.M|re.I)
		ret = compiled.search(message)
		argList = []

		while (ret is not None):
			argList.append(ret.group('value'))
			ret = compiled.search(message, ret.span()[1])

		if len(argList) > 0:
			if len(argList) == 1:
				argument = argList[0]
			if len(argList) > 1:
				argument = argList
	
			setattr(command, value, argument)
			logger.info('argument: %s, value: %s' % (value, argument))

# Format the return message
def get_return(success, message):
	if success:
		ret = {
			"statusCode": 200,
			"isBase64Encoded": False,
			"headers": {
				"Content-Type": "application/json",
				"Access-Control-Allow-Origin": "*"
			}
			#TODO preciso disso para o challenge, mas os modais param de funcionar :-(
			#,'body': json.dumps(message)
		}

	else:
		ret = {
			"statusCode": 500,
			"isBase64Encoded": False,
			"headers": {
				"Content-Type": "application/json",
				"Access-Control-Allow-Origin": "*"
			}, 
			'body': json.dumps(message)
		}

	logger.info('return: ' + json.dumps(ret))

	return ret

# To execute by command line
if __name__ == "__main__":
	args = ''
	for index in range(len(sys.argv)):
		if index > 0:
			args += sys.argv[index] + ' '

	handler (json.loads(args), None)