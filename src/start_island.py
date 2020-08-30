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

kb_start = types.ReplyKeyboardMarkup(True, False)
kb_directions = types.ReplyKeyboardMarkup(True, False)

kb_hide = types.ReplyKeyboardRemove()

kb_start.row('Осмотреться 👀')
kb_directions.row('🏘 Поселение', '🌳 Лес', '🏝 Пляж')

def registration(message):
    CHAT = message.chat.id
    PLAYER = []
    STATUS = []
    EQUIPMENT = []

    cursor.execute('select * from players where id=?', [message.from_user.id])
    player = cursor.fetchone()
    if player == None:
        PLAYER.append(message.from_user.id)
        STATUS.append(message.from_user.id)
        EQUIPMENT.append(message.from_user.id)

        if message.from_user.username != None:
            bot.send_message(CHAT, 'Привет, %s' % message.from_user.username, reply_markup=kb_start)
            PLAYER.append(message.from_user.username)
            STATUS.append(message.from_user.username)
        else:
            bot.send_message(CHAT, 'Привет, %s' % message.from_user.first_name, reply_markup=kb_start)
            PLAYER.append(message.from_user.first_name)
            STATUS.append(message.from_user.first_name)

        player_class = random.randint(0, 5)
        PLAYER.append(player_class)
        PLAYER.append(0)
        player_race = random.randint(0, 3)
        PLAYER.append(player_race)

        for i in range(2, 8):
            STATUS.append(0)
        for i in range(1, 4):
            EQUIPMENT.append(0)

        try:
            cursor.execute('insert into players values (?,?,?,?,?)', PLAYER)
            conn.commit()
            cursor.execute('insert into status values (?,?,?,?,?,?,?,?)', STATUS)
            conn.commit()
            cursor.execute('insert into equipment values (?,?,?,?)', EQUIPMENT)
            conn.commit()
        except Exception as e:
            print(e)

    else:
        bot.send_message(CHAT, 'Привет еще раз')

def look_around(message):
    bot.send_message(message.chat.id, 'Ты осмотрелся и увидел 3 направления', reply_markup=kb_directions)