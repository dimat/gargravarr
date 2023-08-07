from pydantic import BaseModel
from action_handler import *
from actions import *
import logging


class ActionHandlerFactory:
    def __init__(self, sender):
        self.handlers = {
            ActionIgnore: IgnoreHandler(),
            ActionHighRisk: HighRiskTelegramHandler(sender),
            ActionLowRisk: LowRiskTelegramHandler(sender),
            ActionOpportunity: OpportunityTelegramHandler(sender),
            ActionAddToWatchList: AddToWatchListHandler(),
        }

    def handle(self, action: BaseModel, entry):
        action_type = type(action)
        handler = self.handlers.get(action_type)

        if handler is None:
            logging.warning(f"No handler found for action type {action_type.__name__}. The action is ignored.")
        else:
            handler.handle_action(action, entry)
