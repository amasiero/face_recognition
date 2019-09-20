import face_recognition
import cv2
import numpy as np
import os
import socket
import time
import json

path = "static/known_people"

known_face_encodings = []
known_face_names = []

for file in os.listdir(path):
    face = face_recognition.load_image_file(path + "/" + file)
    face_encoding = face_recognition.face_encodings(face)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(file.split('.')[0])

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", 44444))

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    names = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            names.append(name)

    message = {'founds' : names}
    json_message = json.dumps(message)
    server.sendto(bytes(json_message, 'UTF-8'), ('<broadcast>', 37020))
    time.sleep(1)

        #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    #cv2.imshow("Video", frame)

    #if cv2.waitKey(1) & 0xFF == ord("q"):
    #    break

video_capture.release()
cv2.destroyAllWindows()
