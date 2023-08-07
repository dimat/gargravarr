# Gargravarr

> Gargravarr, the disembodied mind and custodian of the Total Perspective Vortex on Frogstar World B 
> ("the most totally evil place in the galaxy"), suffers from real-life dualism and is therefore having 
> trial separation with his body.

**Disclaimer**: This is a work in progress. I'm new to Python, so I'm sure the code is not very Pythonic.

## What is Gargravarr?
It is a bot that will help you to stay on top of the latest news from your favorite websites passing
them through OpenAI's GPT and if there is something interesting that poses a risk or an opportunity
to what you do, it will notify you via Telegram.

## Configuration
Place this file to `data/config.yaml` and fill the gaps:

```yaml
rss_cache:
  directory: ./data/

openai:
  api_key: sk-....

  prompt: |
    ... your prompt here ... Explain what you do and what you are looking for.
    For each of the following news you can answer the following:
    - ignore: the news is not relevant
    - high risk: the news is relevant and you need to take action. Please also explain briefly what action you will take
    - low risk: the news is relevant but you can ignore it. Please explain briefly what the risk is and if any action or additional monitoring should be done.
    - opportunity: the news is relevant and you can take advantage of it. Also opportunity should be actionable, such as adding new integrations to the current trading set-up. If it's a very generic opportunity, then skip it. Please also explain briefly what the opportunity could be.
    - add to watch list: the news is relevant and you need to monitor it. Please explain briefly what the risk is and if any action or additional monitoring should be done.
    - more information: at first you are given a summary of the news, then you can read the full article if you need more information.

notify:
  discord:
    webhook:
      
  telegram:
      token: 
      chat_id: 

sources:
  rss:
    coindesk:
      url: https://www.coindesk.com/arc/outboundfeeds/rss
      selector: section.at-body
    cointelegraph:
      url: https://cointelegraph.com/feed
      selector: article.post__article
```

## Running using Docker

Start:
```bash
docker-compose up -d --build
```

Stop:
```bash
docker-compose down
```

