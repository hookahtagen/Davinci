from __future__ import print_function
import cv2
import argparse
import keras
import numpy as np
from os import listdir
from os.path import isfile, join

model = keras.models.load_model('face_recognition_model.h5')
path ="/home/hendrik/Dokumente/Davinci/FaceEncodings/"

labels = []
file_list= [f for f in listdir(path) if isfile(join(path, f))]
for listitem in file_list:
    labels += [listitem.split('.')[0]]

# Function that detects and displays faces and eyes in a given frame
def detectAndDisplay2(frame):
    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Equalize the histogram of the grayscale frame
    frame_gray = cv2.equalizeHist(frame_gray)
    # Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    # For each detected face
    for (x,y,w,h) in faces:
        # Calculate the center of the face
        center = (x + w//2, y + h//2)
        # Draw an ellipse around the face
        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        # Extract the region of interest (ROI) for the face
        faceROI = frame_gray[y:y+h,x:x+w]
        # In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        # For each detected eye
        for (x2,y2,w2,h2) in eyes:
            # Calculate the center of the eye
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            # Calculate the radius of the eye
            radius = int(round((w2 + h2)*0.25))
            # Draw a circle around the eye
            frame = cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
        # Display the frame with the detected faces and eyes
    cv2.imshow('Capture - Face detection', frame)

def detectAndDisplay(frame):
    

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Equalize the histogram of the grayscale frame
    frame_gray = cv2.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    # For each detected face
    for (x,y,w,h) in faces:
        # Calculate the center of the face
        center = (x + w//2, y + h//2)
        # Draw an ellipse around the face
        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        # Extract the region of interest (ROI) for the face
        faceROI = frame_gray[y:y+h,x:x+w]
        # Resize the ROI to the input shape of the trained model
        faceROI = cv2.resize(faceROI, (128, 128))
        # Convert the ROI to a 4D tensor
        faceROI = frame_gray[y:y+h,x:x+w]
        # Normalize the ROI
        faceROI = faceROI / 255.0
        # Use the trained model to predict the name of the face
        prediction = model.predict(faceROI)
        # Get the index of the highest prediction
        prediction_index = np.argmax(prediction)
        # Get the name of the face
        name = labels[prediction_index]
        # If the prediction is less than the threshold, the face is unknown
        if prediction[0][prediction_index] < 50:
            name = "Unknown"
        # Display the label below the face
        cv2.putText(frame, name, (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    # Display the frame with the detected faces and labels
    cv2.imshow('Capture - Face detection', frame)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='/home/hendrik/Dokumente/Davinci/haarcascade_frontalface_default.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='/home/hendrik/Dokumente/Davinci/haarcascade_eye.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

# Load the face and eye cascades
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()
if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

# Set the camera device number
camera_device = args.camera

# Open the video capture
cap = cv2.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

# Continuously capture frames from the video stream
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    # If the frame could not be read, break the loop
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    # Detect and display faces and eyes in the frame
    detectAndDisplay(frame)
    # If the 'ESC' key is pressed, break the loop
    if cv2.waitKey(10) == 27:
        break