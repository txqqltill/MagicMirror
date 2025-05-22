from MMM_Face_Recognition_SMAI_Common import (
    load_known_faces,
    get_video,
    get_face_data,
    recognize_faces,
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

    face_id = names[0] if names else "Guest"
    faces.append(face_id)
    if len(faces) > 4:
        faces.pop(0)
    if all(f == faces[0] for f in faces):
        switch = True
    else:
        switch = False

    sleep(0.5)

    sample_txt = "/home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/sample.txt"
    with open(sample_txt) as f:
        current_user = f.readline().strip('\n')
    print(f"Person Logged in: {current_user}")

    if switch:
        with open(sample_txt, "w") as f:
            f.write(face_id)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()