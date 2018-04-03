# -*- coding: utf-8 -*-
#!/usr/bin/env python

import telebot

from telebot import types

class Markup:

    def generate(self):
        """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)


        button_plus = types.KeyboardButton(text="+")
        button_minus = types.KeyboardButton(text="-")
        button_edit = types.KeyboardButton(text="#")
        button_list = types.KeyboardButton(text="list")
        button_start = types.KeyboardButton(text="/")
        button_newcart = types.KeyboardButton(text="*0")

        markup.row(button_plus, button_minus, button_edit, button_list, button_start, button_newcart)
        
        return markup