from pyrogram import Client, filters
import requests
from fuzzywuzzy import fuzz
import json
import logging
from functions import send_json, get_json_as_str, save_jsonline_in_file, get_json_as_dict

from config import API_ID, API_HASH, BOT_TOKEN, URL_API_NEURAL

client = Client("responder",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=BOT_TOKEN
                )


@client.on_message(filters.command("start"))
async def on_start(client, msg):
    message_text = (f'Привет, {msg.chat.username}.\n'
                    f'Что бы начать работу введите запрос потерял\\нашел.\n'
                    f'А также не забудьте описать свою находку\\потерю.\n'
                    f'Это поможет улучшить поиск.')
    await client.send_message(msg.chat.id, message_text)


@client.on_message(filters.create(lambda _, __, msg: fuzz.WRatio("теря", msg.text) > 50))
async def on_lost(client, user_msg):
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
    json_dict = get_json_as_dict(user_msg)
    logging.debug(str(json_dict))
    response = requests.get(URL_API_NEURAL, json=json_dict)
    json_response = json.loads(response.json())
    bot_msg = await client.send_message(user_msg.chat.id, "Ваш запрос принят ожидайте!")
    await client.edit_message_text(chat_id=user_msg.chat.id,
                                   message_id=bot_msg.id,
                                   text=f"Найдено {len(json_response)} объявлений")
    for msg in json_response:
        logging.debug(msg["username"] + " : " + msg["msg_id"])
        await client.send_message(user_msg.chat.id, f"{msg['content']}\n\n@{msg['username']}")


def found_filter(msg):
    return fuzz.WRatio("найден", msg.text) > 50 or fuzz.WRatio("нашел", msg.text) > 50


@client.on_message(filters.create(lambda _, __, msg: found_filter(msg)))
async def on_found(client, user_msg):
    json_str = get_json_as_str(user_msg)
    if save_jsonline_in_file(json_str):
        json_dict = get_json_as_dict(user_msg)
        if (send_json(json_dict)):
            await client.send_message(user_msg.chat.id,
                                ("Ваше сообщение будет предложено другим пользователям!\n"
                                 + "Как только на него откликнутся, вы будете оповещены\n")
                                )
        return
    await client.send_message(user_msg.chat.id, "Сообщение является некоректным!")