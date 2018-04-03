# -*- coding: utf-8 -*-
#!/usr/bin/env python

import telebot

from telebot import types
from decimal import Decimal

class InlineMarkup:

    def generate(self):
        """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
        markup = types.InlineKeyboardMarkup()

        button_word = types.InlineKeyboardButton(text=u"сброс", callback_data="null")
        button_back = types.InlineKeyboardButton(text=u"<<", callback_data="back")
        button_mode = types.InlineKeyboardButton(text=u"цена/кол.", callback_data="mode")
        
        button_1 = types.InlineKeyboardButton(text="1", callback_data="1")
        button_2 = types.InlineKeyboardButton(text="2", callback_data="2")
        button_3 = types.InlineKeyboardButton(text="3", callback_data="3")
        button_4 = types.InlineKeyboardButton(text="4", callback_data="4")
        button_5 = types.InlineKeyboardButton(text="5", callback_data="5")
        button_6 = types.InlineKeyboardButton(text="6", callback_data="8")
        button_7 = types.InlineKeyboardButton(text="7", callback_data="7")
        button_8 = types.InlineKeyboardButton(text="8", callback_data="8")
        button_9 = types.InlineKeyboardButton(text="9", callback_data="9")
        button_0 = types.InlineKeyboardButton(text="0", callback_data="0")
        
        button_plus = types.InlineKeyboardButton(text=u"+", callback_data="+")
        button_point = types.InlineKeyboardButton(text=u".", callback_data=".")
        button_minus = types.InlineKeyboardButton(text=u"-", callback_data="-")
        
        button_save = types.InlineKeyboardButton(text=u"Сохранить", callback_data="save")

        markup.row(button_word, button_back, button_mode)
        markup.row(button_1, button_2, button_3)
        markup.row(button_4, button_5, button_6)
        markup.row(button_8, button_9, button_0)
        markup.row(button_plus, button_point, button_minus)
        markup.row(button_save)
        
        return markup
        
    def generate_edit(self):
        """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
        markup = types.InlineKeyboardMarkup()

        button_word = types.InlineKeyboardButton(text=u"сброс", callback_data="upd_null")
        button_back = types.InlineKeyboardButton(text=u"<<", callback_data="upd_back")
        button_mode = types.InlineKeyboardButton(text=u"цена/кол.", callback_data="upd_mode")
        
        button_1 = types.InlineKeyboardButton(text="1", callback_data="upd_1")
        button_2 = types.InlineKeyboardButton(text="2", callback_data="upd_2")
        button_3 = types.InlineKeyboardButton(text="3", callback_data="upd_3")
        button_4 = types.InlineKeyboardButton(text="4", callback_data="upd_4")
        button_5 = types.InlineKeyboardButton(text="5", callback_data="upd_5")
        button_6 = types.InlineKeyboardButton(text="6", callback_data="upd_8")
        button_7 = types.InlineKeyboardButton(text="7", callback_data="upd_7")
        button_8 = types.InlineKeyboardButton(text="8", callback_data="upd_8")
        button_9 = types.InlineKeyboardButton(text="9", callback_data="upd_9")
        button_0 = types.InlineKeyboardButton(text="0", callback_data="upd_0")
        
        button_plus = types.InlineKeyboardButton(text=u"+", callback_data="upd_+")
        button_point = types.InlineKeyboardButton(text=u".", callback_data="upd_.")
        button_minus = types.InlineKeyboardButton(text=u"-", callback_data="upd_-")
        
        button_save = types.InlineKeyboardButton(text=u"Сохранить", callback_data="upd_save")

        markup.row(button_word, button_back, button_mode)
        markup.row(button_1, button_2, button_3)
        markup.row(button_4, button_5, button_6)
        markup.row(button_8, button_9, button_0)
        markup.row(button_plus, button_point, button_minus)
        markup.row(button_save)
        
        return markup
        
    def generate_confirm_newcart(self):
        """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
        markup = types.InlineKeyboardMarkup()

        button_yes = types.InlineKeyboardButton(text=u"Да", callback_data="newcart_yes")
        button_no = types.InlineKeyboardButton(text=u"Нет", callback_data="no")
     

        markup.row(button_yes, button_no)
        
        return markup
        
    def generate_del_list(self, db, username):
        """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
        markup = types.InlineKeyboardMarkup()
        
        
        products = db.getProducts(username)
        
        sym = 0
        for product in products: 
            sym = Decimal(product.price) * Decimal(product.quantity)
            markup.add(types.InlineKeyboardButton(text=u""+str(product.product_id)+u")  "+str(product.price)+u" × "+str(product.quantity)+u" = "+str(Decimal(product.price)*Decimal(product.quantity)), callback_data="-"+str(product.product_id)))

        
        return markup

        
    def generate_edit_list(self, db, username):
        """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
        markup = types.InlineKeyboardMarkup()
        
        
        products = db.getProducts(username)
        
        sym = 0
        for product in products: 
            sym = Decimal(product.price) * Decimal(product.quantity)
            markup.add(types.InlineKeyboardButton(text=u""+str(product.product_id)+u")  "+str(product.price)+u" × "+str(product.quantity)+u" = "+str(Decimal(product.price)*Decimal(product.quantity)), callback_data="#"+str(product.product_id)))

        
        return markup