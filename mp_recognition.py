import face_recognition
import cv2
from multiprocessing import Process, Manager, cpu_count, set_start_method
import time
import numpy
import threading
import platform
import sys
import math

from os import listdir
from os.path import isfile, join

# This is a little bit complicated (but fast) example of running face recognition on live video from your webcam.
# This example is using multiprocess.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

def admin_cfg(num=0):
    """ 
    Explanation: 
        This function reads and updates the "admin-status" value in the "admin.cfg" file.
        The "admin-status" value determines whether the program is in admin mode or not.
    
    Parameters:
        num (int): The value to set the "admin-status" to. Default is 0.
    
    Returns:
        None 
    """
    lines = []

    file = Global.path.replace('FaceEncodings/', '') + 'admin.cfg'
    with open(file, 'r') as f:
        lines = f.readlines()

    for i, listitem in enumerate(lines):
        if "admin-status" in listitem:
            lines[i] = "admin-status = %d\n" % num

    with open(file, 'w') as f:
        f.writelines(lines)


def debug(code=0):
    """ 
    Explanation: 
        This function prints a debug message with the given code.
    
    Parameters:
        code (int): The code to include in the debug message. Default is 0.
    
    Returns:
        None 
    """
    print("DEBUG "+str(code))

def is_looking_at_camera(frame):
    """ 
    Explanation: 
        This function checks if a person in the given frame is looking at the camera.
        It returns True if the person is looking at the camera, and False otherwise.
    
    Parameters:
        frame (numpy array): A frame from a video stream containing a face.
    
    Returns:
        bool: True if the person is looking at the camera, False otherwise. 
    """

    # Convert the frame to RGB
    rgb_frame_1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Use the face_recognition library to detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame_1)

    # If there are no faces in the frame, return False
    if len(face_locations) == 0:
        return False

    # Loop through the faces in the frame
    for face_location in face_locations:
        # Get the coordinates of the face
        top, right, bottom, left = face_location

        # Extract the face from the frame
        face_image = rgb_frame_1[top:bottom, left:right]

        # Use the face_recognition library to detect the facial landmarks
        landmarks = face_recognition.face_landmarks(face_image)

        # Check if the person is looking at the camera by checking the position of the pupils
        if 'left_eye' in landmarks and 'right_eye' in landmarks:
            left_pupil = landmarks['left_eye'][0]
            right_pupil = landmarks['right_eye'][3]
            if left_pupil[1] < left_pupil[0] and right_pupil[1] < right_pupil[0]:
                # The person is looking at the camera
                return True

    # If we reach this point, the person is not looking at the camera
    print("TEST546")
    return False
    

def get_encodings(path="", known_face_encodings=[], known_face_names=[]):

    """ 
    Explanation: 
        This function reads all the images in the given path, extracts their face encodings and names,
        and stores them in the given lists.
    
    Parameters:
        path (str): The path to the directory containing the images.
        known_face_encodings (list): A list to store the face encodings in.
        known_face_names (list): A list to store the names in.
    
    Returns:
        tuple: A tuple containing the updated lists of face encodings and names. 
    """

    
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
        known_face_encodings.append(str(listitem.replace('.jpg','_encoding').replace(' ','_')))
        known_face_names.append(str(listitem.replace('.jpg','')))

    print("TestTestTest***********************")
    print(known_face_encodings)
    print(known_face_names)
    print("TestTestTest**********************")

    return known_face_encodings, known_face_names


