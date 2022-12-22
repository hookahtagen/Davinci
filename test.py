import cv2
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from types import SimpleNamespace

def set_Namespace():
    Global = SimpleNamespace()
    
    #TODO
    #
    #Set fixed variables as paths and so to the "Global" Namespace
    #
    #

    return Global

# create a face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# get the path to the directory containing the face images
face_dir = "/home/hendrik/Dokumente/Davinci/FaceEncodings/"

# create a list to store the labels and the corresponding face images
le = LabelEncoder()
labels = []
face_images = []

# iterate over the face images in the directory
for file in os.listdir(face_dir):
    # extract the label from the filename
    label = file.split('.')[0]
    
    # read the face image
    face_image = cv2.imread(os.path.join(face_dir, file))
    
    # convert the face image to grayscale
    face_image_gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    
    # add the label and the face image to the list
    labels.append(label)
    face_images.append(face_image_gray)

# create a label encoder
le = LabelEncoder()

# fit the label encoder on the labels
le.fit(labels)

# encode the labels
encoded_labels = le.transform(labels)


# train the face recognizer
face_recognizer.train(face_images, encoded_labels)

# read the input image
src = cv2.imread("/home/hendrik/Dokumente/Davinci/FaceEncodings/")

# convert the image to grayscale
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# create a face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# detect faces in the image
faces = face_cascade.detectMultiScale(gray, 1.1, 3)

# iterate over the detected faces
for (x, y, w, h) in faces:
# get the region of interest (ROI) for the face
    roi_gray = gray[y:y+h, x:x+w]
    
# use the face recognizer to predict the label of the face
    label, confidence = face_recognizer.predict(roi_gray)
    
# if the confidence is below a threshold, consider the prediction as "unknown"
    if confidence < 50:
        label = "Unknown"
    
    # draw a rectangle around the face and label it with the predicted label
    cv2.rectangle(src, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(src, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# display the output image
cv2.imshow('output', src)
cv2.waitKey(0)
cv2.destroyAllWindows()