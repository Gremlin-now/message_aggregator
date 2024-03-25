from pyrogram import Client, filters
from config import API_ID, API_HASH
from functions import save_jsonline_in_file, send_json, get_json_as_str, get_json_as_dict
from config import targets


client = Client("msgHandler", api_id=API_ID, api_hash=API_HASH)


@client.on_message(filters.chat(targets))
async def get_new_messages(_, msg):
    j_str = get_json_as_str(msg)
    if save_jsonline_in_file(j_str):
        j_dict = get_json_as_dict(msg)
        send_json(j_dict)

