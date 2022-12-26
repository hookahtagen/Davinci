import sqlite3 as s
import numpy as np
import os
import time
import sys
import face_recognition

check_operand = True
db_name = 'FaceEncodings'

#List of currently supported commands
supported_commands = [
    "add",
    "del",
    "update"
]

#Check if the entered command is a valid command and checks for any errors
#that might occur.

# try:
#     if ".db" in sys.argv[ 1 ]: db_name = sys.argv[ 1 ]
#     else: print( f'Theres a problem with the entered database_file. Please try again.' ), sys.exit( 1 )
#     if sys.argv[ 2 ] in supported_commands:
#         check_operand = True
# except IndexError:
#     print( f'You entered no or too few arguments. Please try again.' )
#     sys.exit( 1 )


# Database name = FaceEncodings.db
# Num of tables = 2
# table names = 'persons', 'faceencodings'
# structure of 'persons': id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, address TEXT, city TEXT, country TEXT
# structure of 'faceencodings': id INTEGER PRIMARY KEY, person_id INTEGER, data BLOB, timestamp REAL, FOREIGN KEY (person_id) REFERENCES persons(id)

def add_menu( num = 0):
    add_menu = [
        f'You want to add { num } pictures.',
        f'Please enter now a path, where the pictures are located and then hit ENTER:',
        f'\nEnter the name of the person in the following format: forename surename',
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

def get_face_encodings( path_of_pics = None , name = None ):
    '''
    Explanation:
        This function gets all face encodings of a given person under a given path.
        It returns a dictionary with the filename as key and the face encoding as value.
    Parameters:
        path_of_pics = string: path to the pictures
        name = string: name of the person
    Returns:
        processed_faces = dictionary: dictionary with the filename as key and the face encoding as value.
    '''

    name = name.lower().replace( ' ', '-' ).replace( '\n', '' )
    processed_faces = { }

    if path_of_pics and os.listdir( path_of_pics ):

        for listitem in os.listdir( path_of_pics ):
            tmp = listitem.replace( '.jpg', '' ).replace( ' ', '-' )
            if tmp not in processed_faces and name in tmp:
                tmp0 = name
                processed_faces[tmp0] = []
            else:
                continue

        for filename in os.listdir( path_of_pics ):
            filename = filename.lower().replace( ' ', '-' ).replace( '\n', '' )
            if filename.endswith( '.jpg' ) and name in filename:
                tmp1 = filename.replace( '-', ' ' )
                image = face_recognition.load_image_file( f'{ path_of_pics }/{ tmp1 }' )
                face_locations = face_recognition.face_locations( image )
                if len( face_locations ) > 1:
                    print( f'There are more than one face in { filename }' )
                    continue
                elif len( face_locations ) == 0:
                    print( f'There are no faces in { filename }' )
                    continue
                else:
                    face_encoding = face_recognition.face_encodings( image, face_locations, num_jitters = 50 )[ 0 ]
                    processed_faces[ name ].append(face_encoding)
                    print( f'Face encoding of { filename } was processed' )
    else:
        print( 'No path was given or the path is wrong!' )
        sys.exit( 1 )
    return processed_faces

def prnt_menu( add_menu_a, num1 = 0, num2 = None ):
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

def add_person( conn = None, cursor = None):
    """ 
    Explanation: 
        This function adds a person to the database and all corresponding data
        by any given key values for the database call, such as name, id, address and so.
        
    
    Parameters:
        None  
    
    Returns:
        None
    """    

    num = int( input( 'How many pictures do you want to add? ' ) )
    add_menu_a = add_menu( num )

    #Ask the user to input a path and store it under path
    print( '\n\n' )
    prnt_menu( add_menu_a, 0, 1 )
    path=input( '' )
    prnt_menu( add_menu_a, 0, 2 )

    #Ask the user to input a name and store it under file_names
    name = input( '\n\nName of person: ' )
    
    #Get all faceencodings of the given person under the given path.
    processed_faces = get_face_encodings( path, name )
    
    print( processed_faces )
    
    

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
    #Ask the user to input a database name and store it under db_name and check if the entered name is a valid database name
    db_name = input( 'Please enter a database name: ' )

    #Connect to the database:
    conn, cursor = connect_to_db( db_name )
    clear_screen( )
    add_person( conn, cursor)
    
    

if __name__ == '__main__':
    if check_operand: #and len( sys.argv ) == 2:
        main( )
    else:
            print( 'Bad argument or too many arguments! Please check your entered command again and then try again' )
            if check_operand == False: 
                print( f'\n*{ sys.argv[2] }* isn\'t a supported command.\n\n' )
            if len( sys.argv ) > 3: 
                print( f'You entered too many arguments. You entered { len( sys.argv ) }' )
            print( f'Supported Commands:\n { supported_commands }' )
            sys.exit( 0 )       


