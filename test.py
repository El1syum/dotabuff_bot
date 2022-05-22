import requests
from bs4 import BeautifulSoup


item_build = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
url = f'https://ru.dotabuff.com/heroes/meepo'
r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
items = soup.find('div', class_='top-right').find('div', class_='kv').find_all('div', class_='match-item-with-time')
for item in items:
    item_name = item.find('a').get('href').split('/')[-1]
    try:
        timing = item.find('div', class_='time').text
    except:
        timing = 'not given'
    item_build += f'{item_name}: {timing}\n'
item_build = 'dasdas\n'+item_build
print(item_build)