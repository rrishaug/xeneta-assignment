from flask import Blueprint, request, jsonify

from . rates_queries import find_avg_prices, find_avg_prices_null

import os

rates_bp = Blueprint('rates_bp', __name__)

# seems like adding a JSONEncoder is also a possibility, but kept it simple for now
def map_avg_price(avg_price):
    return {
        "day": avg_price['day'].isoformat(),
        "avg_price": avg_price['avg_price']
    }

@rates_bp.route("/rates")
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

@rates_bp.route("/rates_null")
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

