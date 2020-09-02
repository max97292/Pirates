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
kb_colony_center = types.ReplyKeyboardMarkup(True, False)
kb_colony_pier = types.ReplyKeyboardMarkup(True, False)

kb_colony.row('🏠 Окраина', '🏙 Центр', '⚓ Причал')
kb_colony_edge.row('🛍︎ Странная лавка' , '💀 Злачный переулок' , '🌿 Лавка травника')
kb_colony_center.row('🏛 Ратуша' , '💹 Рынок' , '🍺 Кабак')
kb_colony_pier.row('⛯ Маяк' , '🧰 Кузня' , '🥃 Бар')

def colony_start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в Поселение', reply_markup=kb_colony)

def colony_edge(message):
    bot.send_message(message.chat.id, 'Добро пожаловать на окраину', reply_markup=kb_colony_edge)
def colony_center(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в центр', reply_markup=kb_colony_center)
def colony_pier(message):
    bot.send_message(message.chat.id, 'Добро пожаловать на причал', reply_markup=kb_colony_pier)