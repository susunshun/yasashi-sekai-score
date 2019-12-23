import settings
import requests
import oseti
import numpy as np
from datetime import datetime

SLACK_URL = "https://slack.com/api/channels.history"

# see: https://api.slack.com/methods/channels.history
payload = {
    "channel": settings.SLACK_CHANNEL_ID,
    "token": settings.SLACK_TOKEN,
    "oldest": datetime(2019,12,23,0,0).strftime('%s')
}

response = requests.get(SLACK_URL, params=payload)
json_data = response.json()
msgs = json_data['messages']

texts = [msg.get('text') for msg in msgs]

# see: https://github.com/ikegami-yukino/oseti
analyzer = oseti.Analyzer()
for text in texts:
    score = analyzer.analyze(text)

    if len(score) > 0:
        score = np.average(score)

    print(str(score) + " => " + text)
