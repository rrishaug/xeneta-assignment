from flask import Blueprint, request, jsonify
from datetime import date

from . rates_queries import find_avg_prices, find_avg_prices_null, insert_prices, insert_prices_experimental
from . currency_conversion import convert_to_usd

import os

rates_bp = Blueprint('rates_bp', __name__)

# seems like adding a JSONEncoder is also a possibility, but kept it simple for now
def map_avg_price(avg_price):
    return {
        "day": avg_price['day'].isoformat(),
        "avg_price": avg_price['avg_price']
    }

@rates_bp.route("/rates", methods=['GET'])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    avg_prices = find_avg_prices(
        date_from, 
        date_to, 
        origin, 
        destination
    )

    return jsonify([map_avg_price(avg_price) for avg_price in avg_prices])

@rates_bp.route("/rates_null", methods=['GET'])
def get_rates_null():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    avg_prices_null = find_avg_prices_null(
        date_from, 
        date_to, 
        origin, 
        destination
    )

    return jsonify([map_avg_price(avg_price) for avg_price in avg_prices_null])

@rates_bp.route("/rates", methods=['POST'])
def add_rate():
    body = request.json
    date_from = body['date_from']
    date_to = body['date_to']
    orig_code = body['origin_code']
    dest_code = body['destination_code']
    price = body['price']

    if isinstance(price, dict):
        price = convert_to_usd(price['amount'], price['currency'])

    date_from = date.fromisoformat(date_from)
    date_to = date.fromisoformat(date_to)

    # created a insert function that creates the date range in postgres instead of looping or batch inserts in python
    # insert_prices(date_from, date_to, orig_code, dest_code, price)
    insert_prices_experimental(date_from, date_to, orig_code, dest_code, price)

    return "", 200
