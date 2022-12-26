'''
    Explanation:
        This is a program that creates a database with a name given by the user
        and creates a table called 'persons' with the following columns: id INTEGER (primary key), name TEXT, age INTEGER, address TEXT, phone TEXT
        and a table called 'faceencodings' with the following columns: id INTEGER (primary key), person_id(foreign key to id (table 'persons')), data

    Task for Copilot: 
        1. Make a program that asks the user for a name and creates a database with that name
        2. create a table called 'persons' with the following columns: id INTEGER (primary key), name TEXT, age INTEGER, address TEXT, phone TEXT
        3. create a table called 'faceencodings' with the following columns: id INTEGER (primary key), person_id(foreign key to id (table 'persons')), data

    List of all needed imports:
        import sqlite3
        import os
        import sys
        import numpy as np
        import time
'''

import sqlite3 as s
import os
import sys
import numpy as np
import time


def connect_to_db( db_name ):
    '''
    Explanation: 
        This function sets the connection to the database and
        creates cursor.
    
    Parameters:
        string db_name 
    
    Returns:
        return conn, cursor (object, object)
    '''

    conn = s.connect( db_name ) 
    cursor = conn.cursor( )
    return conn, cursor

def main( ):
    db_name = input( 'Please enter the name of the database you want to create: ' )
    conn, cursor = connect_to_db( db_name )
    cursor.execute( 'CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, address TEXT, phone TEXT)' )
    cursor.execute( 'CREATE TABLE IF NOT EXISTS faceencodings (id INTEGER PRIMARY KEY, person_id INTEGER, data BLOB, timestamp REAL, FOREIGN KEY (person_id) REFERENCES persons(id))' )
    conn.commit( )
    #Check if all commits were made successfully and display a proper message to the user

    
    conn.close( )

if __name__ == '__main__':
    main( )




