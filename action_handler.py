import logging
import requests
from actions import *


def escape_markdown(text):
    # List of special characters that need to be escaped
    escape_chars = '\*_[]()~`>#'

    return ''.join('\\' + char if char in escape_chars else char for char in text)


class BaseActionHandler:
    def __init__(self, telegram_token, chat_id):
        self.telegram_token = telegram_token
        self.chat_id = chat_id

    def send_telegram_message(self, message):
        url = 'https://api.telegram.org/bot' + self.telegram_token + '/sendMessage'
        response = requests.post(url, json={
            'parse_mode': 'Markdown',
            'chat_id': self.chat_id,
            'text': escape_markdown(message)
        })
        logging.debug(f"Telegram response: {response.status_code} {response.json()}")
        return response.json()

    def handle_action(self, action: BaseModel, entry):
        logging.info(f"Handling action {action} for entry {entry.link}")
        logging.debug(f"Action model dump: {action.model_dump()}")


class IgnoreHandler(BaseActionHandler):
    pass


class HighRiskHandler(BaseActionHandler):
    def handle_action(self, action: ActionHighRisk, entry):
        BaseActionHandler.handle_action(self, action, entry)
        message = f"🚨🚨🚨High Risk: {action.reason}\n\nAffected networks: {', '.join(action.affected_networks)}\n\n{entry.link}"
        self.send_telegram_message(message)


class LowRiskHandler(BaseActionHandler):
    def handle_action(self, action: ActionLowRisk, entry):
        BaseActionHandler.handle_action(self, action, entry)
        message = f"⚠️Low Risk:{action.reason}\n\nAffected networks: {', '.join(action.affected_networks)}\n\n{entry.link}"
        self.send_telegram_message(message)


class OpportunityHandler(BaseActionHandler):
    def handle_action(self, action: ActionOpportunity, entry):
        BaseActionHandler.handle_action(self, action, entry)
        message = f"🤩 Opportunity: {action.reason}\n\nAffected networks: {', '.join(action.affected_networks)}\n\n{entry.link}"
        self.send_telegram_message(message)


class AddToWatchListHandler(BaseActionHandler):
    pass
