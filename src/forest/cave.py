# -*- coding: utf-8 -*-
import random
import time

import telebot
import sqlite3

from telebot import types
from src.config import TOKEN
from src.enemys.enemys import select_enemys
from src.functions.transition import transition

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("DataBase.db", check_same_thread=False)
cursor = conn.cursor()

kb_welcome_cave = types.ReplyKeyboardMarkup(True, False)
kb_forward_cave = types.ReplyKeyboardMarkup(True, False)

kb_welcome_cave.row('⬆️ Идти вперед')


def welcom_cave(message):
    try:
        cursor.execute('update status set location=? where id_player=?', ['cave_start', message.from_user.id])
        conn.commit()
        cursor.execute('update cave_status set enemys=? where id_player=?', [0, message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id,
                     'Ты решил свернуть в пещеру, но что-то тебя остановило. Впереди был очень узкий проход и ты задумался идти вперед или нет?',
                     reply_markup=kb_welcome_cave)


def forward_cave(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        cursor.execute('select * from cave_status where id_player=?', [message.from_user.id])
        cave_status = cursor.fetchone()
        cave_status = cave_status[1]
        cave_status = str(cave_status).split(',')
    except Exception as e:
        print(e)
    if status[9] == 'cave_start':
        try:
            cursor.execute('update status set location=? where id_player=?', ['cave_forward_1', message.from_user.id])
            conn.commit()
        except Exception as e:
            print(e)
    else:
        search = False

        ENEMYS = []

        kb_attack = types.ReplyKeyboardMarkup(True, False)

        kb_attack.row('👊🏻 Атаковать', 'Обойти стороной')

        try:
            cursor.execute('select * from status where id_player=?', [message.from_user.id])
            status = cursor.fetchone()
        except Exception as e:
            print(e)

        if status[9].startswith('cave'):
            cursor.execute('select * from enemy')
            enemys = cursor.fetchall()
            for item in enemys:
                id = str(item[0])
                if id.startswith('7'):
                    if id in cave_status:
                        pass
                    else:
                        ENEMYS.append(item)
                        search = True

        if ENEMYS == []:
            try:
                cursor.execute('update status set location=? where id_player=?',
                               ['cave_end', message.from_user.id])
                conn.commit()
            except Exception as e:
                print(e)
        if status[9] == 'cave_end':
            bot.send_message(message.chat.id, 'Ты дошел до края пещеры, нашел награду')
        else:
            if search == False:
                bot.send_message(message.chat.id, 'Тут произошла ошибочка')
            else:
                selected_enemy = random.randint(0, len(ENEMYS) - 1)
                selected_enemy = ENEMYS[selected_enemy]

                if cave_status == ['0']:
                    cave_status.clear()
                    cave_status.append(str(selected_enemy[0]))
                else:
                    cave_status.append(str(selected_enemy[0]))
                cave_status = ','.join(cave_status)
                print(cave_status)
                try:
                    cursor.execute('update enemy_status set id_enemy=?, health=? where id_player=?',
                                   [selected_enemy[0], selected_enemy[2], message.from_user.id])
                    conn.commit()
                    cursor.execute('update cave_status set enemys=? where id_player=?',
                                   [cave_status, message.from_user.id])
                    conn.commit()
                except Exception as e:
                    print(e)

                bot.send_message(message.chat.id,
                                 'Ты встретил %s (%d❤) на своём пути' % (selected_enemy[1], selected_enemy[2]),
                                 reply_markup=kb_attack)
