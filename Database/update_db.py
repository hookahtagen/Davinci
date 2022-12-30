import sqlite3 as s
import numpy as np
import os
import time
import sys
import face_recognition
import cv2

from mtcnn import MTCNN

# Database name = FaceEncodings.db
# Num of tables = 2
# table names = 'persons', 'faceencodings'
# structure of 'persons': id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, address TEXT, city TEXT, country TEXT
# structure of 'faceencodings': id INTEGER PRIMARY KEY, person_id INTEGER, reference_flag INTEGER, data BLOB, FOREIGN KEY (person_id) REFERENCES persons(id)

def clear_screen( ) -> None:
    '''
    Explanation:
        This function clears the screen.
    Parameters:
        None
    Returns:
        None
    '''
    os.system( 'clear' )


def connect_to_db( db_name ) -> tuple:
    '''
    Explanation: 
        This function sets the connection to the database and
        creates cursor,and before that it chacks if the given database name is a valid database-file in the database directory of the repo. 
        Before returning it checks if the connection is established successfully.
        If not, the program will exit with an error message.
    
    Parameters:
        string db_name 
    
    Returns:
        return conn, cursor (object, object)
    '''
    db_path = '/home/hendrik/Dokumente/Davinci/Database'
    db_name = db_name + '.db'
    if db_name in os.listdir( db_path ):
        conn = s.connect( f'{ db_path }/{ db_name }' )
        cursor = conn.cursor( )
        if conn and cursor:
            print( f'{ db_name } was successfully connected' )
            time.sleep( 3 )
            return conn, cursor
        else:
            print( f'{ db_name } could not be connected' )
            sys.exit( 1 )
    else:
        print( f'{ db_path }/{ db_name } does not exist' )
        print( f'{ db_name } does not exist' )
        sys.exit( 0 )


def get_personal_details() -> tuple:
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
    
def get_face_locations(image):
    
    # Create an MTCNN detector
    detector = MTCNN()

    # Load the input image
    image = cv2.imread(image)

    # Detect faces in the image
    face_locations = detector.detect_faces(image)

    return face_locations


def get_face_encodings( name = None ) -> dict:
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

    path_of_pics = '/home/hendrik/Dokumente/Davinci/Database/FaceEncodings'
    path_of_pics = path_of_pics + '/' + name
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
                #face_locations = face_recognition.face_locations( image )

                face_locations = get_face_locations( image )

                if len( face_locations ) > 1:
                    print( f'There are more than one face in { filename }' )
                    print( 'Skipping ...')
                    continue
                elif len( face_locations ) == 0:
                    print( f'There are no faces in { filename }' )
                    print( 'Skipping ...' )
                    continue
                else: 
                    face_encoding = face_recognition.face_encodings( image, face_locations, num_jitters = 10 )[ 0 ]
                    processed_faces[ name ].append( face_encoding )
                    print( f'Face encoding of { filename } was processed' )
    else:
        print( 'No path was given or the path is wrong!' )
        print( 'Please check if the path is correct!' )
        sys.exit( 1 )
    return processed_faces


def print_warning( ) -> None:
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
    print( 'Pleae make sure that the pictures are in the right folder and that the folder is named correctly.' )
    
    #Ask the user to confirm the file structure.
    while True:
        answer = input( 'Do you want to continue? (y/n): ' )
        if answer.lower() == 'y':
            break
        elif answer.lower() == 'n':
            print( 'Exiting ...' )
            sys.exit( 1 )
        else:
            print( 'Please enter y or n' )
            continue


def try_again( index=0 ) -> None:
    '''
    Explanation:
        This function asks the user if he wants to try again or not.
        If the user wants to try again, the function calls the add_person function.
        If the user does not want to try again, the function exits the program.
    Parameters:
        index = int: index of the function
    Returns:
        None
    '''

    if index == 1:
        print( 'The data was not added correctly!' )
        operand = 'try again'
    elif index == 2:
        print( 'The data was not updated correctly!' )
        operand = 'update the person again'
    elif index == 3:
        print( 'The data was added correctly!' )
        operand = 'add another person'

    while True:
        answer = input( f'Do you want to {operand}? (y/n): ' )
        if answer.lower() == 'y':
            add_person( conn, cursor )
            break
        elif answer.lower() == 'n':
            break
        else:
            print( 'Please enter y or n' )
            continue


