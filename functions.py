import re
import time

import requests
from pyrogram import Client
from config import targets


def send_json(j_dict):
    if len(j_dict["content"].split()) >= 2:
        requests.post("http://79.174.84.206:5000/api/neural", data=j_dict)
        return True
    return False


def get_json_as_dict(msg):
    chat_id = msg.chat.id
    msg_id = msg.id
    text = str(msg.text) if msg.text is not None else str(msg.caption)
    text = ' '.join(re.split(" |\n|\"", text))
    return {"chat_id": str(chat_id), "msg_id": str(msg_id), "content": text}


def save_and_send_all_history(user: Client):
    user.start()
    count_req = 0
    for target in targets:
        for msg in user.get_chat_history(target):
            j_dict = get_json_as_dict(msg)
            if save_jsonline_in_file(j_dict):
                if send_json(j_dict):
                    count_req += 1
                if count_req == 50:
                    time.sleep(10)
                    count_req = 0
    user.stop()


def save_jsonline_in_file(j_dict: dict, file_name: str = "data.jsonline"):
    json_string = str(j_dict)
    with open(file_name, "a+", encoding="utf8") as json_file:
        json_file.seek(0)
        file_text = json_file.read()
        if not re.findall(json_string, file_text):
            json_file.write(json_string)
            return True
    return False

