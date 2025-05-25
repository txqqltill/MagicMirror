from MMM_Face_Recognition_SMAI_Common import (
    load_known_faces,
    get_video,
    get_face_data,
    recognize_faces,
    send_data_to_MM
)
from time import sleep
import cv2

video_capture = get_video()
known_face_encodings, known_face_names = load_known_faces()

recognized_last = None

print("🎥 Starting face recognition. Press 'q' to quit.")
faces = []

while True:
    for _ in range(5):
        ret, frame = video_capture.read()
    ret, frame = video_capture.read()

    face_encodings, face_locations = get_face_data(frame)
    names = recognize_faces(face_encodings, known_face_encodings, known_face_names)

    for (top, right, bottom, left), name in zip(face_locations, names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 4, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    send_data_to_MM(names, faces)

    cv2.imshow("Face Recognition Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()