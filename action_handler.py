import logging
import requests
from actions import *


def escape_markdown(text):
    # List of special characters that need to be escaped
    escape_chars = '\*_[]()~`>#'

    return ''.join('\\' + char if char in escape_chars else char for char in text)


class BaseActionHandler:
    """
    Base class for action handlers
    """
    def handle_action(self, action: BaseModel, entry):
        pass


class BaseMessageSender:
    """
    Base class for message senders
    """
    def send_message(self, message):
        pass


class TelegramMessageSender(BaseMessageSender):
    """
    Telegram message sender
    """
    def __init__(self, telegram_token, chat_id):
        self.telegram_token = telegram_token
        self.chat_id = chat_id

    def send_message(self, message):
        url = 'https://api.telegram.org/bot' + self.telegram_token + '/sendMessage'
        response = requests.post(url, json={
            'parse_mode': 'Markdown',
            'chat_id': self.chat_id,
            'text': escape_markdown(message)
        })
        logging.debug(f"Telegram response: {response.status_code} {response.json()}")
        return response.json()


class DiscordMessageSender(BaseMessageSender):
    """
    Discord message sender
    """
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, message):
        response = requests.post(self.webhook_url, json={
            'content': message
        })
        logging.debug(f"Discord response: {response.status_code}")
        return response.json()


class AggregateSender(BaseMessageSender):
    """
    Aggregate message sender
    """
    def __init__(self, senders):
        self.senders = senders

    def send_message(self, message):
        for sender in self.senders:
            sender.send_message(message)


class BaseSenderActionHandler(BaseActionHandler):
    """
    Base class for Telegram action handlers
    """
    def __init__(self, sender):
        self.sender = sender

    def message(self, action: BaseModel, entry) -> str:
        return ""

    def handle_action(self, action: BaseModel, entry):
        logging.info(f"Handling action {action} for entry {entry.link}")
        logging.debug(f"Action model dump: {action.model_dump()}")
        message = self.message(action, entry)
        if message:
            try:
                self.sender.send_message(message)
            except Exception as e:
                logging.error(f"Failed to send message: {e}")


class IgnoreHandler(BaseActionHandler):
    pass


class HighRiskTelegramHandler(BaseSenderActionHandler):
    def message(self, action: ActionHighRisk, entry):
        return f"🚨🚨🚨High Risk: {action.reason}\n\nAffected networks: {', '.join(action.affected_networks)}\n\n{entry.link}"


class LowRiskTelegramHandler(BaseSenderActionHandler):
    def message(self, action: ActionLowRisk, entry):
        return f"⚠️Low Risk:{action.reason}\n\nAffected networks: {', '.join(action.affected_networks)}\n\n{entry.link}"


class OpportunityTelegramHandler(BaseSenderActionHandler):
    def message(self, action: ActionOpportunity, entry):
        return f"🤩 Opportunity: {action.reason}\n\nAffected networks: {', '.join(action.affected_networks)}\n\n{entry.link}"


class AddToWatchListHandler(BaseActionHandler):
    pass
