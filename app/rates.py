from flask import Blueprint, request, jsonify
from datetime import date

from . rates_queries import find_avg_prices, find_avg_prices_null, insert_prices
from . currency_conversion import convert_to_usd, get_currency_rates
from . exceptions import *
from . globals import logger

import os

rates_bp = Blueprint('rates_bp', __name__)

@rates_bp.errorhandler(ApiException)
def handle_api_exception(ex: ApiException):
    logger.error(f"Error occured while handling API request. Code: [{ex.error[CODE_KEY]}], Message: [{ex.error[MSG_KEY]}]")
    return jsonify(ex.error), ex.status_code

# seems like adding a JSONEncoder is also a possibility, but kept it simple for now
def map_avg_price(avg_price):
    return {
        "day": avg_price['day'].isoformat(),
        "avg_price": avg_price['avg_price']
    }

def validate_date_from_and_date_to(date_from_str: str, date_to_str: str):
    date_from = None
    date_to = None

    try:
        date_from = date.fromisoformat(date_from_str)
    except ValueError:
        raise ApiException(DATE_FROM_INVALID_FORMAT)

    try:
        date_to = date.fromisoformat(date_to_str)
    except ValueError:
        raise ApiException(DATE_TO_INVALID_FORMAT)


    date_from = date.fromisoformat(date_from_str)
    date_to = date.fromisoformat(date_to_str)

    if date_from > date_to:
        raise ApiException(DATE_FROM_AFTER_DATE_TO)

def validate_origin_and_destination(origin: str, destination: str):
    if origin is None:
        raise ApiException(ORIGIN_NULL)
    if destination is None:
        raise ApiException(DESTINATION_NULL)
    if origin == destination:
        raise ApiException(ORIGIN_AND_DESTINATION_SAME)

@rates_bp.route("/rates", methods=['GET'])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # could add some validation to check if the origin and destination exists
    validate_date_from_and_date_to(date_from, date_to)
    validate_origin_and_destination(origin, destination)

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

    # could add some validation to check if the origin and destination exists
    validate_date_from_and_date_to(date_from, date_to)
    validate_origin_and_destination(origin, destination)

    avg_prices_null = find_avg_prices_null(
        date_from, 
        date_to, 
        origin, 
        destination
    )

    return jsonify([map_avg_price(avg_price) for avg_price in avg_prices_null])

def is_int(int_str: str):
    try:
        int(int_str)
        return True
    except ValueError:
        return False

def validate_price(price: str):
    if price is None:
        raise ApiException(PRICE_NULL)
    if not is_int(price):
        raise ApiException(PRICE_INVALID)
    if int(price) < 0:
        raise ApiException(PRICE_NEGATIVE)

def validate_price_dict(price: dict):
    if price is None:
        raise ApiException(PRICE_NULL)
    if get_currency_rates().get(price['currency']) is None:
        raise ApiException(PRICE_UNKNOWN_CURRENCY)
    validate_price(price['amount'])

@rates_bp.route("/rates", methods=['POST'])
def add_rate():
    body = request.json
    date_from_str = body['date_from']
    date_to_str = body['date_to']
    orig_code = body['origin_code']
    dest_code = body['destination_code']
    price_param = body['price']

    # could add some validation to check if the origin and destination exists
    validate_date_from_and_date_to(date_from_str, date_to_str)
    validate_origin_and_destination(orig_code, dest_code)

    price = None

    if isinstance(price_param, dict):
        validate_price_dict(price_param)
        price = convert_to_usd(price_param['amount'], price_param['currency'])
    else:
        validate_price(price_param)
        price = int(price_param)

    date_from = date.fromisoformat(date_from_str)
    date_to = date.fromisoformat(date_to_str)

    insert_prices(date_from, date_to, orig_code, dest_code, price)

    return "", 200
