import face_recognition as fr
import numpy as np
import cv2

# Load a sample picture and learn how to recognize it.
obama_image = fr.load_image_file("C:/Users/Hendrik/Documents/OpenAI\Davinci/obama.jpg")
obama_encoding = fr.face_encodings(obama_image)[0]

michelle_obama_image = fr.load_image_file("C:/Users/Hendrik/Documents/OpenAI\Davinci/michelle obama.jpg")
michelle_obama_encoding = fr.face_encodings(michelle_obama_image)[0]

known_face_encodings = [
    obama_encoding,
    michelle_obama_encoding
]

known_face_names = [
    "Barack Obama",
    "Michelle Obama"
]

face_locations = []
face_encodings = []
face_names = []

# Find all the faces and face encodings in the current frame
img = fr.load_image_file("C:/Users/Hendrik/Documents/OpenAI/Davinci/obama2.jpg")
face_locations = fr.face_locations(img)
face_encodings = fr.face_encodings(img)

face_names = []
for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    matches = fr.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    # # If a match was found in known_face_encodings, just use the first one.
    # if True in matches:
    #     first_match_index = matches.index(True)
    #     name = known_face_names[first_match_index]

    # Or instead, use the known face with the smallest distance to the new face
    face_distances = fr.face_distance(known_face_encodings, face_encoding)

    print(face_distances)

    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]

    face_names.append(name)

for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw a box around the face
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(img, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
cv2.imshow('image', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)
cv2.destroyAllWindows()

