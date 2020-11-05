# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Removeteam:

	def __init__(self, dao, message):
		self.team = None

	def execute(self):

		return Message(message="Deu certo! O time é o " + self.team)

		