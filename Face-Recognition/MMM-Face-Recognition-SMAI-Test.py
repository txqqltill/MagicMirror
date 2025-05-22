import face_recognition
import cv2
import numpy as np
import os

# Path to known faces
KNOWN_FACES_PATH = "/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public"

# Load known face encodings
known_face_encodings = []
known_face_names = []

print("🔍 Loading known face images...")
for file in os.listdir(KNOWN_FACES_PATH):
    if file.endswith("-id.jpg"):
        name = file.replace('-', ' ').split(' ')[0]
        image_path = os.path.join(KNOWN_FACES_PATH, file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 1:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            print(f"✓ Loaded face for: {name}")
        else:
            print(f"⚠️  Skipping {file} - No or multiple faces detected.")

# Start camera
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Could not access the camera.")
    exit()

print("🎥 Starting face recognition. Press 'q' to quit.")

recognized_last = None

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to read from camera.")
        break

    # Resize and convert to RGB
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Detect faces
    rgb_small_frame = np.ascontiguousarray(small_frame[:,:,::-1])

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    names_in_frame = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]

        names_in_frame.append(name)

        # Scale coordinates back up
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 4, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Log recognized names (only if changed)
    if names_in_frame and names_in_frame != recognized_last:
        print("✅ Recognized: " + ", ".join(names_in_frame))
        recognized_last = names_in_frame

    # Show image
    cv2.imshow("Face Recognition Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
