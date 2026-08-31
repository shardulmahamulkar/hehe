import asyncio
import os
import random
from xmlrpc import client
import requests
import websockets
from dotenv import load_dotenv
from websockets import client

load_dotenv()

  # Generate a unique client ID based on the current timestamp
class Room:
    def __init__(self, roomid: int):
        self.roomid = int(roomid)  # A

class Client:

    def __init__(self, client_id: str):
        self.client_id = str(client_id) + str(random.randint(1, 1000))  # Add a random number to ensure uniqueness

    # async def clientid(websocket):
    #     while True:
    #         name = input("Enter your client ID: ")
    #         print(f"\n{message}")
    
    async def send_messages(self, websocket):
        while True:
            msg = await asyncio.to_thread(input, "You: ")

            await websocket.send(msg)


    async def receive_messages(self, websocket):
        while True:
            message = await websocket.recv()

            print(f"\n{message}")

async def send_to_discord(webhook_url):
    while True:
        message = await asyncio.to_thread(input, "You: ")

        await asyncio.to_thread(
            requests.post,
            webhook_url,
            json={"content": message},
        )


async def receive_from_discord(url, headers):
    while True:
        response = await asyncio.to_thread(
            requests.get,
            url,
            headers=headers,
            params={"limit": 10},
        )

        if response.status_code == 200:
            for msg in reversed(response.json()):
                print(f"\n{msg['author']['username']}: {msg['content']}")

        await asyncio.sleep(2)
async def main():
    ngrok_url = input("Enter the ngrok URL: ").rstrip("/")
    dorm=input("discord or normal? (d/n): ")
    if ngrok_url.startswith("https://"):
        ngrok_url = "wss://" + ngrok_url.removeprefix("https://")
    elif ngrok_url.startswith("http://"):
        ngrok_url = "ws://" + ngrok_url.removeprefix("http://")
    c = input('Do you want to create a room? (y/n): ')
    if c == 'n':
        roomid = input("Enter  room ID: ")
    else :
        roomid = random.randint(1, 1000)
        print(f"Room created with ID: {roomid}")
    client_id = input("Enter your client ID: ")
    client = Client(client_id)
    room = Room(roomid)
    
    if(dorm=='d'):
        webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
        channel_id = os.environ["DISCORD_CHANNEL_ID"]
        bot_token = os.environ["DISCORD_BOT_TOKEN"]

        while True:
            msg = await asyncio.to_thread(input, "You: ")
            data = {
                "content": msg
            }
            response = requests.post(webhook_url, json=data)
            
            url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
            headers = {
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json"
            }
            
            # Optional query parameters: limit (max 100), before (message ID), after (message ID)
            params = {
                "limit": 1
            }
            
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
             messages = response.json() # Returns a JSON array of message objects
             for msg in messages:
                 print(f"{msg['author']['username']}: {msg['content']}")

        
    else:

        uri = f"{ngrok_url}/ws/{room.roomid}/{client.client_id}"
    

        async with websockets.connect(uri) as websocket:

            await asyncio.gather(
                # client.clientid(websocket),
                client.send_messages(websocket),
                client.receive_messages(websocket)
            )


if __name__ == "__main__":
    asyncio.run(main())