def check_data( conn: object, name: str, age: int, address: str, phone_number: str ) -> None:
    '''
    Explanation:
        This function checks if the data is correct and asks the user if he wants to add the data to the database or not.
        If not the user can try again.
    Parameters:
        name = str: name of the person
        age = int: age of the person
        address = str: address of the person
        phone_number = str: phone number of the person
    Returns:
        None
    '''

    clear_screen( )

    print( f'Name: { name }' )
    print( f'Age: { age }' )
    print( f'Address: { address }' )
    print( f'Phone number: { phone_number }' )

    while True:
        answer = input( '\nIs the data correct? (y/n): ' )
        if answer.lower() == 'y':
            #Data is correct
            break
        elif answer.lower() == 'n':
            #Data is not correct
            conn.rollback()
            try_again(1)
            break
        else:
            print( 'Please enter y or n' )
            continue


def add_person( conn: object, cursor: object) -> None:
    """ 
    Explanation: 
        General explanation: 
        This function adds a person, where multiple persons could get the same name, to the database and all corresponding data
        by any given key values for the database call, such as name, id, address and so.
        
        more specific explanation:
        This function adds a person to the database and all corresponding data by any given key values for the database call, such as name, id, address and so.
        This data must be queried from the user by the function get_personal_details( ).

        After that the gotten name is used to get the face encodings of the person by the function get_face_encodings( ).
        The first face encoding of the person is then gonna be flagged as the main face encoding of the person (multiple persons could have the same name but not the same face encoding).

        After this the function adds the personal details to the table 'persons' and the face encodings to the table 'faceencodings' in the database.
        To make sure the face encodings are added to the correct person the function adds the id of the person to the table 'faceencodings' as well.

        After everything is commited to the database the function then checks if the data was added correctly by the function check_data( )
        If the data was added correctly the function prints a success message asks the user if he wants to add another person.
        If the data was not added correctly the function prints an error message and asks the user if he wants to try again.

        The function also handles errors such as a value error or a s error.
        
    Parameters:
        None  
    
    Returns:
        None

    Notes:
        processed_faces = dictionary: dictionary with the filename as key and the face encoding as values.

        The sql querys are both in seperate variables to make the code more readable.
        To get the id the whole data gotten from the user is used to query the database.
    """

    print_warning( )

    clear_screen( )

    #Get the personal details of the person
    name, age, address, phone_number = get_personal_details( )

    #Get the face encodings of the person
    processed_faces = get_face_encodings( name )

    #Add the personal details to the table 'persons'
    sql_query = 'INSERT INTO persons ( name, age, address, phone ) VALUES ( ?, ?, ?, ? )'
    cursor.execute( sql_query, ( name, age, address, phone_number ) )

    #Get the id of the person
    last_id = cursor.lastrowid

    

    #Add the face encodings to the table 'faceencodings'. Check if any of the processed face encodings is already in the database and if so don't adds it to the database
    for filename, face_encoding in processed_faces.items( ):
        sql_query = 'SELECT id FROM faceencodings WHERE face_encoding = ?'
        cursor.execute( sql_query, ( face_encoding, ) )
        result = cursor.fetchone( )
        if result is None:
            sql_query = 'INSERT INTO faceencodings ( id, face_encoding ) VALUES ( ?, ? )'
            cursor.execute( sql_query, ( last_id, face_encoding ) )

    check_data( conn, name, age, address, phone_number )
    #Commit the changes to the database
    conn.commit( )


def del_person( ) -> None:
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


def main( ) -> None:
    #Ask the user to input a database name and store it under db_name and check if the entered name is a valid database name
    db_name = input( 'Please enter a database name: ' )

    #Connect to the database:
    conn, cursor = connect_to_db( db_name )

    #Clear the screen befor continuing
    clear_screen( )

    #Add or update a person to/in the database
    add_person( conn, cursor)
    
    
#Run the main function if the program is run directly
if __name__ == '__main__':

    #Run the main function
    main( )
    


