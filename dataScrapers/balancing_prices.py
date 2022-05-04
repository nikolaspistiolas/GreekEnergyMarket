import requests
import requests
import datetime
import pandas as pd
# https://www.admie.gr/sites/default/files/attached-files/type-file/2021/09/20210823_IMBABE_01.xlsx
# https://www.admie.gr/sites/default/files/attached-files/type-file/2021/09/20210823_IMBABE_01.xlsx
# https://www.admie.gr/sites/default/files/attached-files/type-file/2021/9/20210823_IMBABE_01.xlsx
start = datetime.datetime(2021,8,2)
for i in range(int(262/7)):
    day = str(start.day)
    if start.day < 10:
        day = '0' + day
    month = str(start.month)
    if start.month < 10:
        month = '0' + month
    url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start.year}/{month}/{start.year}{month}{day}_IMBABE_01.xlsx'

    print(url)
    file_name = 'balancing_data_prices/' + url.split('/')[-1]

    content = requests.get(url).content

    open(file_name,'wb').write(content)

    try:
        pd.read_excel(file_name)
    except:
        print('IN EXCEPT')
        start2 = start + datetime.timedelta(days=11)
        month2 = start2.month
        if month2 < 10:
            month2 = '0' + str(month2)

        url2 = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start2.year}/{month2}/{start.year}{month}{day}_IMBABE_01.xlsx'
        file_name = 'balancing_data_prices/' + url2.split('/')[-1]
        content = requests.get(url2).content
        open(file_name, 'wb').write(content)
        print(url2)
        pd.read_excel(file_name)
    start += datetime.timedelta(days=7)
