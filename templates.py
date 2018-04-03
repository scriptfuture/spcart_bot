# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys

from util import st_col, empty_nl, empty_nl_temp
from decimal import Decimal

def tpl_delProduct(id, st_amount):

    resMsg = ""
    
    if st_amount is not None:
        resMsg = u"<code>Товар №"+empty_nl(str(id))+u" удалён.</code>\n\r"
        resMsg += u"Общая сумма: <b>"+st_amount+u"</b>"
    else: 
        resMsg = u"<code>Не удалось удалить товар №"+empty_nl(str(id))+u"!</code>"
        
    return resMsg
    
def tpl_newProduct(newProduct):
    
    resMsg = u"<code>Тов. добавлен в корзину:\n\r"
        
    resMsg += st_col(2, u"№", True)+"|"
    resMsg += st_col(6, u"цена")+"|"
    resMsg += st_col(5, u"кол.")+"|"
    resMsg += st_col(7, u"сумма")+"\n\r"

    if newProduct["product_id"] == 1:
        resMsg += ('-' *23) + "\n\r" 
    else:
        resMsg += '-----------//-----------\n\r'
        
    resMsg += st_col(2, empty_nl(str(newProduct["product_id"])), True)+"|"+st_col(6, empty_nl(str(newProduct["price"])))+"|"+st_col(5, empty_nl(str(newProduct["quantity"])))+"|"+st_col(7, empty_nl(str(newProduct["prod_amount"])))
        
    resMsg += u"</code>\n\r\n\rОбщая сумма: <b>"+empty_nl(str(newProduct["amount"]))+"</b>"
    
    return resMsg

    
def tpl_editProduct(editProduct):
    
    resMsg = u"<code>Товар отредактирован:\n\r"
        
    resMsg += st_col(2, u"№", True)+"|"
    resMsg += st_col(6, u"цена")+"|"
    resMsg += st_col(5, u"кол.")+"|"
    resMsg += st_col(7, u"сумма")+"\n\r"

    if editProduct["product_id"] == 1:
        resMsg += ('-' *23) + "\n\r" 
    else:
        resMsg += '-----------//-----------\n\r'
        
    resMsg += st_col(2, empty_nl(str(editProduct["product_id"])), True)+"|"+st_col(6, empty_nl(str(editProduct["price"])))+"|"+st_col(5, empty_nl(str(editProduct["quantity"])))+"|"+st_col(7, empty_nl(str(editProduct["prod_amount"])))
        
    resMsg += u"</code>\n\r\n\rОбщая сумма: <b>"+empty_nl(str(editProduct["amount"]))+"</b>"
    
    return resMsg
    
def tpl_list(products):
    
    cart_line = u"<code>"        
    cart_line += st_col(2, u"№", True)+"|"
    cart_line += st_col(6, u"цена")+"|"
    cart_line += st_col(5, u"кол.")+"|"
    cart_line += st_col(7, u"сумма")+"\n\r"
        
    cart_line += ('-' *23) + u"\n\r" 

    total = 0
    for product in products: 
        sym = Decimal(product["price"]) * Decimal(product["quantity"])
        total += sym
            
        cart_line += st_col(2, empty_nl(str(product["product_id"])), True) + u"|"
        cart_line += st_col(6, empty_nl(str(product["price"]))) + u"|"
        cart_line += st_col(5, empty_nl(str(product["quantity"]))) + u"|"
        cart_line += st_col(7, empty_nl(str(sym)))
        cart_line += u"\n\r"
   
    cart_line += u"</code>\n\rИтого:  <b>"+ empty_nl(str(total)) +u"</b>\n\r"
    
    return cart_line
    
def tpl_edit_msg(price, quant, total, isPrice, product_id):

    res = u"<code>"
    
    if product_id is not None:
        res += u"Товар №"+str(product_id)+u"\n\r"
    
    if isPrice:
        res += st_col(10, u">>Цена: ")+" "+st_col(15, empty_nl_temp(str(price)), True)+u"\n\r"
        res += st_col(10, u"Кол-во: ")+" "+st_col(15, empty_nl_temp(str(quant)), True)+u"\n\r"
    else:
        res += st_col(10, u"Цена: ")+" "+st_col(15, empty_nl_temp(str(price)), True)+u"\n\r"
        res += st_col(10, u">>Кол-во: ")+" "+st_col(15, empty_nl_temp(str(quant)), True)+u"\n\r"

    res += st_col(10, u"Сумма: ")+" "+st_col(15, empty_nl(str(Decimal(price)*Decimal(quant))), True)+u"\n\r"
    res += u"</code>"
        
    res += u"Общая сумма: <b>"+empty_nl(str(total))+u"</b>"
    
    return res
    
def tpl_cmd():

    msg = u'<b>Список всех команд:</b>\n\r'
    msg += u'/new —  Добавить товар через форму (псевдоним: "+", "new")\n\r'
    msg += u'/del — Удалить товар выбрав его из списка товаров (псевдоним: "-", "del")\n\r'
    msg += u'/update — Редактировать товар выбрав его из списка товаров (псевдоним: "#", ""upd"","update", "/upd")\n\r'
    msg += u'/list — Показать содержимое текущей корзины (списка товаров) и итоговую сумму (псевдоним: "list")\n\r'
    msg += u'/start — Вызов начального экрана (псевдоним: "/")\n\r'
    msg += u'/newcart — Очистить текущую коризину и создать новую (псевдонимы: "*0", "newcart", "clean", "nc", "/clean", "/nc")\n\r'
    msg += u'/cmd — Список всех доступных команд (псевдоним: "cmd")\n\r\n\r'
    
    msg += u'<b>Команды с параметрами (пробелы игнорируются):</b>\n\r'

    msg += u'<b>+ {price} * {quant}</b>  — Добавление товара, где {price} цена, {quant} количество товара\n\r'
    msg += u'<b>+ {price}</b> — Добавление товара, где {price} цена товара\n\r'
    
    msg += u'<b>#{id}</b> — Редактирование товара, где {id} номер товара в списке\n\r'
    msg += u'<b>#{id}: {price} * {quant}</b>  — Редактирование товара по его номеру, где {id} номер товара в списке, {price} цена, {quant} количество товара\n\r'
    msg += u'<b>#{id}: * {quant}</b> —  Редактирование товара по его номеру, где {id} номер товара в списке, {quant} количество товара\n\r'
    msg += u'<b>-{id}</b> — Удаление товара, где {id} номер товара в списке\n\r'


    return msg
    