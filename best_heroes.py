import requests
from bs4 import BeautifulSoup

heroes = []
item_list = []
hero_info_bot = []


def list_of_heroes(url):
    global heroes
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    ten_heroes = soup.find('table', class_='sortable').find('tbody').find_all('tr')[:5]
    for hero in ten_heroes:
        name = hero.find_all('td')[1].text
        winrate = hero.find_all('td')[2].text
        pickrate = hero.find_all('td')[3].text
        kda = hero.find_all('td')[4].text
        heroes += [
            {
                'Name': name,
                'Winrate': winrate,
                'Pickrate': pickrate,
                'KDA': kda
            }
        ]


def get_hero_info():
    global hero_info_bot, item_list
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }
    for h in heroes:
        hero = h.get('Name').split()
        hero = '-'.join(hero)
        url = f'https://ru.dotabuff.com/heroes/{hero.lower()}'
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.find('div', class_='top-right').find('div', class_='kv').find_all('div',
                                                                                       class_='match-item-with-time')
        for item in items:
            item_name = item.find('a').get('href').split('/')[-1]
            try:
                timing = item.find('div', class_='time').text
            except:
                timing = 'not given'
            item_list += [hero, f'{item_name}: {timing}']
        # item_list += ['|']

    for first, second in zip(item_list, item_list[1:]):
        if first in hero_info_bot:
            if second in hero_info_bot:
                continue
        else:
            hero_info_bot.append(first)
        if second in hero_info_bot:
            continue
        else:
            hero_info_bot.append(second)
    for hero in range(len(hero_info_bot) * 2):
        if hero_info_bot[hero] != '\n':
            hero_info_bot.insert(hero + 1, '\n')
        else:
            continue


list_of_heroes(url='https://ru.dotabuff.com/heroes/winning')
get_hero_info()
