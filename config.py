from dotenv import dotenv_values

config = dotenv_values(".env")

API_ID = int(config["API_ID"])
API_HASH = config["API_HASH"]
BOT_TOKEN = config["BOT_TOKEN"]

HOST = "http://172.18.0.1:5000"

URL_API_NEURAL = f"{HOST}/api/neural"

targets = [
    "LostFoundK",
    "kriminalunet",
    "poteryal_azn"
]