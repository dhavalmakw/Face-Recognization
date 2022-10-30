
#import libraries
import face_recognition
import cv2
import numpy as np
import os
from datetime import date
import sys

#open webcam
video_capture = cv2.VideoCapture(0)

#take immage from folder to identify which face is on webcam now.
image = face_recognition.load_image_file("dhaval.png")
dv_face_enconding = face_recognition.face_encodings(image)[0]

mother_image = face_recognition.load_image_file("mother.jpeg")
mother_face_enconding = face_recognition.face_encodings(mother_image)[0]

father_image = face_recognition.load_image_file("father.png")
father_face_enconding = face_recognition.face_encodings(father_image)[0]

known_face_encodings = [
    dv_face_enconding,
    mother_face_enconding,
    father_face_enconding,
]

#give name of that faces
known_face_names = [
    "dhaval",
    "mother",
    "father"
]
#declared some list, string, integer value for code purpose
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
flage = 0
list_line = []
new_face = -1
old_face = -1

#till user does not provide keyboard inturrupt
while True:
    #convert webcam face into frames given size.
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        #convert this frame in to RGB color frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # If no face in webcam then 
        if face_encodings == []:
            flage=1
        face_names = []

        #main for loop recognize the face 
        for face_encoding in face_encodings:
            #compaire webcam face and stored face
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"            
            #give a perticular index to collecting face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                #If face is covered second time then..
                name = known_face_names[best_match_index]
                new_face = best_match_index 

                if old_face != new_face or flage == 1 :
                    #open status file to store data
                    t1 = open("temp.txt","w")
                    f1 = open("status.txt","r")
                    s = ""
                    temp = 0
                    for word in f1:
                        number = word.split(" ")
                        temp = int(number[-1])
                        if word[0:6] == name:#compaire file data with webcam faces
                            print("Door is opened")
                            if word[7:15] == "went out":
                                s = word[0:6] + " entered in house "+str(temp)#change stauts of person
                                t1.write(s+"\n")#update status in file
                            else:
                                temp += 1
                                s = word[0:6] + " went out " + str(temp)#change stauts of person
                                t1.write(s+"\n")#update status in file
                                if temp > 5:#for question number 4.
                                    print("Stay at home in this pandemic situation and stay safe.")
                                    sys.exit()
                        else:
                            t1.write(word)
                    f1.close()
                    t1.close()
                    
                    #for upadating data in file we use temp file. Because directl can't update file stored data.
                    t2 = open("temp.txt","r")
                    f2 = open("status.txt","w")
                    print("Person Name |"+" Went out of the house")
                    for line in t2:
                        number = line.split(" ")
                        f2.write(line)
                        #for printing person name and how many times he/she went out of the house.
                        print(number[0]+"      | "+number[-1])
                    flage = 0
            
            #If person is not fount
            else:
                print("You are not authorise to enter in house.")
                countinue
        
            face_names.append(name)
        old_face = new_face#update face index 

    #Draw a box on face detect with webcam    
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)

    #To terminate.
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

#close all windows.
video_capture.release()
cv2.destroyAllWindows()