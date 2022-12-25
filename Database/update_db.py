import sqlite3 as s
import numpy as np
import os
import time
import sys
import face_recognition

check_operand = False
db_name = 'FaceEncodings'

#List of currently supported commands
supported_commands = [
    "add",
    "del",
    "update"
]

#Check if the entered command is a valid command and checks for any errors
#that might occur.
try:
    if ".db" in sys.argv[ 1 ]: db_name = sys.argv[ 1 ]
    else: print( f'Theres a problem with the entered database_file. Please try again.' ), sys.exit( 1 )
    if sys.argv[ 2 ] in supported_commands:
        check_operand = True
except IndexError:
    print( f'You entered no or too few arguments. Please try again.' )
    sys.exit( 1 )


# Database name = FaceEncodings.db
# Num of tables = 2
# table names = 'persons', 'faceencodings'
# structure of 'persons': id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, address TEXT, city TEXT, country TEXT
# structure of 'faceencodings': id INTEGER PRIMARY KEY, person_id INTEGER, data BLOB, timestamp REAL, FOREIGN KEY (person_id) REFERENCES persons(id)

def add_menu( num ):
    add_menu = [
        f'You want to add { num } pictures.',
        f'Please enter now a path, where the files are located and then hit ENTER:',
        f'\nThe filenames of the pictures you want to add should have the following format: forename-surename-index.jpg',
        f'Please paste them separated by a semicolon >>(;)<<. For example: jon-doe-1.jpg, jon-doe-2.jpg, ...'
    ]
    return add_menu

def clear_screen( ):
    os.system( 'clear' )

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

def get_face_encodings( file_path = None, filename_list = None, known_face_encodings = [ ] ):
    """ 
    Explanation: 
        This function reads all the images in the given path, extracts their face encodings and names,
        and stores them in the given lists.
    
    Parameters:
        file_path (str): The path to the directory containing the images.
        known_face_encodings (list): A list to store the face encodings in.
    
    Returns:
        tuple: A tuple containing the updated lists of face encodings and names. 
    """

    clear_screen()
    if filename_list is None or file_path is None or None in filename_list:
        print( f'Image List not found or corrupted. Please try again.')
        sys.exit( 1 )

    
    #Get all Pictures under the given path
    #Store them in a list with file-endings
    
    for name in filename_list:
        path = file_path + name

        tmp1 = face_recognition.load_image_file(path)
        tmp2 = face_recognition.face_encodings(tmp1)[0]

        locals()[name.replace('.jpg','_image')] = tmp1
        locals()[name.replace('.jpg','_encoding')] = tmp2
    
    for listitem in filename_list:
        known_face_encodings.append(str(listitem.replace('.jpg','_encoding').replace(' ','_')))

    print("TestTestTest***********************")
    print(known_face_encodings)
    print("TestTestTest**********************")

    return known_face_encodings


def prnt_menu( add_menu_a, num1 = 0, num2 = 0 ):
    '''
    Explanation: 
        Prints the menu in the function add_person( )
    
    Parameters:
        add_menu_a: list of strings containing menu texts
        num1 = int: which line to display first
        num2 = int: which line to display second    
    Returns:
        None
    '''  

    print( add_menu_a[ num1 ] )
    print( add_menu_a[ num2 ] )

def add_person( ):
    num = int( input( 'How many pictures do you want to add? ' ) )
    add_menu_a = add_menu( num )

    print( '\n\n' )
    prnt_menu( add_menu_a, 0, 1 )
    path=input( '' )
    prnt_menu( add_menu_a, 2, 3 )

    file_names = input( '\n\nFilenames: ' )
    filenames_list=[ ]; filenames_list=file_names.split( ',' )
    filenames_list = [ filename.strip( ) for filename in filenames_list ]
    
    p_face_encodings = get_face_encodings( path, filenames_list )

    print( p_face_encodings )

    
    #Filenames list is no longer needed in the future.
    #The user has just to specify a path via gui, and that chosen path is stored under a variable
    

def del_person( ):
    '''
    Explanation: 
        This function deletes a person from the database and all corresponding data
        by any given key values for the database call, such as name, id, address and so.

        This functions also deletes the corresponding face_encodings from the table 'faceencodings'
    
    Parameters:
        Any key from sqlite3 database table 'persons'.
    
    Returns:
        None
    '''
    a=0

def main( ):
    clear_screen( )
    add_person( )
    
    

if __name__ == '__main__':
    if check_operand and len( sys.argv ) == 3:
        main( )
    else:
            print( 'Bad argument or too many arguments! Please check your entered command again and then try again' )
            if check_operand == False: 
                print( f'\n*{ sys.argv[2] }* isn\'t a supported command.\n\n' )
            if len( sys.argv ) > 3: 
                print( f'You entered too many arguments. You entered { len( sys.argv ) }' )
            print( f'Supported Commands:\n { supported_commands }' )
            sys.exit( 0 )       

#EOF

