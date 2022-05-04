import pandas as pd
import os
import datetime

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


files = os.listdir('/Users/nikolaspistiolas/PycharmProjects/GreekEnergyMarket/dataScrapers/balancing_data_requirements')

files = sorted(files)[1:]

df_gen = pd.DataFrame()

for f in files:
    print(f)

    date = f.split('_')[0]
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    df = pd.read_excel(f'./balancing_data_requirements/{f}', header=1)
    df = df.transpose()
    df = df[[1,6,26,41]]
    df = df.iloc[2:-1]
    df.index = f'{year} {month} {day} ' + df.index
    df.index = pd.to_datetime(df.index)
    start = df.index[0]
    end = df.index[-1] + datetime.timedelta(minutes=30)
    dates = get_dts(start,end, datetime.timedelta(minutes=30))
    df.index = dates
    df_gen = df_gen.append(df)


print(df_gen)
df_gen.columns = ['RES','Load', 'Mandatory Hydro', 'Total FRR']
df_gen.to_csv('_ISP1Requirements.csv')
# print(files)
# df = pd.read_excel('./balancing_data_requirements/20210815_ISP1Requirements_01.xlsx', header=1)
# df = df.transpose()
# df = df.iloc[1:]

# 1 - RES, 6 - Load, 26 - Mandatory Hydro, 41 - Total FRR
