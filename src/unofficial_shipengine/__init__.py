import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHIPENGINE_API_KEY: str = os.environ.get("SHIPENGINE_API_KEY")


class MissingAPIKey(Exception):
    pass


if SHIPENGINE_API_KEY is None:
    raise MissingAPIKey()

session = requests.Session()
session.headers = {
    "Host": "api.shipengine.com",
    "API-Key": SHIPENGINE_API_KEY,
    "Content-Type": "application/json",
}
