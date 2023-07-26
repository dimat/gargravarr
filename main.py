import sys

import yaml
import openai
from action_handler_factory import ActionHandlerFactory
from entry_handler import EntryHandler
from entry_registry import EntryRegistry
from rss_parser import RSSParser
import schedule
import time


def scan():
    print("Starting application")

    # use the first argument as the config path or use the default one
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config/config.yaml"

    # Load configuration from yaml file
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    prompt = config["openai"]["prompt"]

    if prompt is None:
        raise Exception("Prompt is not configured")

    openai.api_key = config["openai"]["api_key"]
    registry = EntryRegistry(config["rss_cache"]["directory"])
    action_handler_factory = ActionHandlerFactory(config["telegram"]["token"], config["telegram"]["chat_id"])

    entry_handler = EntryHandler(action_handler_factory, prompt)

    for name in config["sources"]["rss"]:
        source = config["sources"]["rss"][name]
        RSSParser(source["url"], name, registry, source["selector"]).parse(entry_handler.handle)


def main():
    scan()

    print("Starting scheduler")
    schedule.every(2).hours.do(scan)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
