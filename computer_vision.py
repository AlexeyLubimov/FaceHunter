import numpy as np
import face_recognition
import cv2
import os
import csv
from datetime import datetime


def huntface():
    path = '/Users/aleksejlubimov/Documents/diplom-project/KnowFaces'
    images = []
    classNames = []
    mylist = os.listdir("/Users/aleksejlubimov/Documents/diplom-project/KnowFaces")
    print(mylist)
    for cls in mylist:
        curImg = cv2.imread(f'{path}/{cls}')
        images.append(curImg)
        classNames.append(os.path.splitext(cls)[0])

    print(classNames)


    def markAttendance(name):
         # Получение текущей даты и времени
        now = datetime.now()
        date_format = now.strftime("%d-%m-%Y")
        time_format = now.strftime("%H:%M:%S")

        # Проверка наличия папки "Attendance"
        if not os.path.exists("Attendance"):
            os.makedirs("Attendance")

        # Формирование имени файла
        filename = "Attendance/Attendance.csv"

        # Удаление предыдущих записей
        if os.path.exists(filename):
            os.remove(filename)

        # Запись данных в файл CSV
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Time"])
            writer.writerow([name, time_format])


    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    encodeListKnown = findEncodings(images)
    print("Декодирование закончилось")

    cap = cv2.VideoCapture(0)


    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        

        name = 'Unknown'
        

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            match = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print(faceDis) 
            matchIndex = np.argmin(faceDis) 


            if match[matchIndex] == True:
                    name = classNames[matchIndex]
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

            else:
                name = "Unknown"
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
        

        cv2.imshow("WebCam", img)

        if cv2.waitKey(1) == 27:
             break
        
        
    cv2.destroyAllWindows()
        
          
if __name__ == "__main__":
    huntface()