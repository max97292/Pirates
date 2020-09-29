# -*- coding: utf-8 -*-
import random
import time

import telebot
import sqlite3

from telebot import types
from src.config import TOKEN

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()

kb_colony = types.ReplyKeyboardMarkup(True, False)

kb_colony_edge = types.ReplyKeyboardMarkup(True, False)

kb_colony_edge_antiques = types.ReplyKeyboardMarkup(True, False)

kb_colony_edge_wicked = types.ReplyKeyboardMarkup(True, False)
kb_colony_edge_wicked_first = types.ReplyKeyboardMarkup(True, False)

kb_colony_edge_herbal_shop = types.ReplyKeyboardMarkup(True, False)
kb_colony_edge_herbal_shop_potion = types.ReplyKeyboardMarkup(True, False)

kb_colony_center = types.ReplyKeyboardMarkup(True, False)

kb_colony_center_hall = types.ReplyKeyboardMarkup(True, False)

kb_colony_center_market = types.ReplyKeyboardMarkup(True, False)

kb_colony_center_tavern = types.ReplyKeyboardMarkup(True, False)

kb_colony_pier = types.ReplyKeyboardMarkup(True, False)

kb_colony_pier_lighthouse_first = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier_lighthouse = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier_lighthouse_end = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier_forge_work = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier_forge = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier_bar = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier_bar_end = types.ReplyKeyboardMarkup(True, False)

kb_colony.row('Персонаж')
kb_colony.row('🏠 Окраина', '🏙 Центр', '⚓ Причал')
kb_colony.row('⬅ Назад')

kb_colony_edge.row('Персонаж')
kb_colony_edge.row('🏺 Магазин антиквариата', '🏚 Злачный переулок', '🌿 Лавка травника')
kb_colony_edge.row('⬅ Вернуться на площадь')

kb_colony_edge_antiques.row('🏮 Поддержать проект', '🧧 Смена документов', '📍 Сброс навыков')
kb_colony_edge_antiques.row('🎈 Зелье воскрешения', '🧲 Амулет удачи', '📕Карта сокровищ')
kb_colony_edge_antiques.row('⬅ Назад')

kb_colony_edge_wicked_first.row('🚬 Есть ли какое дельце?')
kb_colony_edge_wicked_first.row('⬅ Назад')
kb_colony_edge_wicked.row('🏚 Домой', '🧥 Скупщик краденного')
kb_colony_edge_wicked.row('⬅ Назад')

kb_colony_edge_herbal_shop.row('🍵 Поправить здоровье', '⚱ Полка с зельями', '💐 Спросить, нужна ли помощь')
kb_colony_edge_herbal_shop.row('⬅ Назад')

kb_colony_edge_herbal_shop_potion.row('🏺 Активированный уголь', '🍵 Микстура восстановления', '⚱ Зелье защиты')
kb_colony_edge_herbal_shop_potion.row('🧉 Экспериментальное зелье', '🍶 Зелье исцеления')
kb_colony_edge_herbal_shop_potion.row('⬅ Назад')

kb_colony_center.row('Персонаж')
kb_colony_center.row('⛪ Ратуша', '💰 Рынок', '🍺 Кабак')
kb_colony_center.row('⬅ Вернуться на площадь')

kb_colony_center_hall.row('🧹 Задания', '✉ Передать конверт', '🔘 Получить зарплату')
kb_colony_center_hall.row('⬅ Назад')

kb_colony_center_market.row('⚖ Торговец', '🧺 Барахолка')
kb_colony_center_market.row('⬅ Назад')

kb_colony_center_tavern.row('💬 Поговорить с барменом', '🥃 Выпить', '🥣 Поесть')
kb_colony_center_tavern.row('👩🏾 Уединиться', '🦴 Спросить о работе')
kb_colony_center_tavern.row('⬅ Назад')

kb_colony_pier.row('Персонаж')
kb_colony_pier.row('🗼 Маяк', '⚒ Кузня', '🍻 Бар')
kb_colony_pier.row('⬅ Вернуться на площадь')

