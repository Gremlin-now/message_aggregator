import json
import re
import time
import string
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

def send_json(json_str):
    try:
      json_as_dict = json.loads(json_str)
      if len(json_as_dict["content"].split()) >= 2:
          response = requests.post(URL_API_NEURAL, json=json_as_dict)
          print(json_str, " - отправил - ", response.status_code)
          return True
    except Exception as e:
        print(json_str, " - ERROR: ", e)
    print(json_str, " -не отправил")
    return False


def get_json_as_str(msg):
    chat_id = msg.chat.id
    msg_id = msg.id
    text = get_normal_text_from(msg)
    json_dict = {"chat_id": str(chat_id), "msg_id": str(msg_id), "content": text}
    json_str = str(json_dict).replace("'", '"')
    return json_str


def save_and_send_all_history(user: Client):
    user.start()
    count_req = 0
    for target in targets:
        for msg in user.get_chat_history(target):
            json_str = get_json_as_str(msg)
            if save_jsonline_in_file(json_str):
                if send_json(json_str):
                    count_req += 1
                if count_req == 50:
                    time.sleep(10)
                    count_req = 0
    user.stop()
    print("Файлы сохранены и отправлены!")


def save_jsonline_in_file(json_str: dict, file_name: str = "data.jsonline"):
    with open(file_name, "a+", encoding="utf8") as json_file:
        json_file.seek(0)
        file_text = json_file.read()
        try:
            if not re.findall(json_str, file_text):
              json_file.write(json_str + "\n")
              return True
        except Exception as e:
            print(json_str, " - ERROR - ", e)
    return False

