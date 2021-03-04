import pytest
import os
import httpretty
import json

from flask import url_for

from app.exceptions import *

def test_get_rates(app, rest_client):
    expected_avg_prices = [
        {
            "avg_price": 1112,
            "day": "2016-01-01"
        },
        {
            "avg_price": 1112,
            "day": "2016-01-02"
        },
        {
            "avg_price": 1112,
            "day": "2016-01-03"
        }
    ]

    date_from = '2016-01-01'
    date_to = '2016-01-03'
    origin = 'CNSGH'
    destination = 'north_europe_main'

    with app.test_request_context():
        url = url_for(
            'rates_bp.get_rates',
            date_from=date_from,
            date_to=date_to,
            origin=origin,
            destination=destination
        )
        response = rest_client.get(url)

    assert len(response.json) == len(expected_avg_prices)
    assert response.json == expected_avg_prices

def test_get_rates_null_expect_not_null(app, rest_client):
    expected_avg_prices = [
        {
            "avg_price": 1112,
            "day": "2016-01-01"
        },
        {
            "avg_price": 1112,
            "day": "2016-01-02"
        },
        {
            "avg_price": 1112,
            "day": "2016-01-03"
        }
    ]

    date_from = '2016-01-01'
    date_to = '2016-01-03'
    origin = 'CNSGH'
    destination = 'north_europe_main'

    with app.test_request_context():
        url = url_for(
            'rates_bp.get_rates_null',
            date_from=date_from,
            date_to=date_to,
            origin=origin,
            destination=destination
        )
        response = rest_client.get(url)

    assert len(response.json) == len(expected_avg_prices)
    assert response.json == expected_avg_prices

def test_get_rates_null_expect_null(app, rest_client):
    expected_avg_prices = [
        {
            "avg_price": None,
            "day": "2016-01-01"
        },
        {
            "avg_price": None,
            "day": "2016-01-02"
        },
        {
            "avg_price": None,
            "day": "2016-01-03"
        }
    ]

    date_from = '2016-01-01'
    date_to = '2016-01-03'
    origin = 'CNGGZ'
    destination = 'NOSVG'

    with app.test_request_context():
        url = url_for(
            'rates_bp.get_rates_null',
            date_from=date_from,
            date_to=date_to,
            origin=origin,
            destination=destination
        )
        response = rest_client.get(url)

    assert len(response.json) == len(expected_avg_prices)
    assert response.json == expected_avg_prices

@pytest.mark.parametrize(
        'route,             date_from,     date_to,        origin,     destination,     expected_error',
    [
        ('get_rates',       '2016-01-0',   '2016-01-03',   'CNGGZ',    'NOSVG',         DATE_FROM_INVALID_FORMAT),
        ('get_rates',       '2016-01-01',  '2016-01-0',    'CNGGZ',    'NOSVG',         DATE_TO_INVALID_FORMAT),
        ('get_rates',       '2016-01-03',  '2016-01-01',   'CNGGZ',    'NOSVG',         DATE_FROM_AFTER_DATE_TO),
        ('get_rates',       '2016-01-01',  '2016-01-03',   None,       'NOSVG',         ORIGIN_NULL),
        ('get_rates',       '2016-01-01',  '2016-01-03',   'CNGGZ',    None,            DESTINATION_NULL),
        ('get_rates',       '2016-01-01',  '2016-01-03',   'CNGGZ',    'CNGGZ',         ORIGIN_AND_DESTINATION_SAME),
        ('get_rates_null',  '2016-01-0',   '2016-01-03',   'CNGGZ',    'NOSVG',         DATE_FROM_INVALID_FORMAT),
        ('get_rates_null',  '2016-01-01',  '2016-01-0',    'CNGGZ',    'NOSVG',         DATE_TO_INVALID_FORMAT),
        ('get_rates_null',  '2016-01-03',  '2016-01-01',   'CNGGZ',    'NOSVG',         DATE_FROM_AFTER_DATE_TO),
        ('get_rates_null',  '2016-01-01',  '2016-01-03',   None,       'NOSVG',         ORIGIN_NULL),
        ('get_rates_null',  '2016-01-01',  '2016-01-03',   'CNGGZ',    None,            DESTINATION_NULL),
        ('get_rates_null',  '2016-01-01',  '2016-01-03',   'CNGGZ',    'CNGGZ',         ORIGIN_AND_DESTINATION_SAME)
    ]
)
def test_get_rates_given_invalid_params(app, rest_client, route, date_from, date_to, origin, destination, expected_error):
    with app.test_request_context():
        url = url_for(
            f"rates_bp.{route}",
            date_from=date_from,
            date_to=date_to,
            origin=origin,
            destination=destination
        )
        response = rest_client.get(url)

    assert response.json == expected_error

