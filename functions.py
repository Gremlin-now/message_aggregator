import json
import re
import time
import string
from fuzzywuzzy import fuzz
import emoji
import requests
from pyrogram import Client
from config import targets, URL_API_NEURAL


def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text


def get_normal_text_from(msg):
    text = str(msg.text) if msg.text is not None else str(msg.caption)
    text = re.sub(r'http\S+', '', text)
    text = " ".join(re.split("\n|\xa0", text))
    text = strip_emoji(text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def send_json(json_dict):
    try:
        if len(json_dict["content"].split()) >= 2:
            response = requests.post(URL_API_NEURAL, json=json_dict)
            print(json_dict, " - отправил - ", response.status_code)
            return True
    except Exception as e:
        print(json_dict, " - ERROR: ", e)
    print(json_dict, " -не отправил")
    return False


def get_json_as_str(msg):
    json_str = str(get_json_as_dict(msg)).replace("'", '"')
    return json_str


def get_json_as_dict(msg):
    username = msg.chat.username
    msg_id = msg.id
    text = get_normal_text_from(msg)
    json_dict = {"username": username, "msg_id": str(msg_id), "content": text}
    return json_dict


def save_and_send_all_history(user: Client):
    user.start()
    count_req = 0
    for target in targets:
        for msg in user.get_chat_history(target):
            json_str = get_json_as_str(msg)
            if save_jsonline_in_file(json_str):
                json_dict = get_json_as_dict(msg)
                if send_json(json_dict):
                    count_req += 1
                if count_req == 200:
                    time.sleep(10)
                    count_req = 0
    user.stop()
    print("Файлы сохранены и отправлены!")


def save_jsonline_in_file(json_str: str, file_name: str = "data.jsonline"):
    with open(file_name, "a+", encoding="utf8") as json_file:
        json_file.seek(0)
        file_text = json_file.read()
        try:
            if (not re.findall(json_str, file_text)
                    and (fuzz.WRatio("найд", json_str) > 50
                         or fuzz.WRatio("наше", json_str) > 50)
                    and fuzz.WRatio("теря", json_str) < 50):
                json_file.write(json_str + "\n")
                return True
        except Exception as e:
            print(json_str, " - ERROR - ", e)
    return False
