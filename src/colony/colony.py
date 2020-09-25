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

kb_colony_pier = types.ReplyKeyboardMarkup(True, False)

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

kb_colony_pier.row('Персонаж')
kb_colony_pier.row('🗼 Маяк', '⚒ Кузня', '🍻 Бар')
kb_colony_pier.row('⬅ Вернуться на площадь')


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


def colony_center(message):
    global kb_colony_center
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_center', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в центр', reply_markup=kb_colony_center)


def colony_pier(message):
    global kb_colony_pier
    try:
        cursor.execute('update status set location=? where id_player=?', ['colony_pier', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать на причал', reply_markup=kb_colony_pier)
