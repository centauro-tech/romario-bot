import logging

from message import Message

from cmd.user import User

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Newuser:

    def __init__(self, dao, message):
       self.sender = None
       self.dao = dao
       self.user = None

    def execute(self):

        message = 'Antes de entrar em campo, você precisa conhecer as regras do jogo.'
        message = message + '\n>Dê uma olhada no nosso <https://www.notion.so/uxcentauro/Guidelines-do-Slack-03024b37b6bd4d48a7f1b23cec4118b1|Guideline> de utilização do Slack.\n>'
        message = message + '\n Se você ficar com alguma dúvida, é só me chamar digitando @Felipão ajuda.'
        sender = self.dao.get_user(self.sender)
        blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "Olá, " + sender['real_name'] + "! Meu olheiro avisou da sua chegada :soccer:"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text":  message
				}
			},
			{
				"type": "divider"
			}
		]

        mObj = Message(blocks=blocks, channel=self.sender)

        userObj = User(dao=self.dao, message=None)
        setattr(userObj, 'sender', self.sender)
        blocks.extend(userObj.execute().blocks)
        
        mObj = Message(blocks=blocks, channel=self.sender)

        return mObj