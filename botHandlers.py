from pyrogram import Client, types
from dotenv import dotenv_values

config = dotenv_values(".env")

API_ID = int(config["API_ID"])
API_HASH = config["API_HASH"]
BOT_TOKEN = config["BOT_TOKEN"]

client = Client("responder",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=BOT_TOKEN
                )

@client.on_message()
async def onStart(client, msg):
    print(msg.chat.id)

