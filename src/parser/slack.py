# -*- coding: utf-8 -*-
import os
import logging
import json

from slack import WebClient
from slack.errors import SlackApiError

from ..message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = WebClient(token=os.environ['sl_token'], ssl=False)

class Slack:

	def __init__(self, event):
		if 'event' in event and 'subtype' in event['event'] and event['event']['subtype'] == 'bot_message':
			return

		if 'event' in event and 'text' in event['event']:
			self.text = event['event']['text']

		if 'event' in event and 'user' in event['event']:
			self.user = event['event']['user']

		if 'event' in event and 'channel' in event['event']:
			self.channel = event['event']['channel']

		if 'channel' in event and 'id' in event['channel']:
			self.channel = event['channel']['id']

		if 'challenge' in event:
			self.validate = event['challenge']

		if 'type' in event and event['type'] == 'block_actions':
			self.actions = str(event['actions'])

	# Envia uma mensagem no slack como o BOT
	def send_message(self, message):
		ret = None

		if isinstance(message, list):
			ret = client.chat_postMessage(
			  channel=self.channel,
			  blocks=message,
			  mrkdwn=True
			)
			
			ret = ret.data

		elif isinstance(message, str):
			ret = client.chat_postMessage(
			  channel=self.channel,
			  text=message,
			  mrkdwn=True
			)

			ret = ret.data

		return ret
