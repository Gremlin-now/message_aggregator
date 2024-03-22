from mailbox import Message

from pyrogram import Client, filters
from dotenv import dotenv_values

config = dotenv_values(".env")

API_ID = int(config["API_ID"])
API_HASH = config["API_HASH"]

targets = [
    "peepoSwamp"
]

client = Client("msgHandler", api_id=API_ID, api_hash=API_HASH)

@client.on_message(filters.chat(targets))
def get_new_messages(client: Client, message: Message):
    print(message)