def get_face_distance_and_angle(ref_frame, reference_face_encoding):
    """
    Explanation: Calculate the distance and angle of a face relative to the camera.
    
    Parameters:
        frame (numpy array): The frame in which to detect the face.
        reference_face_encoding (numpy array): The face encoding of the reference image.
    
    Returns:
        tuple: A tuple containing the distance and angle of the face relative to the camera.
    """
    # Initialize the object tracker
    tracker = cv2.TrackerMedianFlow_create()
    
    # Set up the bounding box of the face in the first frame
    face_locations = face_recognition.face_locations(ref_frame)
    face_encodings = face_recognition.face_encodings(ref_frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        if face_recognition.compare_faces([reference_face_encoding], face_encoding)[0]:
            bbox = (left, top, right-left, bottom-top)
            tracker.init(ref_frame, bbox)
            break
    
    # Calculate the center of the frame
    frame_center_x = ref_frame.shape[1] // 2
    frame_center_y = ref_frame.shape[0] // 2
    
    # Update the object tracker and extract the position of the face
    success, bbox = tracker.update(ref_frame)
    (x, y, w, h) = [int(i) for i in bbox]
    center_x = x + w // 2
    center_y = y + h // 2
    
    # Calculate the distance and angle of the face relative to the center of the frame
    distance = math.sqrt((center_x - frame_center_x)**2 + (center_y - frame_center_y)**2)
    angle = math.atan2(center_y - frame_center_y, center_x - frame_center_x)
    
    # Return the distance and angle of the face
    return distance, angle

# Get next worker's id
def next_id(current_id, worker_num):
    """ 
    Explanation: 
        This function gets the next available worker id.
    
    Parameters:
        None
    
    Returns:
        int: The next available worker id.
    """

    if current_id == worker_num:
        return 1
    else:
        return current_id + 1


# Get previous worker's id
def prev_id(current_id, worker_num):
    """ 
    Explanation: 
        This function gets the previous available worker id.
    
    Parameters:
        None
    
    Returns:
        int: The previous available worker id.
    """
    if current_id == 1:
        return worker_num
    else:
        return current_id - 1


# A subprocess use to capture frames.
def capture(read_frame_list, Global, worker_num):

    """ 
    Explanation: 
        This function captures a frame from the video stream and returns it.
    
    Parameters:
        video_capture (cv2.VideoCapture): The video stream to read a frame from.
    
    Returns:
        numpy array: The captured frame. 
    """

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(Global.device)
    # video_capture.set(3, 640)  # Width of the frames in the video stream.
    # video_capture.set(4, 480)  # Height of the frames in the video stream.
    # video_capture.set(5, 30) # Frame rate.
    print("Width: %d, Height: %d, FPS: %d" % (video_capture.get(3), video_capture.get(4), video_capture.get(5)))

    while not Global.is_exit:
        # If it's time to read a frame
        if Global.buff_num != next_id(Global.read_num, worker_num):
            # Grab a single frame of video
            ret, frame = video_capture.read()
            read_frame_list[Global.buff_num] = frame
            Global.buff_num = next_id(Global.buff_num, worker_num)
        else:
            time.sleep(0.01)

    # Release webcam
    video_capture.release()


# Many subprocess use to process frames.
def process(worker_id, read_frame_list, write_frame_list, Global, worker_num):

    """ 
    Explanation: 
        This function processes a frame from the video stream.
        It detects any known faces and displays their names on the frame.
    
    Parameters:
        frame (numpy array): A frame from the video stream.
        known_face_encodings (list): A list of known face encodings.
        known_face_names (list): A list of known names.
    
    Returns:
        numpy array: The processed frame with names of known faces displayed on it. 
    """
    
    known_face_encodings = Global.known_face_encodings
    known_face_names = Global.known_face_names

    while not Global.is_exit:

        # Wait to read
        while Global.read_num != worker_id or Global.read_num != prev_id(Global.buff_num, worker_num):
            # If the user has requested to end the app, then stop waiting for webcam frames
            if Global.is_exit:
                break

            time.sleep(0.01)

        # Delay to make the video look smoother
        time.sleep(Global.frame_delay)

        # Read a single frame from frame list
        frame_process = read_frame_list[worker_id]

        # Expect next worker to read frame
        Global.read_num = next_id(Global.read_num, worker_num)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = cv2.cvtColor(frame_process, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the frame of video, cost most time
        if Global.use_cascade == 0:
            face_locations = face_recognition.face_locations(rgb_frame)
        else:
            face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            face_locations = face_detector.detectMultiScale(rgb_frame, scaleFactor=1.1, minNeighbors=2)        
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        i=0
        for (top, right, bottom, left), face_encodings in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encodings)

            name = "Unknown"

            # If a match was found in Global.known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                #print("known_face_names[index]: " + str(first_match_index))

            if "Hendrik Siemens" in name:
                admin_cfg(1)
                name="Admin"
            else:
                admin_cfg(0)

            # Draw a box around the face
            set_boxes(frame_process, top, right, bottom, left, name)
            i+=1

        # Wait to write
        while Global.write_num != worker_id:
            time.sleep(0.01)

        # Send frame to global
        write_frame_list[worker_id] = frame_process

        # Expect next worker to write frame
        Global.write_num = next_id(Global.write_num, worker_num)

def set_boxes(frame_process, top, right, bottom, left, name):
    cv2.rectangle(frame_process, (left, top), (right, bottom), (0, 215, 255), 2)

    cv2.rectangle(frame_process, (left, bottom - 35), (right, bottom), (0, 215, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame_process, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    

def set_frame_delay(Global, fps):

    """ 
    Explanation: 
        This function sets the frame delay based on the given frame rate.
    
    Parameters:
        fps (int): The frame rate.
    
    Returns:
        None 
    """

    if fps < 6:
        Global.frame_delay = (1 / fps) * 0.75
    elif fps < 20:
        Global.frame_delay = (1 / fps) * 0.5
    elif fps < 30:
        Global.frame_delay = (1 / fps) * 0.25
    elif fps < 60:
        Global.frame_delay = (1 / fps) * 0.1
    else:
        Global.frame_delay = 0

def setGlobals():

    """ 
    Explanation: 
        This function sets the global variables.
    
    Parameters:
        None
    
    Returns:
        None 
    """

    Global = Manager().Namespace()
    Global.device = 0
    Global.buff_num = 1
    Global.read_num = 1
    Global.write_num = 1
    Global.frame_delay = 0
    Global.is_exit = False
    Global.use_cascade = 0
    read_frame_list = Manager().dict()
    write_frame_list = Manager().dict()
    #Global.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    Global.path ="/home/hendrik/Dokumente/Davinci/FaceEncodings/"
    files = [f for f in listdir(Global.path) if isfile(join(Global.path, f))]

    Global.known_face_encodings=[]
    Global.known_face_names=[]
    
    for name in files:
        tmp1 = face_recognition.load_image_file(Global.path+name)
        tmp2 = face_recognition.face_encodings(tmp1)[0]

        Global.known_face_encodings += [tmp2]
        Global.known_face_names += [str(name.replace('.jpg',''))]
    return Global,read_frame_list,write_frame_list

if __name__ == '__main__':

    """ 
    Explanation: 
        This is the entry point of the program.
        It runs the main program.
    
    Parameters:
        None
    
    Returns:
        None 
    """

    # Fix Bug on MacOS
    if platform.system() == 'Darwin':
        set_start_method('forkserver')

    # Global variables
    Global, read_frame_list, write_frame_list = setGlobals()

    # Number of workers (subprocess use to process frames)
    if cpu_count() > 2:
        worker_num = cpu_count() - 1  # 1 for capturing frames
    else:
        worker_num = 2

    # Subprocess list
    p = []

    # Create a thread to capture frames (if uses subprocess, it will crash on Mac)
    p.append(threading.Thread(target=capture, args=(read_frame_list, Global, worker_num,)))
    p[0].start()

   

    # Create workers
    for worker_id in range(1, worker_num + 1):
        p.append(Process(target=process, args=(worker_id, read_frame_list, write_frame_list, Global, worker_num,)))
        p[worker_id].start()

    # Start to show video
    last_num = 1
    fps_list = []
    tmp_time = time.time()
    while not Global.is_exit:
        while Global.write_num != last_num:
            last_num = int(Global.write_num)

            # Calculate fps
            delay = time.time() - tmp_time
            tmp_time = time.time()
            fps_list.append(delay)
            if len(fps_list) > 5 * worker_num:
                fps_list.pop(0)
            fps = len(fps_list) / numpy.sum(fps_list)
            #print("fps: %.2f" % fps)

            # Calculate frame delay, in order to make the video look smoother.
            # When fps is higher, should use a smaller ratio, or fps will be limited in a lower value.
            # Larger ratio can make the video look smoother, but fps will hard to become higher.
            # Smaller ratio can make fps higher, but the video looks not too smoother.
            # The ratios below are tested many times.
            set_frame_delay(Global, fps)

            #  Display the resulting image 
            cv2.imshow('Video', write_frame_list[prev_id(Global.write_num, worker_num)])

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Global.is_exit = True
            break

        time.sleep(0.01)

    # Quit
    cv2.destroyAllWindows()