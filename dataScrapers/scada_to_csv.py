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


files = os.listdir('./scada')

files = sorted(files)
# files = ['20211202_SystemRealizationSCADA_01.xls']
gen_df = pd.DataFrame()
data = []

for f in files:
    try:
        df = pd.read_excel(f'./scada/{f}', skiprows=3, sheet_name='System_Production')
        df = df.transpose()

        df = df[df.columns.values[10:23]]

        df.columns = df.iloc[1]
        df = df.iloc[2:-1]
        date = f.split('_')[0]
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        date = datetime.datetime(year,month,day)


        df.index = [date + datetime.timedelta(hours=x) for x in range(24)]


        gen_df = gen_df.append(df)
    except:
        df = pd.read_excel(f'./scada/{f}', skiprows=3, sheet_name='System_Production')
        df = df.transpose()

        df = df[df.columns.values[15:28]]

        df.columns = df.iloc[1]
        df = df.iloc[2:-1]

        date = f.split('_')[0]
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])
        date = datetime.datetime(year, month, day)

        df.index = [date + datetime.timedelta(hours=x) for x in range(24)]

        gen_df = gen_df.append(df)
#
# gen_df = pd.DataFrame.from_records(data)
# gen_df.columns = ['Date', 'Values']
# gen_df = gen_df.set_index('Date')
gen_df.to_csv('scada.csv')
