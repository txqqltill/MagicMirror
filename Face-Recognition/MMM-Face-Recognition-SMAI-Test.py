import face_recognition
import cv2
import numpy as np
import os

# Pfad zu den bekannten Gesichtern
KNOWN_FACES_PATH = "/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/public"

# Lade bekannte Gesichter
known_face_encodings = []
known_face_names = []

print("Lade bekannte Gesichter...")
for file in os.listdir(KNOWN_FACES_PATH):
    if file.endswith("-id.jpg"):
        name = file.replace('-', ' ').split(' ')[0]
        image_path = os.path.join(KNOWN_FACES_PATH, file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 1:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            print(f"✓ {name}")
        else:
            print(f"⚠️  {file}: Kein oder mehr als ein Gesicht erkannt – übersprungen.")

# Kamera öffnen
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Kamera konnte nicht geöffnet werden.")
    exit()

print("Drücke 'q' zum Beenden.")
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Kein Bild von der Kamera erhalten.")
        break

    # Bild verkleinern und Farben umdrehen (BGR → RGB)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Gesichter erkennen
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unbekannt"

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]

        # Koordinaten zurückskalieren
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Rechteck und Name zeichnen
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 4, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Gesichtserkennung (Test)", frame)

    # Beenden mit Taste 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
