import requests
import pandas as pd
import datetime

# https://www.admie.gr/sites/default/files/attached-files/type-file/2022/05/20220510_ISP1UnitAvailabilities_02.xlsx

start = datetime.datetime(2021,8,2)
<<<<<<< HEAD
for i in range(int(262/7)):
=======
for i in range(320):
>>>>>>> c0d0f1ddbc9bb259911536966e005bc6af7c21f7
    day = str(start.day)
    if start.day < 10:
        day = '0' + day
    month = str(start.month)
    if start.month < 10:
        month = '0' + month
    url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start.year}/{month}/{start.year}{month}{day}_ISP1UnitAvailabilities_02.xlsx'
    print(i, url)
    file_name = 'unit_availabilities/' + url.split('/')[-1]
    content = requests.get(url).content
    open(file_name, 'wb').write(content)
    try:
        pd.read_excel(file_name)

        print("FFFFFFFFF")

    except:
        print('IN EXCEPT')
        start2 = start - datetime.timedelta(days=1)
        month2 = start2.month
        if month2 < 10:
            month2 = '0' + str(month2)
        url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start2.year}/{month2}/{start.year}{month}{day}_ISP1UnitAvailabilities_02.xlsx'
        print(url)
        file_name = 'unit_availabilities/' + url.split('/')[-1]
        content = requests.get(url).content
        open(file_name, 'wb').write(content)
    start += datetime.timedelta(days=1)
