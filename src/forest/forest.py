# -*- coding: utf-8 -*-
import random
import time

import telebot
import sqlite3

from telebot import types
from src.config import TOKEN
from src.transition import transition

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()


def forest_start(message):
    kb_forest = types.ReplyKeyboardMarkup(True, False)
    kb_forest.row('⬆ Двигаться дальше')
    kb_forest.row('⬅ Назад')

    try:
        cursor.execute('update status set location=? where id_player=?', ['forest', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать в лес', reply_markup=kb_forest)


def forest_forward(message):
    kb_forest = types.ReplyKeyboardMarkup(True, False)
    kb_forest.row('⬆ Двигаться дальше')

    try:
        cursor.execute('select location from status where id_player=?', [message.from_user.id])
        location = cursor.fetchone()
        location = location[0]
        if location == 'forest':
            location = 'forest1'
        elif location == 'forest1':
            location = 'forest2'
        elif location == 'forest2':
            location = 'forest3'
        elif location == 'forest3':
            location = 'forest_big'
        transition(message, 0)
        cursor.execute('update status set location=? where id_player=?', [location, message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    if location != 'forest_big':
        kb_forest.row('⬅ Назад')
        bot.send_message(message.chat.id, 'Ты ушел глубже в лес', reply_markup=kb_forest)
    else:
        cave_chance = random.uniform(0, 1)
        if cave_chance > 0.8:
            kb_forest.row('🦴 Пещера')
            kb_forest.row('⬅ Назад')
        else:
            kb_forest.row('⬅ Назад')
        bot.send_message(message.chat.id, 'Добро пожаловать в большой лес', reply_markup=kb_forest)


def forest_backward(message):
    kb_forest = types.ReplyKeyboardMarkup(True, False)
    kb_forest.row('⬆ Двигаться дальше')

    try:
        cursor.execute('select location from status where id_player=?', [message.from_user.id])
        location = cursor.fetchone()
        location = location[0]
        if location == 'forest1':
            location = 'forest'
        elif location == 'forest2':
            location = 'forest1'
        elif location == 'forest3':
            location = 'forest2'
        elif location == 'forest_big':
            location = 'forest3'
        transition(message, 0)
        cursor.execute('update status set location=? where id_player=?', [location, message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    if location != 'forest_big':
        kb_forest.row('⬅ Назад')
        bot.send_message(message.chat.id, 'Ты вернулся обратно в лес', reply_markup=kb_forest)
    else:
        cave_chance = random.uniform(0, 1)
        if cave_chance > 0.8:
            kb_forest.row('🦴 Пещера')
            kb_forest.row('⬅ Назад')
        else:
            kb_forest.row('⬅ Назад')
        bot.send_message(message.chat.id, 'Добро пожаловать в большой лес', reply_markup=kb_forest)
