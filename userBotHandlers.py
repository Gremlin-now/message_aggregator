from pyrogram import Client, filters
from dotenv import dotenv_values

config = dotenv_values(".env")

API_ID = int(config["API_ID"])
API_HASH = config["API_HASH"]

targets = [
    "LostFoundK",
    "kriminalunet",
    "poteryal_azn"
]

client = Client("msgHandler", api_id=API_ID, api_hash=API_HASH)


@client.on_message(filters.chat(targets))
def get_new_messages(client, msg):
    with open("data.jsonlines", "a") as json_file:
        msg_id = str(msg.chat.id) + ":" + str(msg.id)
        print(print(msg_id, " - добавлен"))
        json_file.write("\n{\"id\": "+msg_id+"}")
