from . database import database

from datetime import date, timedelta

FIND_AVG_PRICE_SQL = """
    select p.day as day, cast(round(avg(p.price)) as int) as avg_price, count(p.price) as price_count
    from prices p
    where p.day between :fromDate and :toDate
      and p.orig_code in (
        select prt.code
        from ports prt
          join regions reg on prt.parent_slug = reg.slug
        where prt.code = :origin
          or prt.parent_slug in (select child_slug from region_hierarchy where parent_slug = :origin)
    )
      and p.dest_code in (
        select prt.code
        from ports prt
          join regions reg on prt.parent_slug = reg.slug
        where prt.code = :destination
          or prt.parent_slug in (select child_slug from region_hierarchy where parent_slug = :destination)
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

INSERT_PRICE = """
    insert into prices(orig_code, dest_code, day, price)
    values (:origCode, :destCode, :day, :price)
"""

INSERT_PRICE_WITH_DATE_RANGE = """
    insert into prices(orig_code, dest_code, day, price)
    select :origCode, :destCode, day::date, :price
    from generate_series(
      :dateFrom,
      :dateTo,
      '1 day'::interval
    ) day;
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

def insert_prices_loop(date_from: date, date_to: date, orig_code: str, dest_code: str, price: int):
    date = date_from

    while date <= date_to:
        params = {
            'origCode': orig_code,
            'destCode': dest_code,
            'day': date,
            'price': price
        }

        rows = database.session.execute(INSERT_PRICE, params)
        date = date + timedelta(days=1)

    database.session.commit()


def insert_prices(date_from: date, date_to: date, orig_code: str, dest_code: str, price: int):
    '''
    Depending on size of date range its probably easier to let postgres create the date range
    For small date ranges the looping function above seems slightly faster from some quick testing of the rest calls
    For larger batches allowing postgres to create the range seems significantly faster
    Could use both and add some logic to decide which to select based on size of the date range
    '''

    params = {
        'origCode': orig_code,
        'destCode': dest_code,
        'dateFrom': date_from,
        'dateTo': date_to,
        'price': price
    }
    
    database.session.execute(INSERT_PRICE_WITH_DATE_RANGE, params)
    database.session.commit()

    return find_avg_prices(date_from, date_to, orig_code, dest_code)
