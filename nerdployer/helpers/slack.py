import requests
import json


class Slack(object):

    @staticmethod
    def notify(webhook, channel, icon, bot_name, message):
        requests.post(webhook, data=json.dumps({'channel': channel, 'username': bot_name, 'text': message, 'icon_emoji': icon}))
