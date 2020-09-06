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

def select_enemys(message):
    ENEMYS = []

    kb_attack = types.ReplyKeyboardMarkup(True, False)

    kb_attack.row('👊🏻 Атаковать', 'Обойти стороной')

    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()

        if status[9] == 'beach':
            cursor.execute('select * from enemy')
            enemys = cursor.fetchall()
            for item in enemys:
                id = str(item[0])
                if id.startswith('2'):
                    ENEMYS.append(item)

        if status[9] == 'colony':
            cursor.execute('select * from enemy')
            enemys = cursor.fetchall()
            for item in enemys:
                id = str(item[0])
                if id.startswith('3'):
                    ENEMYS.append(item)

        if status[9] == 'forest_big':
            cursor.execute('select * from enemy')
            enemys = cursor.fetchall()
            for item in enemys:
                id = str(item[0])
                if id.startswith('5'):
                    ENEMYS.append(item)
        elif status[9] == 'forest':
            cursor.execute('select * from enemy')
            enemys = cursor.fetchall()
            for item in enemys:
                id = str(item[0])
                if id.startswith('4'):
                    ENEMYS.append(item)

        if status[9] == 'cave':
            cursor.execute('select * from enemy')
            enemys = cursor.fetchall()
            for item in enemys:
                id = str(item[0])
                if id.startswith('7'):
                    ENEMYS.append(item)
    except Exception as e:
        print(e)

    selected_enemy = random.randint(0, len(ENEMYS)-1)
    selected_enemy = ENEMYS[selected_enemy]

    try:
        cursor.execute('update enemy_status set id_enemy=? where id_player=?', [selected_enemy[0], message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)


    bot.send_message(message.chat.id, 'Ты встретил %s на своём пути' % selected_enemy[1], reply_markup=kb_attack)

def attack_enemy(message):
    try:
        cursor.execute('select * from enemy_status where id_player=?', [message.from_user.id])
        enemy_status = cursor.fetchone()
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        cursor.execute('select * from enemy where id=?', [enemy_status[1]])
        enemy = cursor.fetchone()
    except Exception as e:
        print(e)

    #player_health