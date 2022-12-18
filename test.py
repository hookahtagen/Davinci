import face_recognition

from os import listdir
from os.path import isfile, join

known_face_encodings = []
known_face_names = []

def get_encodings(path=""):

    #Get all Pictures under the given path
    #Store them in a list with file-endings
    files = [f for f in listdir(path) if isfile(join(path, f))]
    
    for name in files:
        path2 = path + name

        tmp1 = face_recognition.load_image_file(path2)
        tmp2 = face_recognition.face_encodings(tmp1)[0]

        locals()[name.replace('.jpg','_image')] = tmp1
        locals()[name.replace('.jpg','_encoding')] = tmp2
    
    for listitem in files:
        known_face_encodings.append(listitem.replace('.jpg','_encoding'))
        known_face_names.append(listitem.replace('.jpg',''))
    
    

get_encodings("C:/Users/Hendrik/Documents/OpenAI/Davinci/FaceEncodings/")