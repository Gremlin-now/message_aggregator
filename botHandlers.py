
from pyrogram import Client, filters
from dotenv import dotenv_values
from time import sleep
import re

config = dotenv_values(".env")

API_ID = int(config["API_ID"])
API_HASH = config["API_HASH"]
BOT_TOKEN = config["BOT_TOKEN"]

waiting_list = {}

client = Client("responder",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=BOT_TOKEN
                )


def send_data(data):
    print("Sending")


async def delete_from_waiting_list_and_send(key):
    sleep(30)
    send_data(waiting_list[key])
    waiting_list.pop(key)


@client.on_message(filters.command("start"))
async def on_start(client, msg):
    message_text = (f'Привет, {msg.chat.username}.\n'
                    f'Что бы начать работу введите запрос потерял\\нашел.\n'
                    f'Используя эти ключевые слова опишите, свою находку\\потерю.')
    await client.send_message(msg.chat.id, message_text)


@client.on_message(filters.create(lambda _, __, msg: re.findall("потеря", msg.text.lower())))
async def on_lost(client, msg):
    waiting_list[msg.chat.id] = {
        "id": str(msg.chat.id) + ":" + str(msg.id),
        "message_text": msg.text
    }
    print("on_lost: ", waiting_list[msg.chat.id])



