# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Message:

	def __init__(self, message=None, channel=None, sender=None, blocks=None):
		self.message = message
		self.channel = channel
		self.sender = sender
		self.blocks = blocks