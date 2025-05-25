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

faces = []

while True:
    for _ in range(5):
        ret, frame = video_capture.read()
    ret, frame = video_capture.read()

    face_encodings, _ = get_face_data(frame)
    names = recognize_faces(face_encodings, known_face_encodings, known_face_names)

    send_data_to_MM(names, faces)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()