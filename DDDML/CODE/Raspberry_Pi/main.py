import datetime
import cv2
from sqllite import insert_timestamp
from timestamp import Time
from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=24
GPIO.setup(buzzer,GPIO.OUT)
faceCascade = cv2.CascadeClassifier('/home/raspberry/Desktop/test/haarcascade_frontalface_alt.xml')
eyeCascade = cv2.CascadeClassifier('/home/raspberry/Desktop/test/haarcascade_eye_tree_eyeglasses.xml')
count=0


def update_clock(system_t):
    os = datetime.datetime.now()
    system_t = os.strftime("%H:%M:%S")
    # system_d = os.strftime('%A')
    return system_t

def update_day(system_d):
    day= datetime.datetime.now()
    system_d = day.strftime('%A')
    return system_d

ostime = datetime.datetime.now()

system_time=ostime.strftime('%H:%M:%S')
system_day=ostime.strftime('%A')

cap = cv2.VideoCapture(0)
while(1):

    ret, img = cap.read()
    if ret:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(frame, 1.1, 5)
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
            frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
            eyes = eyeCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(eyes)==0:
                count+=1
                if(count==3):
                    # Saved closed eye image in folder
                    cv2.imwrite('/home/raspberry/Desktop/test/testimage.jpg', img)
                    count = 0
                    print('WARNING: eyes closed')
                    a = Time( update_day(system_day), 'Driver unknown', update_clock(system_time))
                    # created database for saving timestamps
                    insert_timestamp(a)
                    cv2.putText(frame_tmp, "WARNING!!!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 0, 255), 2)
                    cv2.putText(frame_tmp, update_clock(system_time),(00,200),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                 
                    GPIO.output(buzzer, GPIO.HIGH)
                    sleep(0.1)
                    GPIO.output(buzzer,GPIO.LOW)
                    sleep(0.1)
            else:
                count = 0
                cv2.putText(frame_tmp, "ALL GOOD", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 225, 0), 2)
                cv2.putText(frame_tmp, update_clock(system_time), (00, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 225, 0), 2)

            frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)

            cv2.imshow('FACE DETECTION', frame_tmp)

        waitkey = cv2.waitKey(1)
        if waitkey == ord('q') or waitkey == ord('Q'):
            cv2.destroyAllWindows()
            break