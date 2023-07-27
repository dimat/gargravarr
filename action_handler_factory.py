from pydantic import BaseModel
from action_handler import *
from actions import *
import logging


class ActionHandlerFactory:
    def __init__(self, telegram_token, chat_id):
        self.handlers = {
            ActionIgnore: IgnoreHandler(telegram_token, chat_id),
            ActionHighRisk: HighRiskHandler(telegram_token, chat_id),
            ActionLowRisk: LowRiskHandler(telegram_token, chat_id),
            ActionOpportunity: OpportunityHandler(telegram_token, chat_id),
            ActionAddToWatchList: AddToWatchListHandler(telegram_token, chat_id),
        }

    def handle(self, action: BaseModel, entry):
        action_type = type(action)
        handler = self.handlers.get(action_type)

        if handler is None:
            logging.warning(f"No handler found for action type {action_type.__name__}. The action is ignored.")
        else:
            handler.handle_action(action, entry)
