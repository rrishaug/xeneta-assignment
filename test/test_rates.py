import pytest

from flask import url_for

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