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

kb_correct_healt = types.ReplyKeyboardMarkup(True, False)

kb_correct_healt.row('❤ Восстановить здоровье', '🩺 Снять отрицательные эффекты')
kb_correct_healt.row('⬅ Назад')


def correct_health(message):
    global kb_correct_healt
    try:
        cursor.execute('update status set location=? where id_player=?', ['correct_health', message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Выбери чего ты хочешь добиться', reply_markup=kb_correct_healt)


def heal(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        full_health = status[5]
        cursor.execute('update status set health=? where id_player=?', [full_health, message.from_user.id])
        conn.commit()
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, 'Ты полностью восстановил свое здоровье 💖')


def activated_coal(message):
    bot.send_message(message.chat.id, 'Уголь пока не успели выкопать 💁‍♂')


def recovery_potion(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        full_health = status[5]
        health = status[4]
        if health == full_health:
            bot.send_message(message.chat.id, 'Зачем тебе пить, ведь ты уже полон сил 💪')
        else:
            health += 400
            if health > full_health:
                health = full_health
            cursor.execute('update status set health=? where id_player=?', [health, message.from_user.id])
            conn.commit()
            bot.send_message(message.chat.id, 'Ты выпил микстуру и тебе немного полегчало')
    except Exception as e:
        print(e)


def healing_potion(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        full_health = status[5]
        health = status[4]
        if health == full_health:
            bot.send_message(message.chat.id, 'Твое здоровье и так на высоте')
        else:
            cursor.execute('update status set health=? where id_player=?', [full_health, message.from_user.id])
            conn.commit()
            bot.send_message(message.chat.id, 'Ты полностью восстановил свое здоровье 💖')
    except Exception as e:
        print(e)


def protection_potion(message):
    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        protection = status[7]
        protection += 30
        cursor.execute('update status set protection=? where id_player=?', [protection, message.from_user.id])
        conn.commit()
        bot.send_message(message.chat.id, 'Зелье защиты были успешно выпито')
        time.sleep(60)
        protection -= 30
        cursor.execute('update status set protection=? where id_player=?', [protection, message.from_user.id])
        conn.commit()
        bot.send_message(message.chat.id, 'Зелье защиты перестало действовать')
    except Exception as e:
        print(e)
