import requests
import requests
import datetime
import pandas as pd

start = datetime.datetime(2021,8,15)
for i in range(260):
    day = str(start.day)
    if start.day < 10:
        day = '0' + day
    month = str(start.month)
    if start.month < 10:
        month = '0' + month
    url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start.year}/{month}/{start.year}{month}{day}_ISP1Requirements_01.xlsx'
    start += datetime.timedelta(days=1)
    print(url)
    file_name = 'balancing_data_requirements/' + url.split('/')[-1]

    content = requests.get(url).content
    open(file_name,'wb').write(content)
    try:
        pd.read_excel(file_name)
    except:
        start