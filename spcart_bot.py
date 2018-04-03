# -*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf8  

import sys
import time
import re
import telebot
import traceback

from telebot import types

from spcb_db import SPCB_DB
from markup import Markup
from inline_markup import InlineMarkup

from util import st_col

from handle_keyboard import handle_keyboard
from handle_inline_keyboard import handle_inline_keyboard
from templates import tpl_cmd

TOKEN = '<YOUR_TOKEN>' # полученный у @BotFather

bot = telebot.TeleBot(TOKEN)

# соединение с базой данных
db = SPCB_DB('localhost', '<user>', '<password>', 'spcart_bot')

markup = Markup()
inline_markup = InlineMarkup()

if __name__ == '__main__':
    db.connect()

@bot.message_handler(commands=['start', ''])
def start(message):

    try:
    
        msg = u'SPCartBot — Калькулятор покупок.\n\r'
        msg += u'Основные команды:\n\r'
        msg += u'/new —  Добавить товар через форму (псевдоним: "+", "new")\n\r'
        msg += u'/del — Удалить товар выбрав его из списка товаров (псевдоним: "-", "del")\n\r'
        msg += u'/update — Редактировать товар выбрав его из списка товаров (псевдоним: "#", ""upd"","update", "/upd")\n\r'
        msg += u'/list — Показать содержимое текущей корзины и итоговую сумму (псевдоним: "list")\n\r'
        msg += u'/start — Вызов начального экрана (псевдоним: "/")\n\r'
        msg += u'/newcart — Очистить текущую корзину и создать новую (псевдонимы: "*0", "newcart", "clean", "nc", "/clean", "/nc")\n\r'
        msg += u'/cmd — Список всех доступных команд (псевдоним: "cmd")\n\r'
    
        sent = bot.send_message(message.chat.id, msg, reply_markup=markup.generate(), parse_mode='HTML')
    except Exception as e: print(traceback.format_exc(10))
    
@bot.message_handler(commands=['cmd'])
def cmd(message):

    try:
        # получаем список всех команд
        msg = tpl_cmd()
        sent = bot.send_message(message.chat.id, msg, reply_markup=markup.generate(), parse_mode='HTML')
    except Exception as e: print(traceback.format_exc(10))
    
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    db.setMsg(message, bot)
    handle_keyboard(message, db, bot, inline_markup)   
   
   
@bot.callback_query_handler(func=lambda c: c.data)
def pages(c):
    db.setMsg(c.message, bot)
    handle_inline_keyboard(c, db, bot, inline_markup)

bot.polling()