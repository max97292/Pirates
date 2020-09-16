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
    search = False

    ENEMYS = []

    kb_attack = types.ReplyKeyboardMarkup(True, False)

    kb_attack.row('👊🏻 Атаковать', 'Обойти стороной')

    try:
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
    except Exception as e:
        print(e)

    if status[9] == 'beach':
        cursor.execute('select * from enemy')
        enemys = cursor.fetchall()
        for item in enemys:
            id = str(item[0])
            if id.startswith('2'):
                ENEMYS.append(item)
                search = True

    if status[9] == 'colony':
        cursor.execute('select * from enemy')
        enemys = cursor.fetchall()
        for item in enemys:
            id = str(item[0])
            if id.startswith('3'):
                ENEMYS.append(item)
                search = True

    if status[9] == 'forest_big':
        cursor.execute('select * from enemy')
        enemys = cursor.fetchall()
        for item in enemys:
            id = str(item[0])
            if id.startswith('5'):
                ENEMYS.append(item)
                search = True

    elif status[9].startswith('forest'):
        cursor.execute('select * from enemy')
        enemys = cursor.fetchall()
        for item in enemys:
            id = str(item[0])
            if id.startswith('4'):
                ENEMYS.append(item)
                search = True

    if status[9] == 'cave':
        cursor.execute('select * from enemy')
        enemys = cursor.fetchall()
        for item in enemys:
            id = str(item[0])
            if id.startswith('7'):
                ENEMYS.append(item)
                search = True

    if search == False:
        bot.send_message(message.chat.id, 'Тут произошла ошибочка')
    else:
        selected_enemy = random.randint(0, len(ENEMYS) - 1)
        selected_enemy = ENEMYS[selected_enemy]

        try:
            cursor.execute('update enemy_status set id_enemy=?, health=? where id_player=?',
                           [selected_enemy[0], selected_enemy[2], message.from_user.id])
            conn.commit()
            cursor.execute('')
        except Exception as e:
            print(e)

        bot.send_message(message.chat.id, 'Ты встретил %s (%d❤) на своём пути' % (selected_enemy[1], selected_enemy[2]), reply_markup=kb_attack)


