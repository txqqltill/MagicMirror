import face_recognition
import cv2
from numpy import ascontiguousarray
import os
from time import sleep
from colorama import Fore

# Path to known faces and fallback name
__KNOWN_FACES_PATH = "/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public"
__DEFAULT_NAME = "User"

# Load and encode all known face images from disk
def load_known_faces():
    known_face_encodings = []
    known_face_names = []

    print("🔍 Loading known face images...")
    for file in os.listdir(__KNOWN_FACES_PATH):
        if file.endswith("-id.jpg"):
            name = file.replace('-', ' ').split(' ')[0]
            image_path = os.path.join(__KNOWN_FACES_PATH, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) == 1:
                known_face_encodings.append(encodings[0])
                known_face_names.append(name)
                print(f"✓ Loaded face for: {name}")
            else:
                print(Fore.YELLOW + f"⚠ Skipping {file} - No or multiple faces detected.")
    
    return known_face_encodings, known_face_names

# Open the webcam safely
def get_video():
    video_capture = cv2.VideoCapture(0)
    while not video_capture.isOpened():
        print(Fore.RED + "❌ Could not access the camera. Is it plugged in?")
        sleep(0.5)
    return video_capture

# Resize and convert the image to RGB and return encodings and face locations
def get_face_data(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = ascontiguousarray(small_frame[:, :, ::-1])
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    return face_encodings, face_locations

# Match a face encoding to known people
def recognize_faces(face_encodings, known_encodings, known_names):
    names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = __DEFAULT_NAME
        if True in matches:
            index = matches.index(True)
            name = known_names[index]
        names.append(name)
    return names

def log_person(current_user):
    print(f"Person Logged in: {current_user}")