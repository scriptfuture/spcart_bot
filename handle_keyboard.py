# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re
import traceback

from util import st_col
from templates import tpl_delProduct, tpl_newProduct, tpl_list, tpl_edit_msg, tpl_editProduct, tpl_cmd


def handle_keyboard(message, db, bot, inline_markup):

    try:

        q = message.text

        if q == "+" or q == "/new" or q == "new":
        
            # получаем общую сумму товаров
            total = db.getProductsTotal(message.from_user.id)
            
            # удаляем временный продукт
            db.delProductTemp(message.from_user.id, 'c')
            
            # создаём новый временный продукт
            db.setProductTemp(message.from_user.id, 'c', '', '')
        
            # начальный шаблон
            resMsg = tpl_edit_msg(0, 1, total, True, None)
        
            sent = bot.send_message(message.chat.id, resMsg, reply_markup=inline_markup.generate(), parse_mode='HTML')
                
        elif q == "-" or q == "/del" or q == "del":
            sent = bot.send_message(message.chat.id, u'Выбирите товар который нужно удалить:', reply_markup=inline_markup.generate_del_list(db, message.from_user.id))
            
        elif q == "#" or q == "/update" or q == "/upd" or q == "upd" or q == "update":
            sent = bot.send_message(message.chat.id, u'Выбирите товар для редактирования:', reply_markup=inline_markup.generate_edit_list(db, message.from_user.id))
                
        elif q == "list" or q == "/list":
            
            products = db.getProducts(message.from_user.id)
            
            # получаем шаблон корзины (списка товаров)        
            cart_line = tpl_list(products)

            sent = bot.send_message(message.chat.id, cart_line, parse_mode='HTML')
            
        elif q == "cmd":

            # получаем список всех команд
            msg = tpl_cmd()
            
            sent = bot.send_message(message.chat.id, msg, parse_mode='HTML')
            
        elif q == "newcart" or q == "clean" or q == "nc"  or q == "*0" or q == "/newcart" or q == "/clean" or q == "/nc":
            sent = bot.send_message(message.chat.id, u"<b>Создать новую корзину?</b>\n\rТовары текущей корзины будут удалены.", parse_mode='HTML', reply_markup=inline_markup.generate_confirm_newcart())
                
        #q = " +  345.432  *  34"
        elif re.search(r'^([ ]*)\+([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)\*([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)$', q):

            p = re.compile('^([ ]*)\+([ ]*)(?P<price>([0-9]+)(\.[0-9]+)?)([ ]*)\*([ ]*)(?P<quant>([0-9]+)(\.[0-9]+)?)([ ]*)$')
            r = p.search(q)
            
            # сохраняем в базу
            newProduct = db.newProduct(message.from_user.id, r.group("price"), r.group("quant"))
            
            # рендерим шаблон нового продукта
            resMsg = tpl_newProduct(newProduct);
            
            bot.send_message(message.chat.id, resMsg, parse_mode='HTML')  
            

        #q = "+  347.12"
        elif re.search(r'^([ ]*)\+([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)$', q): 
            p = re.compile('^([ ]*)\+([ ]*)(?P<price>([0-9]+)(\.[0-9]+)?)([ ]*)$')
            r = p.search(q)
            
            # сохраняем в базу
            newProduct = db.newProduct(message.from_user.id, r.group("price"), "1")
            
            # рендерим шаблон нового продукта
            resMsg = tpl_newProduct(newProduct);
            
            bot.send_message(message.chat.id, resMsg, parse_mode='HTML')  

        #q = " # 325"
        elif re.search(r'^([ ]*)\#([ ]*)([0-9]+)([ ]*)$', q): 
            p = re.compile('^([ ]*)\#([ ]*)(?P<id>([0-9]+))([ ]*)$')
            r = p.search(q)
            
            # получаем общую сумму товаров
            total = db.getProductsTotal(message.from_user.id)
            
            product = db.getProduct(message.from_user.id, r.group("id"))
            
            if product is not None:
            
                # удаляем временный продукт
                db.delProductTemp(message.from_user.id, 'u')
            
                # создаём временный продукт с product_id
                db.setProductTemp(message.from_user.id, 'u', 'product_id', r.group("id"))
            
                # начальный шаблон
                resMsg = tpl_edit_msg(product["price"], product["quantity"], total, True, r.group("id"))
                
                bot.send_message(message.chat.id, resMsg, reply_markup=inline_markup.generate_edit(), parse_mode='HTML')
            else: 
                resMsg = u"Ошибка при редактировании. Повторите попытку."
                
                bot.send_message(message.chat.id, resMsg, parse_mode='HTML')
        
           

        #q = " # 28: 128.9 *4.9"
        elif re.search(r'^([ ]*)\#([ ]*)([0-9]+)([ ]*)\:([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)\*([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)$', q):

            p = re.compile('^([ ]*)\#([ ]*)(?P<id>([0-9]+))([ ]*)\:([ ]*)(?P<price>([0-9]+)(\.[0-9]+)?)([ ]*)\*([ ]*)(?P<quant>([0-9]+)(\.[0-9]+)?)([ ]*)$')
            r = p.search(q)
            
            editProduct = db.updateProduct(message.from_user.id, r.group("id"), r.group("price"), r.group("quant"))
            
            # рендерим шаблон отредактированного товара
            if editProduct is not None:
                resMsg = tpl_editProduct(editProduct)
            else:
                resMsg = u"Ошибка при редактировании. Повторите попытку."
            
            bot.send_message(message.chat.id, resMsg, parse_mode='HTML')  
            
            
        #q = " # 28: 128.9"
        elif re.search(r'^([ ]*)\#([ ]*)([0-9]+)([ ]*)\:([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)$', q):

            p = re.compile('^([ ]*)\#([ ]*)(?P<id>([0-9]+))([ ]*)\:([ ]*)(?P<price>([0-9]+)(\.[0-9]+)?)([ ]*)$')
            r = p.search(q)
            
            editProduct = db.updateProductPrice(message.from_user.id, r.group("id"), r.group("price"))
            
            # рендерим шаблон отредактированного товара
            if editProduct is not None:
                resMsg = tpl_editProduct(editProduct)
            else:
                resMsg = u"Ошибка при редактировании. Повторите попытку."
            
            bot.send_message(message.chat.id, resMsg, parse_mode='HTML')  
         
        #q = "#236: *7.1"
        elif re.search(r'^([ ]*)\#([ ]*)([0-9]+)([ ]*)\:([ ]*)\*([ ]*)([0-9]+)(\.[0-9]+)?([ ]*)$', q):

            p = re.compile('^([ ]*)\#([ ]*)(?P<id>([0-9]+))([ ]*)\:([ ]*)\*([ ]*)(?P<quant>([0-9]+)(\.[0-9]+)?)([ ]*)$')
            r = p.search(q)
            
            editProduct = db.updateProductQuant(message.from_user.id, r.group("id"), r.group("quant"))
            
            # рендерим шаблон отредактированного товара
            if editProduct is not None:
                resMsg = tpl_editProduct(editProduct)
            else:
                resMsg = u"Ошибка при редактировании. Повторите попытку."
            
            bot.send_message(message.chat.id, resMsg, parse_mode='HTML')  
            

        #q = " - 325"
        elif re.search(r'^([ ]*)\-([ ]*)([0-9]+)([ ]*)$', q): 
            p = re.compile('^([ ]*)\-([ ]*)(?P<id>([0-9]+))([ ]*)$')
            r = p.search(q)
            
            st_amount = db.delProduct(message.from_user.id, r.group("id"))
            
            # получаем шаблон текст о удалении
            resMsg = tpl_delProduct(r.group("id"), st_amount)

            sent = bot.send_message(message.chat.id, resMsg, parse_mode='HTML')
        
    except Exception as e: print(traceback.format_exc(10))
   