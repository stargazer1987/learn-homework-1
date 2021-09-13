"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import ephem
import logging
import warnings
import settings

from datetime import datetime



from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

warnings.filterwarnings("ignore", category=DeprecationWarning) 
dt_now = datetime.now()

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def planet_search(update, context):
    text = 'Вызван /planet'
    update.message.reply_text(text)
    user_text = update.message.text.split()
    if len(user_text) == 1:
      update.message.reply_text("Введите планету после /planet")
    else:
      user_text = user_text[1]
      try:
        planet = getattr(ephem, user_text.lower().capitalize())
      except:
        update.message.reply_text("Введите существующую планету на английском после /planet")
      position = planet(dt_now)
      const = ephem.constellation(position)
      update.message.reply_text(const)

def word_count(update, context):
    text = 'Вызван /wordcount'
    update.message.reply_text(text)
    user_text = update.message.text.split()
    if len(user_text) == 1:
      update.message.reply_text("Введите слова после /wordcount")
    else:
        user_text = user_text[1:]
        count = 0
        for word in user_text:
            for letter in word:
                if letter in '.,!?<>;:-+@#$%:^&*()[]}{`~№"1234567890':
                  word = word.replace(letter, '')
            word = word.strip()
            if word != '':
                count += 1
    update.message.reply_text(f"{count} слов(а)")

def full_moon(update, context):
    text = 'Вызван /next_full_moon'
    update.message.reply_text(text)
    user_text = update.message.text.split()
    if len(user_text) == 1:
        update.message.reply_text("Введите дату после /next_full_moon")
    elif len(user_text) > 2:
        update.message.reply_text("Введите дату в формате yyyy-mm-dd после /next_full_moon")
    else:
        user_text = user_text[1]
        try:
            date = ephem.next_full_moon(user_text)
            print(date)
            update.message.reply_text(f'Ближайшее полнолуние будет {date}')
        except:
            update.message.reply_text('Дату не удается распозать, введите еще раз')

# Функция работает локально, но не в Телеграм-боте, дописывается
"""
def play_cities(update, context):
    text = 'Вызван /cities'
    update.message.reply_text(text)
    cities = ['Андреанаполь','Абакан','Москва','Петрозаводск','Ростов','Новгород','Калуга','Пермь','Ялта',
    'Воскресенск','Киев','Вологда','Волгоград','Тверь','Тула','Тамбов','Пенза','Симферополь','Хабаровск',
    'Липецк']
    PLAY_GAME = True
    while PLAY_GAME:
        update.message.reply_text("Введите город")
        user_city = update.message.text.split()
        if len(user_city) == 1 or len(user_city) > 2:
            update.message.reply_text("Введите город - одно слово")
            break
        else:
            user_city = user_city[1].lower()
            for letter in user_city:
                if letter in '.,!?<>;:-+@#$%:^&*()[]}{`~№"1234567890':
                    user_city = user_city.replace(letter, '')
            user_city = user_city.strip().capitalize()
            if user_city in cities:
                current_letter = user_city[-1]
                if current_letter in ' йьъы':
                    current_letter = user_city[-2]
                cities.remove(user_city)
                if len(cities) == 0:
                    update.message.reply_text('Список городов пуст. Пользователь выиграл')
                    PLAY_GAME = False
                    break
                for city in cities:
                    if current_letter == city[0].lower():
                        update.message.reply_text(city) # Ответ бота
                        cities.remove(city)
                        if len(cities) == 0:
                            update.message.reply_text('Список городов пуст. Компьютер выиграл')
                            PLAY_GAME = False
                            break
                        break
                else:
                    update.message.reply_text('Подхоящих городов в списке не отсталось. пользователь выиграл')
                    PLAY_GAME = False
            else:
                update.message.reply_text("Такого города не обнаружено, попробуйте другой")
"""
        


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_search))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("next_full_moon", full_moon))
    #dp.add_handler(CommandHandler("cities", play_cities))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
