import requests
import requests
import datetime

# https://www.admie.gr/sites/default/files/attached-files/type-file/2022/04/20220307_IMBABE_02.xlsx
start = datetime.datetime(2021,8,16)
for i in range(int(262/7)):
    day = str(start.day)
    if start.day < 10:
        day = '0' + day
    month = str(start.month)
    if start.month < 10:
        month = '0' + month
    url = f'https://www.admie.gr/sites/default/files/attached-files/type-file/{start.year}/{month}/{start.year}{month}{day}_IMBABE_02.xlsx'
    start += datetime.timedelta(days=7)
    print(url)
    file_name = 'balancing_data_prices/' + url.split('/')[-1]

    content = requests.get(url).content
    open(file_name,'wb').write(content)

