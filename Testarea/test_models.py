'''
    This is just a test for different methods of getting
    face locations of an image.
'''

import cv2  
import face_recognition
import sys
import time
import os
from PIL import Image
import numpy as np

path_to_image = '/home/hendrik/Documents/Davinci/Testarea/test1.jpg' 
exit_flag: bool = False


def resize_image( image: object ):
    height, width = image.shape[ :2 ]
    scale_factor = min( 1024 / width, 768 / height )# Calculate the scaling factor
    resized_image = cv2.resize(image, None, fx = scale_factor, fy = scale_factor, interpolation = cv2.INTER_LINEAR)# Resize the image
    return resized_image

def scale_image( image: object, direction: str ):
    
    factor = 4
    div_factor = 0.25
    
    if direction == 'up':
        small_image = cv2.resize( image, ( 0, 0 ), fx = factor, fy = factor )
    small_image = cv2.resize( image, ( 0, 0 ), fx = div_factor, fy = div_factor )
    return small_image


def get_location( image: object ):
    image = scale_image( image, 'down' )
    face_location = face_recognition.face_locations( image, number_of_times_to_upsample=3, model='hog' )
    
    # Scale up the face locations in 'face_location' by a factor of 4
    for i, value in enumerate( face_location ):
        top = face_location[ i ] [ 0 ] 
        right = face_location[ i ] [ 1 ]
        bottom = face_location[ i ] [ 2 ]
        left = face_location[ i ] [ 3 ]
        
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        face_location[ i ] = [ top, right, bottom, left ]
    
    
    image = scale_image( image, 'up' )
    return face_location

def main() -> None:

    # Load the image
    image = cv2.imread( path_to_image )
    
    # while True:
    #     cv2.imshow( 'image', resize_image( image ) )
        
    #     if cv2.waitKey( 0 ) & 0xFF == ord( 'q' ):
    #         cv2.destroyAllWindows( )
    #         flag = True
    #         break
    
    if exit_flag:
        sys.exit( )
        
    #image = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )
    
    # Get the locations of the face in the image
    face_location = get_location( image )
    
    for i, value in enumerate( face_location ):
        top = face_location[ i ] [ 0 ] 
        right = face_location[ i ] [ 1 ]
        bottom = face_location[ i ] [ 2 ]
        left = face_location[ i ] [ 3 ]
        
        # Log the coordinates of the face
        print( f'\nFace { i+1 } coordinates are: ' )
        print( 'top: ' + str( top ) )
        print( 'right: ' + str( right ) )
        print( 'bottom: ' + str( bottom ) )
        print( 'left: ' + str( left ) )
        
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        #cv2.namedWindow("Image Viewer", cv2.WINDOW_AUTOSIZE)
        #image = cv2.cvtColor( image, cv2.COLOR_RGB2BGR)
    
    
    cv2.imshow( 'img', resize_image( image ) )
    
    if cv2.waitKey( 0 ) & 0xFF == ord( 'q' ):
        cv2.destroyAllWindows( )
    
    
    

if __name__ == '__main__':
    main()