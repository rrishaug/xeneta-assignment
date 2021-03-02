from . database import database

from datetime import date

FIND_AVG_PRICE_SQL = """
    select p.day as day, cast(round(avg(p.price)) as int) as avg_price, count(p.price) as price_count 
    from prices p 
    where p.day between :fromDate and :toDate 
    and p.orig_code in (
        select prt.code 
        from ports prt 
        join regions reg on prt.parent_slug = reg.slug 
        where prt.code = :origin 
        or prt.parent_slug = :origin 
        or reg.parent_slug = :origin 
    ) 
    and p.dest_code in (
        select prt.code 
        from ports prt 
        join regions reg on prt.parent_slug = reg.slug 
        where prt.code = :destination 
        or prt.parent_slug = :destination 
        or reg.parent_slug = :destination 
    ) 
    group by day 
    order by day
"""

PRICE_COUNT_THRESHOLD_VALUE = 3

FIND_AVG_PRICE_NULL_SQL = f"""
select 
  apc.day as day, 
  case 
    when apc.price_count >= :countThresholdValue then apc.avg_price 
    else null 
  end as avg_price 
from (
  {FIND_AVG_PRICE_SQL}
) as apc 
"""

def map_avg_price_row(row):
    return {
        "day": row.day,
        "avg_price": row.avg_price
    }

def find_avg_prices(date_from: date, date_to: date, origin: str, destination:str):
    params = {
        'fromDate': date_from,
        'toDate': date_to,
        'origin': origin,
        'destination': destination
    }

    rows = database.session.execute(FIND_AVG_PRICE_SQL, params)
    return [map_avg_price_row(row) for row in rows]

def find_avg_prices_null(date_from: date, date_to: date, origin: str, destination:str):
    params = {
        'fromDate': date_from,
        'toDate': date_to,
        'origin': origin,
        'destination': destination,
        'countThresholdValue': PRICE_COUNT_THRESHOLD_VALUE
    }

    rows = database.session.execute(FIND_AVG_PRICE_NULL_SQL, params)
    return [map_avg_price_row(row) for row in rows]