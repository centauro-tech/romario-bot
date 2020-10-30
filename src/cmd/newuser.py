import logging

from message import Message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Newuser:

    def __init__(self, dao, message):
       self.sender = None

    def execute(self):

        message = 'Antes de entrar em campo, você precisa conhecer as regras do jogo.'
        message = message + '\n>De uma olhada no nosso <https://www.notion.so/uxcentauro/Guidelines-do-Slack-277117b085a3479f85c3a3bd3b5e141f|Guidelines> de utilização do Slack.\n>'
        message = message + '\n Se você ficar com alguma dúvida, é só digitar @Felipão ajuda.'
        blocks = [
			{
				"type": "header",
				"text": {
					"type": "plain_text",
					"text": "Bem vinde  ao time! :soccer:"
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
        
        return mObj