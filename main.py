import sys
import yaml
import openai
import logging
import schedule
import time

from action_handler import TelegramMessageSender, DiscordMessageSender, AggregateSender
from action_handler_factory import ActionHandlerFactory
from entry_handler import EntryHandler
from entry_registry import EntryRegistry
from rss_parser import RSSParser


def scan():
    """
    Load configuration, set up necessary objects and parse each RSS source.
    """
    logging.info("Starting application")

    # use the first argument as the config path or use the default one
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config/config.yaml"

    # Load configuration from yaml file
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    validate_config(config)

    senders = []
    if "telegram" in config["notify"]:
        cfg = config["notify"]["telegram"]
        if cfg["token"] is None:
            raise Exception("Telegram token is not configured")
        if cfg["chat_id"] is None:
            raise Exception("Telegram chat ID is not configured")
        senders.append(TelegramMessageSender(cfg["token"], cfg["chat_id"]))

    if "discord" in config["notify"]:
        cfg = config["notify"]["discord"]
        senders.append(DiscordMessageSender(cfg["webhook"]))

    if len(senders) == 0:
        raise Exception("No notification method is configured")

    sender = AggregateSender(senders)

    prompt = config["openai"]["prompt"]
    openai.api_key = config["openai"]["api_key"]

    registry = EntryRegistry(config["rss_cache"]["directory"])
    action_handler_factory = ActionHandlerFactory(sender)

    entry_handler = EntryHandler(action_handler_factory, prompt)

    for name in config["sources"]["rss"]:
        source = config["sources"]["rss"][name]
        parser = RSSParser(source["url"], name, registry, source["selector"])
        parser.parse(entry_handler.handle)


def validate_config(config):
    """
    Validate the configuration and raise an exception if it is not valid.
    :param config:
    :return: nothing
    :raises Exception: if the configuration is not valid
    """
    if config["openai"]["api_key"] is None:
        raise Exception("OpenAI API key is not configured")
    if config["openai"]["prompt"] is None:
        raise Exception("OpenAI prompt is not configured")


def main():
    """
    Initialize the application and start the scheduler.
    """

    logging.basicConfig(level=logging.DEBUG)

    scan()

    logging.info("Starting scheduler")
    schedule.every(2).hours.do(scan)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
