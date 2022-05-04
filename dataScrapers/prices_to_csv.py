import pandas as pd
import os
import datetime
import pytz


def get_dts(start_date, end_date, delta):
    print(start_date.month)
    if is_dst_change(start_date.replace(tzinfo=None), 'Europe/Athens'):
        if start_date.month == 3:
            dts = [dt for dt in datetime_range(start_date, end_date, delta, skip=True)]

        elif start_date.month == 10:
            print('HERE')
            dts = [dt for dt in datetime_range(start_date, end_date, delta, add_twice=True)]
    else:
        dts = [dt for dt in datetime_range(start_date, end_date, delta)]
    return dts


def datetime_range(start, end, delta, hour=2, skip=False, add_twice=False):
    current = start

    while current < end:
        if skip:
            if current.hour != hour:
                yield current.replace(tzinfo=None)
        elif add_twice:
            if current.hour == hour:
                yield current.replace(tzinfo=None)
                yield current.replace(tzinfo=None)
            else:
                yield current.replace(tzinfo=None)
        else:
            yield current.replace(tzinfo=None)
        current += delta


def is_dst_change(day: datetime.datetime, timezone):
    # Override time to midnight
    day = day.replace(hour=0, minute=0, second=0, microsecond=0)
    tz = pytz.timezone(timezone)
    return tz.utcoffset(day + datetime.timedelta(days=1)) != tz.utcoffset(day)


files = os.listdir('./balancing_data_prices')
files = sorted(files)[1:]

gen_df = pd.DataFrame()

for f in files:
    df = pd.read_excel(f'./balancing_data_prices/{f}')
    df['STARTDATE'] = pd.to_datetime(df['STARTDATE'])
    df.index = df['STARTDATE']
    df = df.drop(['STARTDATE','ENDDATE','Balancing Energy IDEV (MWh)','Balancing Energy UDEV (MWh)'], axis=1)
    start = df.index[0]
    end = df.index[-1]
    while start < end:
        dates = get_dts(start, start + datetime.timedelta(days=1), datetime.timedelta(minutes=15))
        tmp_df = df.loc[(df.index < start + datetime.timedelta(days=1))]
        df = df.loc[(df.index >= start + datetime.timedelta(days=1))]
        tmp_df.index = dates
        gen_df = gen_df.append(tmp_df)
        start += datetime.timedelta(days=1)


gen_df.to_csv('BalancePrices.csv')