kb_colony_pier_lighthouse_first.row('🚪 Войти и осмотреться')
kb_colony_pier_lighthouse.row('📝 Повысить уровень специализации', '💼 Поговорить о работе')
kb_colony_pier_lighthouse_end.row('📝 Повысить уровень специализации', '✨ Получить благословение')
kb_colony_pier_lighthouse.row('⬅ Назад')
kb_colony_pier_lighthouse_first.row('⬅ Назад')
kb_colony_pier_lighthouse_end.row('⬅ Назад')

kb_colony_pier_forge.row('👙 Заказать экипировку', '🔪 Заказать оружие')
kb_colony_pier_forge_work.row('🪓 Рабочий вопрос')
kb_colony_pier_forge_work.row('⬅ Назад')
kb_colony_pier_forge.row('⬅ Назад')

kb_colony_pier_bar.row('🥃 Выпить', '🎲 Сыграть', '🎲 Кости')
kb_colony_pier_bar.row('🃏 Карты', '🎷 Заказать музыку')
kb_colony_pier_bar.row('⬅ Назад')
kb_colony_pier_bar_end.row('⛵ Собрать команду/Наняться в команду')
kb_colony_pier_bar_end.row('⬅ Назад')


def colony_start(message):
    global kb_colony
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в Поселение', reply_markup=kb_colony)


def colony_edge(message):
    global kb_colony_edge
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_edge', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать на окраину', reply_markup=kb_colony_edge)


def colony_edge_antiques(message):
    global kb_colony_edge_antiques
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_edge_antiques', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин антиквара', reply_markup=kb_colony_edge_antiques)


def colony_edge_wicked(message):
    global kb_colony_edge_wicked
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_edge_wicked', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в злачный переулок', reply_markup=kb_colony_edge_wicked_first)


def colony_edge_herbal_shop(message):
    global kb_colony_edge_herbal_shop
    try:
        cursor.execute('update status set location=? where id_player=?',
                       ['colony_edge_herbal_shop', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в лавку травника', reply_markup=kb_colony_edge_herbal_shop)


def colony_edge_herbal_shop_potion(message):
    global kb_colony_edge_herbal_shop_potion
    try:
        cursor.execute('update status set location=? where id_player=?',
                       ['colony_edge_herbal_shop_potion', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Вы посмотрели на полку с зельями',
                     reply_markup=kb_colony_edge_herbal_shop_potion)


def colony_center(message):
    global kb_colony_center
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_center', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в центр', reply_markup=kb_colony_center)


def colony_center_hall(message):
    global kb_colony_center_hall
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_center_hall', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в ратушу', reply_markup=kb_colony_center_hall)


def colony_center_market(message):
    global kb_colony_center_market
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_center_market', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать на рынок', reply_markup=kb_colony_center_market)


def colony_center_tavern(message):
    global kb_colony_center_tavern
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_center_tavern', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в кабак', reply_markup=kb_colony_center_tavern)


def colony_pier(message):
    global kb_colony_pier
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_pier', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать на причал', reply_markup=kb_colony_pier)


def colony_pier_lighthouse(message):
    global kb_colony_pier_lighthouse_first
    try:
        cursor.execute('update status set location=? where id_player=?',
                       ['colony_pier_lighthouse', message.from_user.id])
        conn.commit()
        cursor.execute('select * from players where id=?', [message.from_user.id])
        spec = cursor.fetchone()
        spec = spec[3]
    except Exception as e:
        print(e)
    if spec == 0:
        keyboard = kb_colony_pier_lighthouse_first
    else:
        keyboard = kb_colony_pier_lighthouse
    bot.send_message(message.chat.id, 'Добро пожаловать в маяк', reply_markup=keyboard)

def colony_pier_forge(message):
    global kb_colony_pier_forge
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_pier_forge', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в кузню', reply_markup=kb_colony_pier_forge)


def colony_pier_bar(message):
    global kb_colony_pier_bar
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_pier_bar', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в бар', reply_markup=kb_colony_pier_bar)
