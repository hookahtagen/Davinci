import glob
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from os import listdir
from os.path import isfile, join
from collections import defaultdict

def train_split(x_to_train, y_to_train, test_size=0.2):
    return train_test_split(x_to_train, y_to_train, test_size=test_size)


def build_face_recognition_model():
    # Build the model
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(6, activation='sigmoid'))
    return model

def load_face_recognition_dataset():
    # List all image files in the dataset directory
    path ="/home/hendrik/Dokumente/Davinci/FaceEncodings/"
    file_list= [f for f in listdir(path) if isfile(join(path, f))]
    # Initialize the list of images and labels
    images = []
    labels = []

    # For each file in the list
    for file in file_list:
        # Read the image data
        image = cv2.imread(path+file)
        # Resize the image to a uniform size
        image = cv2.resize(image, (128, 128))
        # Extract the label from the filename
        label = file.split('.')[0]
        # Add the image and label to the lists
        images += [image]
        labels += [label]
    # Convert the lists to NumPy arrays
    X = np.array(images)
    y = np.array(labels)

    encoder = LabelEncoder()
    y = encoder.fit_transform(y)
    y = to_categorical(y)
    print('*************************************')
    print(X)
    print(y)
    print('*************************************')
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_split(X, y, test_size=0.2)
    return X_train, y_train, X_test, y_test


x_train, y_train, x_test, y_test = load_face_recognition_dataset()

# Build the model
model = build_face_recognition_model()

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model on the training data
model.fit(x_train, y_train, epochs=10, batch_size=32)

# Save the model to a file
model.save('face_recognition_model.h5')