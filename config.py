from dotenv import dotenv_values

config = dotenv_values(".env")

API_ID = int(config["API_ID"])
API_HASH = config["API_HASH"]
BOT_TOKEN = config["BOT_TOKEN"]

targets = [
    "LostFoundK",
    "kriminalunet",
    "poteryal_azn"
]