import os
import requests

OPEN_EX_RATES_LATEST_URL = "https://openexchangerates.org/api/latest.json"
API_KEY = os.environ["OPEN_EX_RATES_API_KEY"]

# caching currecy rates for simplicity and to avoid hitting api request cap
CACHE = None


def fetch_latest_rates():
    params = {
        "app_id": API_KEY
    }
    r = requests.get(OPEN_EX_RATES_LATEST_URL, params=params)
    return r.json()['rates']

def convert_to_usd(amount: int, from_currency:str):
    global CACHE
    if CACHE is None:
        CACHE = fetch_latest_rates()

    usd_amount = amount / CACHE[from_currency]
    return int(usd_amount)
