# -*- coding: utf-8 -*-

import configparser
import sys

from message import Message

class Notechuser:

	def __init__(self, help, message):
		self.text = message

	def execute(self):
		mObj = Message(message='Ahhhh, estou em fase de testes, por enquanto a peneira é apenas para Tecnologia. Assim que isso mudar, aviso :wink:')
		return mObj