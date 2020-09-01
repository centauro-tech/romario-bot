# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Tag:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.type = None
		self.value = None

	def execute(self):
		tag = self.dao.save_tag(type_tag=self.type, tag_value=self.value)

		mObj = Message(message='Tag do tipo _*' + self.type + '*_, valor _*' + self.value + '*_ incluída com sucesso')
		return mObj