def test_add_rate(app, rest_client, database):
    expected_get_2_result = [
        {
            "avg_price": 1234,
            "day": "2020-12-23"
        },
        {
            "avg_price": 1234,
            "day": "2020-12-24"
        },
        {
            "avg_price": 1234,
            "day": "2020-12-25"
        }
    ]
    rate = {
        "date_from": "2020-12-23",
        "date_to": "2020-12-25",
        "origin_code": "CNGGZ",
        "destination_code": "NOSVG",
        "price": 1234
    }

    with app.test_request_context():
        get_url = url_for(
            'rates_bp.get_rates',
            date_from=rate['date_from'],
            date_to=rate['date_to'],
            origin=rate['origin_code'],
            destination=rate['destination_code']
        )
        post_url = url_for('rates_bp.add_rate')

        get_1_response = rest_client.get(get_url)
        post_response = rest_client.post(post_url, json=rate)
        get_2_response = rest_client.get(get_url)

    assert get_1_response.status_code == 200
    assert post_response.status_code == 200
    assert get_2_response.status_code == 200

    assert len(get_1_response.json) == 0
    assert len(get_2_response.json) == 3

    assert get_2_response.json == expected_get_2_result
    assert post_response.json == expected_get_2_result

@httpretty.activate
def test_add_rate_with_conversion(app, rest_client):
    api_key = os.environ["OPEN_EX_RATES_API_KEY"]
    open_ex_api_url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    latest_ex_rates = {
        "rates": {
            "NOK": 0.1
        }
    }
    httpretty.register_uri(httpretty.GET, open_ex_api_url, body=json.dumps(latest_ex_rates))
    expected_get_2_result = [
        {
            "avg_price": 10000,
            "day": "2021-01-01"
        }
    ]
    rate = {
        "date_from": "2021-01-01",
        "date_to": "2021-01-01",
        "origin_code": "CNGGZ",
        "destination_code": "NOSVG",
        "price": {
            "amount": 1000,
            "currency": "NOK"
        }
    }

    with app.test_request_context():
        get_url = url_for(
            'rates_bp.get_rates',
            date_from=rate['date_from'],
            date_to=rate['date_to'],
            origin=rate['origin_code'],
            destination=rate['destination_code']
        )
        post_url = url_for('rates_bp.add_rate')

        get_1_response = rest_client.get(get_url)
        post_response = rest_client.post(post_url, json=rate)
        get_2_response = rest_client.get(get_url)

    assert get_1_response.status_code == 200
    assert post_response.status_code == 200
    assert get_2_response.status_code == 200

    assert len(get_1_response.json) == 0
    assert len(get_2_response.json) == 1

    assert get_2_response.json == expected_get_2_result

@pytest.mark.parametrize(
        'date_from,     date_to,        origin_code,    destination_code,   price,                                  expected_error',
    [
        ('2021-01-0',   '2021-01-03',   'CNGGZ',        'NOSVG',            1000,                                   DATE_FROM_INVALID_FORMAT),
        ('2021-01-01',  '2021-01-0',    'CNGGZ',        'NOSVG',            1000,                                   DATE_TO_INVALID_FORMAT),
        ('2021-01-03',  '2021-01-01',   'CNGGZ',        'NOSVG',            1000,                                   DATE_FROM_AFTER_DATE_TO),
        ('2021-01-01',  '2021-01-03',   None,           'NOSVG',            1000,                                   ORIGIN_NULL),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        None,               1000,                                   DESTINATION_NULL),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        'CNGGZ',            1000,                                   ORIGIN_AND_DESTINATION_SAME),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        'NOSVG',            None,                                   PRICE_NULL),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        'NOSVG',            {"amount": 1000, "currency": "SEK"},    PRICE_UNKNOWN_CURRENCY),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        'NOSVG',            "asdf1234",                             PRICE_INVALID),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        'NOSVG',            -1000,                                  PRICE_NEGATIVE),
        ('2021-01-01',  '2021-01-03',   'CNGGZ',        'NOSVG',            {"amount": -100, "currency": "NOK"},    PRICE_NEGATIVE)
    ]
)
@httpretty.activate
def test_add_rate_given_invalid_params_expect_error(app, rest_client, date_from, date_to, origin_code, destination_code, price, expected_error):
    api_key = os.environ["OPEN_EX_RATES_API_KEY"]
    open_ex_api_url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    latest_ex_rates = {
        "rates": {
            "NOK": 0.1
        }
    }
    httpretty.register_uri(httpretty.GET, open_ex_api_url, body=json.dumps(latest_ex_rates))

    with app.test_request_context():
        url = url_for('rates_bp.add_rate')
        body = {
            "date_from": date_from,
            "date_to": date_to,
            "origin_code": origin_code,
            "destination_code": destination_code,
            "price": price
        }

        response = rest_client.post(url, json=body)

    assert response.json == expected_error
