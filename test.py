import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]

url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Optional query parameters: limit (max 100), before (message ID), after (message ID)
params = {
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    messages = response.json() # Returns a JSON array of message objects
    for msg in messages:
        print(f"{msg['author']['username']}: {msg['content']}")
else:
    print(f"Failed to fetch messages. Error code: {response.status_code}")
    print(response.text)
