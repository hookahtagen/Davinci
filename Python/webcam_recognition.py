'''
    Author:     Hendrik Siemens
    Date:       2022-12-30
    
    Version:    0.0.1
    
    WebCam Face Recognition
        For full documentation and usage info, see:

        What does this program do?
            This program uses the webcam to detect faces and recognize them. If a face is known to the system,
            it will display the name of the person. Otherwise the face is unknown, it will display "Unknown".
            
            The Face Recognition library is used to detect and recognize faces. The library is based on the
            dlib library. The dlib library is used to detect faces. It is based on the Histogram of Oriented
            Gradients (HOG) feature combined with a linear classifier, an image pyramid, and sliding window
            detection scheme. The model has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark.
            
            
'''

from glob import glob
import os
import sqlite3 as s
import sys
import numpy as np
import cv2
import face_recognition
from types import SimpleNamespace

def set_global_env( ) -> SimpleNamespace:
    '''
        Explanation:
            This function sets the global environment.
            
        Parameters:
            None
        
        Returns:
            global_env: SimpleNamespace
    '''
    
    # Declaring a global Namespace
    global global_env
    global_env = SimpleNamespace( )
    
    # General variables
    global_env.process_this_frame: bool = True
    
    # Webcam variables
    global_env.device_id: int = 0
    global_env.capture = cv2.VideoCapture( global_env.device_id )
    global_env.webcam_id: int = 0
    global_env.webcam_width: int = 640
    global_env.webcam_height: int = 480
    global_env.resize_factor: int = 0.25
    
    
    # Database variables
    global_env.db_path: str = '/home/hendrik/Documents/Davinci/Database/'
    global_env.db_name: str = 'FaceEncodings.db'
    
    return global_env

def connect_to_db( gloval_env: object ) -> list[ s.Connection, s.Cursor ]:
    '''
        Explanation:
            This function connects to the database and returns the connection and cursor.
            
        Parameters:
            gloval_env: object
            
        Returns:
            list[ s.Connection, s.Cursor ]
            
    '''
    
    global global_env
    
    db_name: str = global_env.db_path + global_env.db_name
    conn = s.connect( db_name )
    cursor = conn.cursor( )
    
    return conn, cursor


def process_video( gloval_env: object ) -> None:
    global global_env
    
 
    while True:
        # Grab a single frame of video
        ret, frame = global_env.capture.read( )
        
        if global_env.process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize( frame, ( 0, 0 ), fx=global_env.resize_factor, fy=global_env.resize_factor )
            
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[ :, :, ::-1 ]
            
            # Find all the faces and face encodings in the current frame of video
            if sys.argv[ 1 ] == '1':
                face_locations = face_recognition.face_locations( rgb_small_frame, number_of_times_to_upsample=1, model='cnn' )
            else:
                face_locations = face_recognition.face_locations( rgb_small_frame, number_of_times_to_upsample=2, model='hog' )
            
            face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations )
            
        global_env.process_this_frame = not global_env.process_this_frame
        
        # Display the results
        for listitem in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            # face_locations[0] = top
            # face_locations[1] = right
            # face_locations[2] = bottom
            # face_locations[3] = left
            top = listitem[ 0 ] * 4
            right = listitem[ 1 ] * 4
            bottom = listitem[ 2 ] * 4
            left = listitem[ 3 ] * 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    global_env.capture.release()
    cv2.destroyAllWindows()
            
            
        
    

def main( ) -> None:
    global global_env
    global_env = set_global_env( )
    
    process_video( global_env )


if __name__ == "__main__":
    
    global global_env
    global_env = set_global_env( )
    
    conn, cursor = connect_to_db( global_env )
    
    if not conn or not cursor:
        print( 'Error connecting to database' )
        sys.exit( 1 )
    
    main( )