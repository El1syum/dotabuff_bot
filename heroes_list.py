# import json
# import math
# from bs4 import BeautifulSoup
# import requests
#
#
# def main(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
#     }
#     hero_stats = []
#     mid_win_list = []
#     r = requests.get(url=url, headers=headers)
#
#     soup = BeautifulSoup(r.text, 'lxml')
#     all_heroes = soup.find('table', class_='sortable no-arrows r-tab-enabled').find('tbody').find_all('tr')
#     for hero in all_heroes[0:2]:
#         name_hero = hero.find_all('td')[1].text
#         middle_winrate = hero.find_all('td', class_='r-group-1')[-1].text
#         off_winrate = hero.find_all('td', class_='r-group-2')[-1].text
#         safe_winrate = hero.find_all('td', class_='r-group-3')[-1].text
#         jungle_winrate = hero.find_all('td', class_='r-group-4')[-1].text
#         hero_stats += [
#             {
#             'Hero name': name_hero,
#             'Middle winrate': middle_winrate,
#             'Off winrate': off_winrate,
#             'Safe_winrate': safe_winrate,
#             'Jungle winrate': jungle_winrate
#             }
#         ]
#
#     for hero in hero_stats:
#         mid_win_list += [hero['Middle winrate']]
#
#     mid_win = max(mid_win_list)
#     best_mid = soup.soup.find('table', class_='sortable no-arrows r-tab-enabled').find('tbody').find_all('tr').find(text=mid_win)
#     print(best_mid)
#
#     with open('hero_stats.json', 'w', encoding='utf-8') as file:
#         json.dump(hero_stats, file, indent=4, ensure_ascii=False)
#
# if __name__ == '__main__':
#     main(url='https://ru.dotabuff.com/heroes/meta?view=played&metric=lane')
