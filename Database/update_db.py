import sqlite3 as s
import numpy as np
import os
import time
import sys
import face_recognition


# Database name = FaceEncodings.db
# Num of tables = 2
# table names = 'persons', 'faceencodings'
# structure of 'persons': id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, address TEXT, city TEXT, country TEXT
# structure of 'faceencodings': id INTEGER PRIMARY KEY, person_id INTEGER, data BLOB, timestamp REAL, FOREIGN KEY (person_id) REFERENCES persons(id)



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

def add_menu( num = 0):
    add_menu = [
        f'You want to add { num } pictures.',
        f'Please enter now a path, where the pictures are located and then hit ENTER:',
        f'\nEnter the name of the person in the following format: forename surename',
    ]
    return add_menu
def ad_personal_details():
    '''
    Explanation:
        This function asks the user for the personal details of the person.
        The user is asked for age, address and phone number which are stored in separate variables.
    Parameters:
        None
    Returns:
        name, age, address, phone_number
    '''

    name = input( 'Name: ' )
    age = input( 'Age: ' )
    address = input( 'Address: ' )
    phone_number = input( 'Phone number: ' )
    return name, age, address, phone_number
    

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

def print_warning( ):
    '''
    Explanation:
        This function prints a warning to the user and displaying the needed file structure for importing the pictures
        into the program and tells the user to follow the file structure precisely.
        File structure:
            - path
                forename-surename 1:
                    forename-surename-1.jpg
                    forename-surename-2.jpg
                    forename-surename-3.jpg
                    ...
                forename-surename 2:
                    forename-surename 2-1.jpg
                    forename-surename 2-2.jpg
                    forename-surename 2-3.jpg
                    ...
                ...
    Parameters:
        None
    Returns:
        None
    '''

    file_structure = [
        'File structure:',
        '- path',
        '    forename-surename 1:',
        '        forename-surename-1.jpg',  
        '        forename-surename-2.jpg',
        '        forename-surename-3.jpg',
        '        ...',
        '    forename-surename 2:',
        '        forename-surename 2-1.jpg',
        '        forename-surename 2-2.jpg',
        '        forename-surename 2-3.jpg',
        '        ...',
        '    ...',
    ]

    print( 'WARNING: Please follow the file structure precisely!' )
    print( 'File structure:' )
    for item in file_structure:
        print( item )
   

    
def change_person( conn = None, cursor = None):
    """ 
    Explanation: 
        This function adds a person to the database and all corresponding data
        by any given key values for the database call, such as name, id, address and so.
        The function also adds the face encodings of the person to the database.
    Parameters:
        None  
    
    Returns:
        None
    """

    #Print a warning to the user displaying the needed file structure and then ask the user for the path to the pictures.
    print_warning()

    #Ask the user for the path to the pictures.
    path=input( '\n\nPath to pictures:' )

    #Ask the user for the personal details of the person.
    name, age, address, phone = ad_personal_details()

    #Get all faceencodings of the given person under the given path.
    processed_faces = get_face_encodings( path, name )

    #Insert the person and its data into the database; avoid string formatting to build the sql query. Keep the previously described database structure in mind and insert the face encodings into the database. Commit the changes to the database.
    cursor.execute( 'INSERT INTO persons(name, age, address, phone) VALUES(?, ?, ?, ?)', (name, age, address, phone) )
    conn.commit( )
    
    #Get the id of the person from the database.
    cursor.execute( 'SELECT id FROM persons WHERE name = ?', (name, ) )
    person_id = cursor.fetchone( )[ 0 ]

    #Insert the face encodings into the database.
    for face_encodings in processed_faces[ name ]:
        cursor.execute( 'INSERT INTO faceencodings(person_id, data) VALUES(?, ?)', (person_id, face_encodings.tobytes( ) ) )
        conn.commit( )

    #Check if the person was added to the database successfully and print a message to the user
    cursor.execute( 'SELECT * FROM persons WHERE name = ?', (name, ) )
    if cursor.fetchone( ):
        print( f'{ name } was added to the database successfully' )
    else:
        print( f'{ name } was not added to the database successfully' )



    


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

    #To be implemented
    a=0

def main( ):
    #Ask the user to input a database name and store it under db_name and check if the entered name is a valid database name
    db_name = input( 'Please enter a database name: ' )

    #Connect to the database:
    conn, cursor = connect_to_db( db_name )

    #Clear the screen befor continuing
    clear_screen( )

    #Add or update a person to/in the database
    change_person( conn, cursor)
    
    
#Run the main function if the program is run directly
if __name__ == '__main__':

    #Run the main function
    main( )
    


