# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pymysql.cursors

from util import empty_nl

from decimal import Decimal

import pymysql

import traceback

from db import DB

class SPCB_DB(DB):

    message = None
    bot = None
    db_error_text = "Ошибка базы данных. Попробуйте повторить операцию."
    
    def __init__(self, host, user, password, db):
        super().__init__(host, user, password, db)
    
    
    def setMsg(self, message, bot):
        self.message = message
        self.bot = bot

        
    def getProducts(self, user_id):
    
        products = []
        try:
        
            products = self.fetch('SELECT * FROM products WHERE user_id = %s ORDER BY product_id', (int(user_id)))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: 
                print(traceback.format_exc(10))
            
        except Exception as e: 
            self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
        
        return products
        
    def getProductsTotal(self, user_id):
    
        rowRes = 0
        try:
        
            row = self.fetchone("SELECT (SELECT SUM(price * quantity) total FROM products WHERE user_id = %s) full_total FROM products LIMIT 1", (int(user_id)))
            
            print(row)
            
            if row is not None:
                rowRes = row["full_total"]
                
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
                
        except Exception as e: print(traceback.format_exc(10))
        
        return rowRes
        
    def getProductIds(self, user_id):
    
        products = []
        try:
        
            products = self.fetch('SELECT id FROM products WHERE user_id = %s ORDER BY ts', (int(user_id)))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return products
        
    def getProduct(self, user_id, product_id):
    
        row = None
        try:
            row = self.fetchone('SELECT * FROM products WHERE user_id = %s AND product_id = %s', (int(user_id), int(product_id)))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return row
        
    def getCart(self, user_id):
    
        row = None
        try:
        
            row = self.fetchone('SELECT * FROM carts WHERE user_id = %s', (int(user_id)))

        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return row
        
    def newCart(self, user_id):
        
        try:         
            self.execute('INSERT INTO carts(user_id, product_count, amount) VALUES(%s, %s, %s)', (int(user_id), 1, 0))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
    def cleanCart(self, user_id):
        
        try:         
            self.execute('DELETE FROM carts WHERE user_id = %s', (int(user_id)))
            self.execute('DELETE FROM products WHERE user_id = %s', (int(user_id)))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
    def updateCart(self, user_id, product_count, amount):
        
        try:         
            self.execute('UPDATE carts SET product_count = %s, amount = %s WHERE user_id = %s', (int(product_count), Decimal(amount), int(user_id)))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
    def newProduct(self, user_id, price, quant):
        
        product_id = '1'
        amount = '0'
        
        cart = self.getCart(user_id)
        
        print(cart)
            
        if cart is None:
            self.newCart(user_id)
        else:
            product_id = int(cart["product_count"]) + 1  
            amount = cart["amount"]
            
        try:
            
            # сохраняем товар
            self.execute('INSERT INTO products(user_id, product_id, price, quantity) VALUES(%s, %s, %s, %s)', (int(user_id), int(product_id), Decimal(price), Decimal(quant)))
            
            # вычисляем общую сумму
            amount = Decimal(amount) + (Decimal(price) * Decimal(quant))
                
            # обновляем корзину
            self.updateCart(user_id, product_id, amount)  
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return {"product_id": product_id, 'price': Decimal(price), 'quantity': Decimal(quant), 'amount': amount, 'prod_amount': (Decimal(price) * Decimal(quant))}
       
    def updateProductId(self, user_id, id, product_id):
        
        try:         
            self.execute('UPDATE products SET product_id = %s WHERE user_id = %s AND id = %s', (int(product_id), int(user_id), int(id)))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))     
   
   
    def updateProduct(self, user_id, product_id, price, quant):
        
        amount = 0
        
        # получаем общую сумму из корзины
        cart = self.getCart(user_id)
        
        if cart is None:
            self.newCart(user_id)
        else: 
            amount = Decimal(cart["amount"])
        
        try:         
        
            product = self.getProduct(user_id, product_id)
            
            if product is not None:                                                  
            
                # вычисляем общую сумму
                amount = Decimal(amount) - (Decimal(product["price"]) * Decimal(product["quantity"]))
                amount = Decimal(amount) + (Decimal(price) * Decimal(quant))
            

                self.execute('UPDATE products SET  price = %s,  quantity = %s WHERE user_id = %s AND product_id = %s', (Decimal(price), Decimal(quant), int(user_id), int(product_id)))
                
                # обновляем корзину
                self.updateCart(user_id, product_id, amount) 
                
                return {"product_id": product_id, 'price': Decimal(price), 'quantity': Decimal(quant), 'amount': amount, 'prod_amount': (Decimal(price) * Decimal(quant))}
                
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return None
        
        
    def updateProductPrice(self, user_id, product_id, price):
        
        amount = 0
        
        # получаем общую сумму из корзины
        cart = self.getCart(user_id)
        
        if cart is None:
            self.newCart(user_id)
        else: 
            amount = Decimal(cart["amount"])
        
        try:         
        
            product = self.getProduct(user_id, product_id)
            
            if product is not None:                                                  
            
                # вычисляем общую сумму
                amount = Decimal(amount) - (Decimal(product["price"]) * Decimal(product["quantity"]))
                amount = Decimal(amount) + (Decimal(price) * Decimal(product["quantity"]))
            

                self.execute('UPDATE products SET  price = %s WHERE user_id = %s AND product_id = %s', ( Decimal(price), int(user_id), int(product_id)))
                
                # обновляем корзину
                self.updateCart(user_id, product_id, amount) 
                
                return {"product_id": product_id, 'price': Decimal(price), 'quantity': Decimal(product["quantity"]), 'amount': amount, 'prod_amount': (Decimal(price) * Decimal(product["quantity"]))}
                
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return None
        
    def updateProductQuant(self, user_id, product_id, quant):
        
        amount = 0
        
        # получаем общую сумму из корзины
        cart = self.getCart(user_id)
        
        if cart is None:
            self.newCart(user_id)
        else: 
            amount = Decimal(cart["amount"])
        
        try:         
        
            product = self.getProduct(user_id, product_id)
            
            if product is not None:                                                  
            
                # вычисляем общую сумму
                amount = Decimal(amount) - (Decimal(product["price"]) * Decimal(product["quantity"]))
                amount = Decimal(amount) + (Decimal(product["price"]) * Decimal(quant))
            

                self.execute('UPDATE products SET  quantity = %s WHERE user_id = %s AND product_id = %s', (Decimal(quant), int(user_id), int(product_id)))
                
                # обновляем корзину
                self.updateCart(user_id, product_id, amount) 
                
                return {"product_id": product_id, 'price': Decimal(product["price"]), 'quantity': Decimal(quant), 'amount': amount, 'prod_amount': (Decimal(product["price"]) * Decimal(quant))}
                
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return None
        
    def delProduct(self, user_id, product_id):
    
        minus_amount = None
        
        try:   
        
            cart = self.getCart(user_id)
            product = self.getProduct(user_id, product_id)           
            
            # изменить сумму
            self.execute('DELETE FROM products WHERE user_id = %s AND product_id = %s', (int(user_id), int(product_id)))
            
            minus_product_id = int(cart["product_count"]) - 1
            minus_amount = int(cart["amount"]) - (int(product["price"]) * int(product["quantity"]))
            
            # обновляем корзину
            if minus_amount is not None:
                self.updateCart(user_id, minus_product_id, minus_amount)  
            
            # обновляем список продуктов (product_id)
            productIds = self.getProductIds(user_id)
            i = 1
            for prod in productIds: 
                self.updateProductId(user_id, prod["id"], i)
                print(i)
                i = i + 1
                
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return minus_amount
        
    def getProductTemp(self, user_id, action):
    
        row = None
        try:
        
            row = self.fetchone('SELECT * FROM products_temp WHERE user_id = %s AND action = %s', ( int(user_id), action))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))
            
        except Exception as e: print(traceback.format_exc(10))
        
        return row
        
    def delProductTemp(self, user_id, action):
        
        try:     
            
            # изменить сумму
            self.execute('DELETE FROM products_temp WHERE user_id = %s AND action = %s', (int(user_id), action))
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.err.InternalError:
            try:
                self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
            except Exception as e: print(traceback.format_exc(10))

        except Exception as e: print(traceback.format_exc(10))
        
    def setProductTemp(self, user_id, action, name, val):        
            
        # получаем временный продукт
        product_temp = self.getProductTemp(user_id, action)
        
        param = None
        
        price = '0'
        quant = '1'
        kb_mode = 'p'
        
        # если его нет создаём
        if product_temp is None:
        
            if name == 'product_id': 
            
                # получаем продукт по id
                product = self.getProduct(user_id, int(val))   
            
                param = (int(user_id), empty_nl(Decimal(product["price"])), empty_nl(Decimal(product["quantity"])), 'u', int(val))
                

                # сохраняем товар во временной таблице
                try:
                    self.execute('INSERT INTO products_temp(user_id, price, quantity, action, product_id) VALUES(%s, %s, %s, %s, %s)', param)
                     
                    # получаем временный продукт
                    product_temp = self.getProductTemp(user_id, action)
                    
                # Сообщаем пользователю об ошибке базы данных
                except pymysql.err.InternalError:
                    try:
                        self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
                    except Exception as e: print(traceback.format_exc(10))
                    
                except Exception as e: print(traceback.format_exc(10))
                
            else:
                param = (int(user_id), 'c')

                # сохраняем товар во временной таблице
                try:
                     self.execute('INSERT INTO products_temp(user_id, action) VALUES(%s, %s)', param)
                     
                     # получаем временный продукт
                     product_temp = self.getProductTemp(user_id, action)
                     
                # Сообщаем пользователю об ошибке базы данных
                except pymysql.err.InternalError:
                    try:
                        self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
                    except Exception as e: print(traceback.format_exc(10))
                     
                except Exception as e: print(traceback.format_exc(10))
        
        else:
        
            # значения по умалчанию
            price = product_temp["price"]
            quant = product_temp["quantity"]
            kb_mode = product_temp["kb_mode"]
        
            # если есть обновляем
            try:    
                    
                if name == 'num' and product_temp["kb_mode"] == 'p':
                    
                    if product_temp["price"] == '0' and product_temp["flag_price_use"]  == 'n':
                        price = val
                    else:
                        price = product_temp["price"] + val
                        
                    param =  (Decimal(price), 'y', int(user_id), action)
                    
                    self.execute('UPDATE products_temp SET  price = %s, flag_price_use = %s  WHERE user_id = %s AND action = %s', param)
                    
                elif name == 'num' and product_temp["kb_mode"] == 'q': 
                
                    if product_temp["quantity"] == '1' and product_temp["flag_quantity_use"] == 'n':
                        quant = val
                    else:
                        quant = product_temp["quantity"] + val
                        
                    param = (Decimal(quant), 'y', int(user_id), action)
                
                    self.execute('UPDATE products_temp SET  quantity = %s, flag_quantity_use = %s  WHERE user_id = %s AND action = %s', param)
                    
                elif name == 'mode':
               
                    kb_mode = 'p'
                    if product_temp["kb_mode"] == 'p':
                        kb_mode = 'q'
                    
                    param = (kb_mode, int(user_id), action)
                
                    self.execute('UPDATE products_temp SET  kb_mode = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == 'null' and product_temp["kb_mode"] == 'p':
                
                    price = '0';
                    param =  (Decimal(price), int(user_id), action)
                    
                    self.execute('UPDATE products_temp SET  price = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == 'null' and product_temp["kb_mode"] == 'q': 
                
                    quant = '0';
                    param = (Decimal(quant), int(user_id), action)
                
                    self.execute('UPDATE products_temp SET  quantity = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == 'back' and product_temp["kb_mode"] == 'p':
                
                    price = '0'
                    if len(product_temp["price"]) >= 2:
                        price = product_temp["price"][0:-1]
                
                    param =  (Decimal(price), int(user_id), action)
                    
                    self.execute('UPDATE products_temp SET  price = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == 'back' and product_temp["kb_mode"] == 'q': 
                    
                    quant = '0'
                    if len(product_temp["quantity"]) >= 2:
                        quant = product_temp["quantity"][0:-1]
                    
                    param = (Decimal(quant), int(user_id), action)
                
                    self.execute('UPDATE products_temp SET quantity = %s WHERE user_id = %s AND action = %s', param)

                elif name == '.' and product_temp["kb_mode"] == 'p':
                
                    if "." not in price:
                        price += '.'
                
                    param =  (Decimal(price), int(user_id), action)
                    
                    self.execute('UPDATE products_temp SET  price = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == '.' and product_temp["kb_mode"] == 'q': 
                    
                    if "." not in quant:
                        quant += '.'

                    param = (Decimal(quant), int(user_id), action)
                
                    self.execute('UPDATE products_temp SET  quantity = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == '+' and product_temp["kb_mode"] == 'p':
                
                    price = Decimal(product_temp["price"])+1
                
                    param =  (price, int(user_id), action)
                    
                    print(param)
                    
                    self.execute('UPDATE products_temp SET  price = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == '+' and product_temp["kb_mode"] == 'q': 
                    
                    quant = Decimal(product_temp["quantity"])+1
                    
                    param = (quant, int(user_id), action)
                    
                    print(param)
                
                    self.execute('UPDATE products_temp SET  quantity = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == '-' and product_temp["kb_mode"] == 'p':
                
                    if Decimal(product_temp["price"]) >= 1:
                        price = Decimal(product_temp["price"])-1
                
                    param =  (price, int(user_id), action)
                    
                    self.execute('UPDATE products_temp SET  price = %s WHERE user_id = %s AND action = %s', param)
                    
                elif name == '-' and product_temp["kb_mode"] == 'q': 
                    
                    if Decimal(product_temp["quantity"]) >= 1:
                        quant = Decimal(product_temp["quantity"])-1
                    
                    param = (quant, int(user_id), action)
                
                    self.execute('UPDATE products_temp SET  quantity = %s WHERE user_id = %s AND action = %s', param)
               
            # Сообщаем пользователю об ошибке базы данных
            except pymysql.err.InternalError:
                try:
                    self.bot.send_message(self.message.chat.id, self.db_error_text, parse_mode='HTML')
                except Exception as e: print(traceback.format_exc(10)) 
                
            except Exception as e: print(traceback.format_exc(10))
            
        return {'price': price, 'quant': quant, "action": action, "kb_mode": kb_mode}