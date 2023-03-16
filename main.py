import json
import logging
import os.path

import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

from best_heroes import heroes, hero_info_bot

if not os.path.exists('logs/'):
    os.mkdir('logs')

with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

TOKEN = data.get('TOKEN')

logging.basicConfig(filename='logs/bot.log', level=logging.INFO, encoding='utf-8')

heroes_list = []
hero_info_bot = ''.join(hero_info_bot)
menu_message = "Choose what do u want: \n\n" \
               "1. See who in the top by winrate now🔝\n" \
               "2. Get a itembuild of some hero👊\n" \
               "3. Look at the trends📈\n" \
               "4. Check a pickrate of some hero↗"


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start", "menu"])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        btn1 = types.KeyboardButton("1")
        # btn2 = types.KeyboardButton("Top heroes info")
        btn2 = types.KeyboardButton('2')
        btn3 = types.KeyboardButton('3')
        btn4 = types.KeyboardButton('4')
        btn5 = types.KeyboardButton('Main menu')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        if message.text == '/start':
            bot.send_message(message.chat.id, "Hello friend! I am simple, not official dotabuff bot. \n"
                                              "With me u can get some info from Dotabuff.com! \n"
                                              "Choose what do u want: \n\n"
                                              "1. See who in the top by winrate now🔝\n"
                                              "2. Get a itembuild of some hero👊\n"
                                              "3. Look at the trends📈\n"
                                              "4. Check a pickrate of some hero↗".format(message.from_user),
                             reply_markup=markup)
        elif message.text == '/menu':
            bot.send_message(message.chat.id, menu_message.format(message.from_user), reply_markup=markup)

    def itembuild(message):
        if message.text == 'Main menu':
            bot.send_message(message.chat.id, menu_message)
        else:
            logging.info(message)
            item_build = ''
            hero = message.text.split()
            hero = '-'.join(hero).lower()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
            }
            url = f'https://ru.dotabuff.com/heroes/{hero.lower()}'
            try:
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
                    item_build += f'{item_name}: {timing}\n'
                item_build = f'{hero.capitalize()}:\n' + item_build
                bot.send_message(message.chat.id, item_build)
            except Exception as e:
                logging.error(f'ITEMBUILD FUNC ERROR\n{e}')
                bot.send_message(message.chat.id, 'Check out ur hero name!!')

    def trends(message):
        if message.text == 'Main menu':
            bot.send_message(message.chat.id, menu_message)
        else:
            logging.info(message)
            count = int(message.text)
            messagee = ''
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
            }
            try:
                r = requests.get(url='https://www.dotabuff.com/heroes/trends', headers=headers)
                soup = BeautifulSoup(r.text, 'lxml')
                cards = soup.find('table', class_='sortable').find('tbody').find_all('tr')[:count]
                for card in cards:
                    hero_name = str(card.find('td', class_='cell-centered').get('data-value'))
                    previous_percentage = round(float(card.find_all('td')[1].get('data-value')), 2)
                    current_percentage = round(float(card.find_all('td')[2].get('data-value')), 2)
                    change = round(current_percentage - previous_percentage, 2)
                    messagee += f'Hero name: {hero_name}\nPrevious_percentage: {previous_percentage}\nCurrent_percentage: {current_percentage}\nChange: {change}\n\n'
                bot.send_message(message.chat.id, f'Here u go!\n{messagee}')
            except Exception as e:
                logging.error(f'TRENDS FUNC ERROR\n{e}')
                bot.send_message(message.chat.id,
                                 f'Oooopppss... Ur number is toooooo big, i cant send u THIS count of information😣')

    def pickrate_and_winrate(message):
        if message.text == 'Main menu':
            bot.send_message(message.chat.id, menu_message)
        else:
            logging.info(message)
            hero = message.text.split()
            hero = '-'.join(hero)
            j = 1
            headers = {
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
            }
            url = f'https://dotabuff.com/heroes/{hero.lower()}'
            hero_info = []
            try:
                r = requests.get(url=url, headers=headers)

                soup = BeautifulSoup(r.text, 'lxml')
                container = soup.find('div', class_='col-8')
                lines_count = container.find_all('section')[0].find('article').find('table').find('tbody').find_all(
                    'tr')
                for i in lines_count:
                    td_list = i.find_all('td')
                    hero_info.append(td_list[0].text)
                    hero_info.append('Pickrate: ' + td_list[1].text)
                    hero_info.append('Winrate: ' + td_list[2].text)
                    j += 1
                popularity = 'Popularity: ', soup.find('div', class_='header-content-container').find('div',
                                                                                                      class_='header-content-secondary').find(
                    'dl').find('dd').text

                hero_info = '\n'.join(hero_info) + '\n' + ''.join(popularity)
                bot.send_message(message.chat.id, f'Here u go: \n {hero_info}')

            except Exception as e:
                logging.error(f'PICKRATE_AND_WINRATE FUNC ERROR\n{e}')
                bot.send_message(message.chat.id, '[!]Oops... Smth went wrong... Check ur hero name[!]')

    @bot.message_handler(content_types=["text"])
    def hero_info_func(message):
        logging.info(message)

        if message.text == '1':
            for h in heroes:
                hero_name = h.get('Name').split()
                hero_name = '-'.join(hero_name)
                hero_winrate = h.get('Winrate')
                hero_stat = f'{hero_name}: {hero_winrate}'
                heroes_list.append(hero_stat)
            bot.send_message(message.chat.id, ', '.join(heroes_list))
            heroes_list.clear()

        # elif message.text == 'asd':
        #     bot.send_message(message.chat.id, 'Sure my friend!''\n'f' {hero_info_bot}')

        elif message.text == '2':
            msg = bot.send_message(message.chat.id, 'Write down hero name:')
            bot.register_next_step_handler(msg, itembuild)

        elif message.text == '3':
            msg = bot.send_message(message.chat.id, 'How many heroes do u want to see?')
            bot.register_next_step_handler(msg, trends)

        elif message.text == '4':
            msg = bot.send_message(message.chat.id, 'Write down hero name:')
            bot.register_next_step_handler(msg, pickrate_and_winrate)

        elif message.text == 'Main menu':
            bot.send_message(message.chat.id, menu_message)

    bot.infinity_polling()


if __name__ == '__main__':
    telegram_bot(TOKEN)
