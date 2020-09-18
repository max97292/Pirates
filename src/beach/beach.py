# -*- coding: utf-8 -*-
import random
import time

import telebot
import sqlite3

from telebot import types
from src.config import TOKEN
from src.enemys.enemys import select_enemys

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()


def beach_start(message):
    global kb_beach
    kb_beach = types.ReplyKeyboardMarkup(True, False)

    try:
        cursor.execute('select * from players where id=?', [message.from_user.id])
        player = cursor.fetchone()
    except Exception as e:
        print(e)

    if player[4] == 1:
        kb_beach.row('🚶🏻 Идти прямо', '🌳 Свернуть в лес')
    if player[4] == 2:
        kb_beach.row('🚶🏼 Идти прямо', '🌳 Свернуть в лес')
    if player[4] == 3:
        kb_beach.row('🚶🏿 Идти прямо', '🌳 Свернуть в лес')

    kb_beach.row('⬅ Назад')

    try:
        cursor.execute('update status set location=? where id_player=?', ['beach', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Добро пожаловать на пляж', reply_markup=kb_beach)


def beach_forward(message):
    kb_beach = types.ReplyKeyboardMarkup(True, False)

    try:
        cursor.execute('select * from players where id=?', [message.from_user.id])
        player = cursor.fetchone()
    except Exception as e:
        print(e)

    if player[4] == 1:
        kb_beach.row('🚶🏼 Идти прямо', '🌳 Свернуть в лес')
    if player[4] == 2:
        kb_beach.row('🚶🏻 Идти прямо', '🌳 Свернуть в лес')
    if player[4] == 3:
        kb_beach.row('🚶🏿 Идти прямо', '🌳 Свернуть в лес')

    kb_beach.row('⬅ Назад')

    try:
        cursor.execute('update status set location=? where id_player=?', ['beach', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Ты прошелся дальше по пляжу', reply_markup=kb_beach)

    chance = random.uniform(0, 1)
    if chance < 0.5:
        select_enemys(message)
