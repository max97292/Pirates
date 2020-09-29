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


def select_spec(message):
    kb_spec = types.ReplyKeyboardMarkup(True, False)
    try:
        cursor.execute('select * from players where id=?', [message.from_user.id])
        players = cursor.fetchone()
    except Exception as e:
        print(e)

    if players[2] == 1:
        kb_spec.row('🎖 Капитан', '📯 Командир')
    if players[2] == 2:
        kb_spec.row('🎭 Счастливчик', '💰 Торгаш')
    if players[2] == 3:
        kb_spec.row('⚔ Верзила', '💣 Стрелок')
    if players[2] == 4:
        kb_spec.row('🔭 Картограф', '⚗️ Алхимик')

    bot.send_message(message.chat.id, 'бла-бла-бла, ты классный, вот тебе 1 из 2 специализаций', reply_markup=kb_spec)
