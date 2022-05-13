# https://www.admie.gr/sites/default/files/attached-files/type-file/2022/04/20220427_SystemRealizationSCADA_01.xls
import datetime
import requests
import pandas as pd

start = datetime.datetime(2021,8,15)
for i in range(290):
    day = str(start.day)
    if start.day < 10:
        day = '0' + day
    month = str(start.month)
    if start.month < 10:
        month = '0' + month
    url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start.year}/{month}/{start.year}{month}{day}_SystemRealizationSCADA_01.xls'
    print(url)
    file_name = 'scada/' + url.split('/')[-1]
    content = requests.get(url).content
    open(file_name,'wb').write(content)

    try:
        pd.read_excel(file_name)
    except:

        start2 = start + datetime.timedelta(days=1)
        month2 = start2.month
        if month2 < 10:
            month2 = '0' + str(month2)
        url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start2.year}/{month2}/{start.year}{month}{day}_SystemRealizationSCADA_01.xls'
        print('IN EXCEPT', url)
        file_name = 'scada/' + url.split('/')[-1]
        content = requests.get(url).content
        open(file_name, 'wb').write(content)
        pd.read_excel(file_name)
    start += datetime.timedelta(days=1)
