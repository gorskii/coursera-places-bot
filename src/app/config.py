import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ["PLACES_BOT_API_TOKEN"]

REDIS_URL = os.environ["REDIS_URL"]
