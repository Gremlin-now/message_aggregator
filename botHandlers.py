from pyrogram import Client, filters
import requests
from requests import HTTPError
from fuzzywuzzy import fuzz
from functions import send_json, get_json_as_dict, save_jsonline_in_file

from config import API_ID, API_HASH, BOT_TOKEN

waiting_list = {}

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
    bot_msg = client.send_message(user_msg.chat.id, "Ваш запрос принят ожидайте!")
    try:
        j_dict = get_json_as_dict(user_msg)
        response = requests.get("ЗАЛУПА", data=j_dict)
        response.raise_for_status()
        json_response = response.json()
        data = json_response["data"]
        client.edit_message_text(chat_id=user_msg.chat.id,
                                 message_id=bot_msg.id,
                                 text=f"Найдено {len(data)} объявлений")
        for msg in data:
            client.copy_message(user_msg.chat.id, int(msg["chat_id"]), int(msg["msg_id"]))
    except HTTPError as http_err:
        print(f"STATUS: {http_err}")
    except Exception as err:
        print(f"ERROR: {err}")


def found_filter(_, __, msg):
    return fuzz.WRatio("найден", msg.text) > 50 or fuzz.WRatio("нашел", msg.text) > 50


@client.on_message(filters.create(found_filter))
async def on_found(client, user_msg):
    j_dict = get_json_as_dict(user_msg)
    if save_jsonline_in_file(j_dict):
        send_json(j_dict)
        client.send_message(user_msg.chat.id,
                            ("Ваше сообщение будет предложено другим пользователям!\n"
                             + "Как только на него откликнутся, вы будете оповещены\n")
                            )
        return
    client.send_message(user_msg.chat.id, "Сообщение является некоректным!")