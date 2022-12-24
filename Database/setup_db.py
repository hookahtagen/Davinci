import sqlite3 as s

#Connect to the database; if non existing, it will be created
connect = s.connect("FaceEncodings.db", isolation_level='immediate')

cursor = connect.cursor()

person_field = "id INTEGER PRIMARY KEY, name TEXT, age INTEGER, address TEXT, phone TEXT"
face_encoding = ""