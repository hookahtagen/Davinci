'''
    This is just a test for different methods of getting
    face locations of an image.
'''


import cv2  
import face_recognition
import sys
import time
import os


path_to_image = '/home/hendrik/Documents/Davinci/Testarea/test1.jpg' 




def get_location( image: object ) -> list[ int, int, int, int ]:
    face_location = face_recognition.face_locations( image, number_of_times_to_upsample=1, model='hog' )
    
    return face_location

def main() -> None:

    # Load the image
    image = cv2.imread( path_to_image )
    image = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )
    
    # Get the locations of the face in the image
    face_location = get_location( image )
    
    top = face_location[ 0 ] 
    right = face_location[ 1 ]
    bottom = face_location[ 2 ]
    left = face_location[ 3 ]
    
    # Log the coordinates of the face
    print( 'Face coordinates are: ' )
    print( 'top: ' + str( top ) )
    print( 'right: ' + str( right ) )
    print( 'bottom: ' + str( bottom ) )
    print( 'left: ' + str( left ) )
    
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.imshow( 'image', image )
    
    if cv2.waitKey( 0 ) & 0xFF == ord( 'q' ):
        cv2.destroyAllWindows( )
    
    
    

if __name__ == '__main__':
    main()