def attack_enemy(message):
    try:
        cursor.execute('select * from enemy_status where id_player=?', [message.from_user.id])
        enemy_status = cursor.fetchone()
        cursor.execute('select * from status where id_player=?', [message.from_user.id])
        status = cursor.fetchone()
        cursor.execute('select * from enemy where id=?', [enemy_status[1]])
        enemy = cursor.fetchone()
        cursor.execute('select kit from equipment where id_player=?', [message.from_user.id])
        kit = cursor.fetchone()
        kit = kit[0]
        cursor.execute('select * from items where id=?', [kit])
        item = cursor.fetchone()
    except Exception as e:
        print(e)

    if enemy == None:
        bot.send_message(message.chat.id, 'Тут нет монстров')

    else:

        player_health = status[4]
        monster_health = enemy_status[2]

        player_full_health = status[5]
        monster_full_health = enemy[2]

        player_power = status[6]
        monster_power = enemy[3]

        player_protection = status[7]
        monster_protection = enemy[4]

        player_agility = status[10]
        player_agility = player_agility/100

        monster_name = enemy[1]

        monster_type = enemy[5]
        monster_incoming = enemy[6]
        monster_outgoing = list(str(enemy[7]))

        move = enemy_status[3]

        if item is not None:
            item_damage = item[2]
            item_usability = item[3]
            item_usability = item_usability/100
            item_type = item[6]
        else:
            item_damage = 0
            item_usability = 0/100
            item_type = 0

        message_out = 'Бой против %s \n\n' % (monster_name)

        '''while True:
            if player_health <= 0:
                bot.send_message(message.chat.id, message_out)# + '\n❤0/%d\n') % [player_full_health[0] ]
                break'''

        if move == 5:
            step = random.randint(0,1)
        elif move == 0:
            step = 1
        elif move == 1:
            step = 0

        if step == 0:
            damage = player_power

            low_damage = damage * 0.5
            high_damage = damage * 1.5

            usability = random.uniform(0, 1)
            if (item_usability) > usability:
                low_damage = damage * item_usability

            attack = random.randint(low_damage, high_damage)

            if monster_incoming == 1:
                if item_type == 2:
                    pass
                else:
                    attack -= attack * random.uniform(0, 0.3)
            if monster_incoming == 2:
                if item_type == 1:
                    pass
                elif item_type == 2:
                    attack -= attack * random.uniform(0, 0.1)
                else:
                    attack -= attack * random.uniform(0, 0.9)

            chance = random.uniform(0,1)
            if chance < 0.125:
                attack *= 0
                bot.send_message(message.chat.id, 'Монстро уклонился')
            else:
                chance = random.uniform(0, 0.875)
                if chance < 0.125:
                    attack *= 0.5
                    monster_health -= attack
                    if monster_health <= 0:
                        monster_health = 0
                    bot.send_message(message.chat.id, 'Монстро избежал урон\nАтака: %d\nLow/high: %d/%d\n❤ монстра: %d' % (attack, low_damage, high_damage, monster_health))
                else:
                    monster_health -= attack
                    if monster_health <= 0 :
                        monster_health = 0
                    bot.send_message(message.chat.id, 'Атака: %d\nLow/high: %d/%d\n❤ монстра: %d' % (attack, low_damage, high_damage, monster_health))
            try:
                cursor.execute('update enemy_status set health=?, move=? where id_player=?',
                               [int(monster_health), int(step), message.from_user.id])
                conn.commit()
            except Exception as e:
                print(e)

            if monster_health <= 0:
                try:
                    cursor.execute('update enemy_status set id_enemy=?, health=?, move=? where id_player=?',
                                   [0, 0, 5, message.from_user.id])
                    conn.commit()
                except Exception as e:
                    print(e)

                bot.send_message(message.chat.id, 'Монстр умер')

        if step == 1:
            enemy_damage = monster_power

            enemy_low_damage = enemy_damage * 0.5
            enemy_high_damage = enemy_damage * 1.5

            enemy_attack = random.randint(enemy_low_damage, enemy_high_damage)

            enemy_attack -= player_protection
            if enemy_attack < 1:
                enemy_attack = random.randint(1, 20)

            enemy_chance = random.uniform(0,1)
            if enemy_chance < player_agility/2:
                enemy_attack *= 0
                bot.send_message(message.chat.id, 'Игрок уклонился')
            else:
                enemy_chance = random.uniform(0, 1-player_agility/2)
                if enemy_chance < player_agility/2:
                    enemy_attack *= 0.5
                    player_health -= enemy_attack
                    if player_health <= 0:
                        player_health = 0
                    bot.send_message(message.chat.id,
                                     'Игрок избежал урон\nАтака: %d\nLow/high: %d/%d\n❤ игрока: %d' % (enemy_attack, enemy_low_damage, enemy_high_damage, player_health))
                else:
                    enemy_attack *= 1
                    player_health -= enemy_attack
                    if player_health <= 0:
                        player_health = 0
                    bot.send_message(message.chat.id, 'Монстр атаковал: %d\nLow/high: %d/%d\n❤ игрока: %d' % (enemy_attack, enemy_low_damage, enemy_high_damage, player_health))

            try:
                cursor.execute('update enemy_status set health=?, move=? where id_player=?',
                               [int(monster_health), int(step), message.from_user.id])
                conn.commit()
                cursor.execute('update status set health=? where id_player=?', [int(player_health), message.from_user.id])
            except Exception as e:
                print(e)

            if player_health <=0 :
                try:
                    cursor.execute('update enemy_status set id_enemy=?, health=?, move=? where id_player=?',
                                   [0,0,5, message.from_user.id])
                    conn.commit()
                    cursor.execute('update status set health=? where id_player=?',
                                   [int(player_health), message.from_user.id])
                except Exception as e:
                    print(e)

                bot.send_message(message.chat.id, 'Ты умер')

def pass_by(message):
    chance = random.uniform(0, 1)
    if chance < 0.5:
        try:
            cursor.execute('update enemy_status set id_enemy=?, move=? where id_player=?',
                           [0, 5, message.from_user.id])
            conn.commit()
        except Exception as e:
            print(e)
        bot.send_message(message.chat.id, 'Ты обошел стороной монстра')