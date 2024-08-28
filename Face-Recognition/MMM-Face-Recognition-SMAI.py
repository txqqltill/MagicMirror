# SMAI V1.01 - Face Recognition Module

# Modified by: Pratik & Eben
# This is a modified script from the open source face recognition repo:
#https://github.com/ageitgey/face_recognition
# Patch update to fix bugs

import requests
import face_recognition
import cv2
import numpy as np
import sys
import os
import time
from colorama import Fore, Style, init

video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()
if frame is None:
    print("Camera not able to capture any images, is the camera plugged in?")

time.sleep(0.1)

# Load a sample pictures and learn how to recognize them.
people = []
print("Loading known face image(s)")
for file in os.listdir("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public"):
    if file.endswith("-id.jpg"):
        fileName = file.replace('-', ' ').split(' ')[0]
        rec_image = face_recognition.load_image_file("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public/%s-id.jpg" % (fileName))
        
        rec_face_encodings = face_recognition.face_encodings(rec_image)
        if len(rec_face_encodings) < 1:
            print(Fore.RED + "%s was not recognized" % (fileName))
            exit()
        if len(rec_face_encodings) > 1:
            raise ValueError("more than one person recognized in the picture %s-id.jpg" % (fileName))
        rec_face_encoding = rec_face_encodings[0]
        people.append(rec_face_encoding)
        print(file.replace('-', ' ').split(' ')[0])

# Initialize some variables
face_locations = []
face_encodings = []

faces = []

while True:
    # Grab a single frame of video from the usb camera as a numpy array

    #remove buffered image so there is less delay 
    for i in range(5):
        ret, frame = video_capture.read()
    
    ret, frame = video_capture.read()
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    
    rgb_small_frame = np.ascontiguousarray(small_frame[:,:,::-1]) # <---- fixes error 

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    face_id = "Guest"
    
    # Loop over each face found in the frame to see if it's someone we know.
    
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(people, face_encoding)
        index = 0
        for file in os.listdir("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public"):
                if file.endswith("-id.jpg"):
                    if match[index]:
                        face_id = file.replace('-', ' ').split(' ')[0]
                    index = index + 1

    #dont switch user if one image was recognized wrong
    switch = True    
    faces.append(face_id)
    if len(faces) > 5:
        faces.pop(0)   
    faceS = faces[0]
    for face in faces:
        if face != faceS:
            switch = False
    time.sleep(0.5)

    
    #if another person is recognized they get directly connected, if the current user is a guest
    with open("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt") as f:
        first_line = f.readline().strip('\n')
    print("Person Logged in: {}!".format(first_line))
    if switch or first_line == "Guest":
        f = open("/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt", "w")
        f.write(face_id)
        f.close()
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()
