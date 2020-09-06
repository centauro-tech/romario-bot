# -*- coding: utf-8 -*-
import configparser
import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Removetechinfo:

	def __init__(self, dao, message):
		self.dao = dao
		self.text = message
		self.team = None
		self.idx = None
		self.sender = None

	def execute(self):
		savedTeam = self.dao.get_saved_team(team_id=self.team)

		tech_info_lst = savedTeam['tech_info']
		tech_info = tech_info_lst[int(self.idx)]
		tech_info_lst.remove(tech_info)

		savedTeam = self.dao.save_team(team_id=self.team, tech_info_lst=tech_info_lst)

		mObj = None
		if self.sender is not None:
			mObj = []
			mObj.append(Message(message='<@' + self.sender + '> removeu um item da ficha técnica do time ' + savedTeam['name'], channel=savedTeam['slack_channel']))
			mObj.append(Message(message='Item removido com sucesso ao time ' + savedTeam['name'], channel=self.sender))

		return mObj