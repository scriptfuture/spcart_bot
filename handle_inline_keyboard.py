# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import re
import traceback

from util import st_col
from templates import tpl_delProduct, tpl_newProduct, tpl_edit_msg, tpl_editProduct
from decimal import Decimal


def handle_inline_keyboard(c, db, bot, inline_markup):
    """Редактируем сообщение каждый раз, когда пользователь переходит по
    страницам.
    """

    print(c.data)
    
    if c.data == 'mode':
 
        try:
        
            tempProduct = db.setProductTemp(c.from_user.id, 'c', "mode", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))

            
    elif c.data == 'back':
    
        try:
        
            tempProduct = db.setProductTemp(c.from_user.id, 'c', "back", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))

           
    elif c.data == 'null':

        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'c', "null", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))
       
        
    elif c.data == '+':
    
        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'c', "+", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))
    
        
    elif c.data == '-':

        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'c', "-", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))
  
        
        
    elif c.data == '.':
        
        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'c', ".", c.data)
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))

        
    elif re.search(r'^\d+$', c.data):
   
        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'c', "num", c.data)
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'c')
        except Exception as e: print(traceback.format_exc(10))
        
    elif c.data == 'save':
    
        try:
    
            # получаем временный текущий продукт
            tempProduct = db.getProductTemp(c.from_user.id, 'c')
            print(tempProduct)
            
            # создаём в базе на основе него новый
            newProduct = db.newProduct(c.from_user.id, Decimal(tempProduct["price"]), Decimal(tempProduct["quantity"]))

            # удаляем временный продукт
            db.delProductTemp(c.from_user.id, 'c')
            
            #  рендерим шаблон
            resMsg = tpl_newProduct(newProduct)
            
            bot.send_message(c.message.chat.id, resMsg, parse_mode='HTML')  
        
        except Exception as e: print(traceback.format_exc(10))

    # Редактирование товара
    elif  c.data == 'upd_mode':

        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'u', "mode", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))

            
    elif c.data == 'upd_back':
    
        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'u', "back", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))

           
    elif c.data == 'upd_null':

        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'u', "null", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))
       
        
    elif c.data == 'upd_+':
  
        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'u', "+", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))
    
        
    elif c.data == 'upd_-':

        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'u', "-", "")
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))
  
        
        
    elif c.data == 'upd_.':
    
        try:
            tempProduct = db.setProductTemp(c.from_user.id, 'u', ".", c.data)
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))

        
    elif re.search(r'^upd_([0-9]{1})$', c.data):
        try:
            p = re.compile('^upd_(?P<num>[0-9]{1})$')
            r = p.search(c.data)
        
            tempProduct = db.setProductTemp(c.from_user.id, 'u', 'num', r.group("num"))
        
            # модифицируем сообщение
            edit_msg(c, bot, db, inline_markup, tempProduct["price"], tempProduct["quant"], tempProduct["kb_mode"], 'u')
        except Exception as e: print(traceback.format_exc(10))
        
    elif c.data == 'upd_save':
    
        try:
    
            # получаем временный текущий продукт
            tempProduct = db.getProductTemp(c.from_user.id, 'u')
            
            # делаем запрос на обновление продукта в базе
            if tempProduct.product_id is not None:
                editProduct = db.updateProduct(c.from_user.id, tempProduct.product_id, tempProduct.price, tempProduct.quantity)
            else:
                editProduct = None
            
            # рендерим шаблон отредактированного товара
            if editProduct is not None:
                
                # удаляем временный продукт
                db.delProductTemp(c.from_user.id, 'u')
            
                # получаем шаблон редактирования
                resMsg = tpl_editProduct(editProduct)
            else:
                resMsg = u"Ошибка при редактировании. Повторите попытку."

            
            bot.send_message(c.message.chat.id, resMsg, parse_mode='HTML')  
        
        except Exception as e: print(traceback.format_exc(10))
        
        
    # подтерждение содания новой корзины
    elif c.data == 'newcart_yes':
    
        try:
            newcart = db.cleanCart(c.from_user.id)
            if newcart is not None:
                bot.send_message(c.message.chat.id, u"<b>Создана новая корзина.</b>", parse_mode='HTML')
        except Exception as e: print(traceback.format_exc(10))
       
    elif c.data == 'no':
        try:
            bot.send_message(c.message.chat.id, u"Операция отменена.", parse_mode='HTML')  
        except Exception as e: print(traceback.format_exc(10))
        
    #c.data = " - 325"
    elif re.search(r'^([ ]*)\-([ ]*)([0-9]+)([ ]*)$', c.data): 
    
        try:
            p = re.compile('^([ ]*)\-([ ]*)(?P<id>([0-9]+))([ ]*)$')
            r = p.search(c.data)
            
            resMsg = u"-"+str(r.group("id"))
          
            sent = bot.send_message(c.message.chat.id, resMsg)
            
            # удаляем товар
            st_amount = db.delProduct(c.from_user.id, r.group("id"))
            
            # получаем шаблон текст о удалении
            resMsg = tpl_delProduct(r.group("id"), st_amount)
            
            sent = bot.send_message(c.message.chat.id, resMsg, parse_mode='HTML')
            
        except Exception as e: print(traceback.format_exc(10))
        
    #c.data = " # 325"
    elif re.search(r'^([ ]*)\#([ ]*)([0-9]+)([ ]*)$', c.data): 
    
        try:
        
            p = re.compile('^([ ]*)\#([ ]*)(?P<id>([0-9]+))([ ]*)$')
            r = p.search(c.data)
            
            resMsg = u"#"+str(r.group("id"))
          
            
            sent = bot.send_message(c.message.chat.id, resMsg)
            
            # --редактируем товар--
            # получаем общую сумму товаров
            total = db.getProductsTotal(c.from_user.id)
            
            product = db.getProduct(c.from_user.id, r.group("id"))
            
            if product is not None:
            
                # создаём временный продукт с product_id
                db.setProductTemp(c.from_user.id, 'u', 'product_id', r.group("id"))
            
                # начальный шаблон
                resMsg = tpl_edit_msg(product.price, product.quantity, total, True, r.group("id"))
                
                bot.send_message(c.message.chat.id, resMsg, reply_markup=inline_markup.generate_edit(), parse_mode='HTML')
            else: 
                resMsg = u"Ошибка при редактировании. Повторите попытку."
                
                bot.send_message(c.message.chat.id, resMsg, parse_mode='HTML')
            
        except Exception as e: print(traceback.format_exc(10))
        
    else:
        print(u"Query is empty!")
        
      
    
    
def edit_msg(c, bot, db, inline_markup, price_st, quant_st, kb_mode, mode):

    total_db = db.getProductsTotal(c.from_user.id)
    total = Decimal('0')

    if total_db is not None:
        total = Decimal(total_db)
    
    total += (Decimal(price_st)*Decimal(quant_st))
    
    res = ""
    if kb_mode == 'q':
        res = tpl_edit_msg(price_st, quant_st, total, False, None)
    else:
        res = tpl_edit_msg(price_st, quant_st, total, True, None)
    
    try:
    
        if mode == 'u':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=res,
                parse_mode='HTML', reply_markup=inline_markup.generate_edit())
        else:
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text=res,
                parse_mode='HTML', reply_markup=inline_markup.generate())
    except Exception as e: print(traceback.format_exc(10))