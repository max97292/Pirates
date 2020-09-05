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


def person_show_characteristics(message):
    try:
        cursor.execute('select * from players where id=?', [message.from_user.id])
        player = cursor.fetchone()
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        cursor.execute('select name from player_class')
        classes = cursor.fetchall()
    except Exception as e:
        print(e)

    if player[2] == 1:
        player_class = classes[0][0]
    if player[2] == 2:
        player_class = classes[1][0]
    if player[2] == 3:
        player_class = classes[2][0]
    if player[2] == 4:
        player_class = classes[3][0]

    if player[4] == 1:
        player_race = '🧔🏼'
    if player[4] == 2:
        player_race = '🧔'
    if player[4] == 3:
        player_race = '🧔🏿'

    bot.send_message(message.chat.id, '🏴‍☠ Пират %s\n'
                                      'Класс %s\n'
                                      'Специализация %s\n'
                                      '\n'
                                      'Имя: %s\n'
                                      'Уровень: %d\n'
                                      '🕛 Опыт: (%d/%d)\n'
                                      '\n'
                                      '❤ Здоровье: %d/%d\n'
                                      '🔪 Сила атаки: %d/%d\n'
                                      '🛡 Защита: %d/%d\n'
                                      '🥄 Голод: %d/%d\n'
                                      '\n'
                                      'Экипировка:\n'
                                      '' % (player_race,
                                            str(player_class),
                                            player[3],
                                            status[1],
                                            status[2],
                                            status[3], status[3],
                                            status[4], status[4],
                                            status[5], status[5],
                                            status[6], status[6],
                                            status[7], status[7]))
