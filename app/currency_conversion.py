import os
import requests

from . globals import logger
from . exceptions import *

OPEN_EX_RATES_LATEST_URL = "https://openexchangerates.org/api/latest.json"
API_KEY = os.environ["OPEN_EX_RATES_API_KEY"]

# caching currecy rates for simplicity and to avoid hitting api request cap
CACHE = None


def fetch_latest_rates():
    params = {
        "app_id": API_KEY
    }
    r = requests.get(OPEN_EX_RATES_LATEST_URL, params=params)

    if r.status_code != 200:
        logger.error("Failed to fetch exchange rates response")
        raise ApiException(INTERNAL_SERVER_ERROR, status_code=500)

    return r.json()['rates']

def ensure_cache_is_populated():
    global CACHE
    if CACHE is None:
        CACHE = fetch_latest_rates()

def get_currency_rates():
    ensure_cache_is_populated()
    return CACHE

def convert_to_usd(amount: int, from_currency:str):
    if from_currency == "USD":
        return amount

    ensure_cache_is_populated()

    usd_amount = amount / CACHE[from_currency]
    return int(usd_amount)
