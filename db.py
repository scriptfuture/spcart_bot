# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pymysql.cursors
import traceback

class DB:

    def __init__(self, host, user, password, db):
        
        self.host=host
        self.user=user
        self.password=password
        self.db=db
    

    def connect(self):
        """ Connect to MySQL database """
        
        # mysql-python
        try:
            # Connect to the database
            self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.DatabaseError as err:
            print("Error: ", traceback.format_exc(10))

    def close(self):
        try:
           self.connection.close()
           
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.DatabaseError as err:
            print("Error: ", err)
            raise pymysql.DatabaseError("DatabaseError")
        
    def fetchone(self, sql, options):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute(sql, options)
                result = cursor.fetchone()
            
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.DatabaseError as err:
            print("Error: ", err)
            raise pymysql.DatabaseError("DatabaseError")

        return result
   
    def fetch(self, sql, options):
    
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute(sql, options)
                result = cursor.fetchall()
                
        # Сообщаем пользователю об ошибке базы данных
        except pymysql.DatabaseError as err:
            print("Error: ", err)
            raise pymysql.DatabaseError("DatabaseError")

        return result
   
    def execute(self, sql, options):
    
        try:
        
            with self.connection.cursor() as cursor:
                cursor.execute(sql, options)

            self.connection.commit()

        # Сообщаем пользователю об ошибке базы данных
        except pymysql.DatabaseError as err:
            print("Error: ", err)
            raise pymysql.DatabaseError("DatabaseError")