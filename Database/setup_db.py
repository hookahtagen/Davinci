import sqlite3 as s
import numpy as np
import os
import time

def clear_screen():
    os.system('clear')

def prnt_message(num=0):
    message_list = {
        "0":"Error!",
        "1":"Connection successfull!",
        "2":"Exiting now!"
    }
    print("******************")
    print(message_list[str(num)])
    print("******************")


#Connect to the database; if non existing, it will be created
connect = s.connect("FaceEncodings.db", isolation_level='immediate')
clear_screen()
prnt_message(1)
time.sleep(2)
cursor = connect.cursor()

person_field = "id INTEGER PRIMARY KEY, name TEXT, age INTEGER, address TEXT, phone TEXT"
face_encoding = "id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, encoding BLOB"

#create two tables containing the keys listed above




clear_screen()
prnt_message(2)