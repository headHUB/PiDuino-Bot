# display the raspicam uv4l video stream, and do some facial recognition
#
# run this with:
# tryout_command_gui.py locally
# arduino_command_center3.py on the pi
# and connect_serial3.ino an the arduino
# watch the stream in your brwoser at 'http://192.168.0.105:8080/stream/video.mjpeg'
# thread idee van http://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt

import time
import cv2
import urllib 
import socket
import numpy as np
import sys
import threading


# utp setup
TCP_IP = '192.168.0.105'
TCP_PORT = 5006
BUFFER_SIZE = 1024


distance = ''
looptime = time.time()
lasttime = time.time()
i = np.zeros((240,320,3), dtype=np.uint8)
gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = ()




def videothread(stream, bytes, run_event):
    global distance
    global i
    cv2.namedWindow('PiDuino video stream', cv2.WINDOW_NORMAL)
    while run_event.is_set():
        try:
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                font = cv2.FONT_HERSHEY_SIMPLEX

                for (x, y, w, h) in faces:
                    cv2.rectangle(i, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(i,str(distance),(0,25), font, 1, (0,0,255), 2, cv2.CV_AA)
                # i2 = cv2.resize(i, (0,0), fx=2.0, fy=2.0)
                cv2.imshow('PiDuino video stream',i)
                # cv2.waitKey(0)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stream.close()
                    # exit(0)
                    break
        except KeyboardInterrupt:
            print "video thread received keyboard interrupt, stopping..."
            stream.close()
            exit(0)
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


def feedbackthread(s, run_event):
    global distance
    global looptime
    global lasttime
    while run_event.is_set():
        try:
            looptime = time.time()
            if looptime - lasttime > 0.5:
                lasttime = time.time()
                distance = s.recv(BUFFER_SIZE)[-5:-2]
                if distance == '':
                    distance = '0'
                if not distance[0] in '123456789':
                    distance = distance[-2:]
                # print distance
            else:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print "feedback thread received keyboard interrupt, stopping..."
            exit(0)


def facedetectthread(run_event):
    global i
    global faces
    frontFaceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    sideFaceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalcatface_extended.xml')
    pixelDistanceSquared = 400
    time.sleep(5)
    while run_event.is_set():
        try:
            gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            faces = frontFaceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            #  some tryout stuff to see if i could improve face detection by
            # using multiple detectors. currently still too buggy.

            # frontFaces = frontFaceCascade.detectMultiScale(
            #     gray,
            #     scaleFactor=1.1,
            #     minNeighbors=5,
            #     minSize=(30, 30),
            #     flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            # )
            # sideFaces = sideFaceCascade.detectMultiScale(
            #     gray,
            #     scaleFactor=1.1,
            #     minNeighbors=5,
            #     minSize=(30, 30),
            #     flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            # )

            # if len(sideFaces) == 0 and len(frontFaces) == 0:
            #     print "no faces found bruv"
            #     faces = ()
            # elif len(frontFaces) == 0:
            #     print "no fronts bruv"
            #     faces = sideFaces
            #     print faces
            # elif len(sideFaces) == 0:
            #     print "no sides bruv"
            #     faces = sideFaces
            #     print faces
            # else:
            #     print "averaging face"
            #     faces = ()
            #     for front in frontFaces:
            #         (x1, y1, w1, h1) = front
            #         for side in sideFaces:
            #             (x2, y2, w2, h2) = side
            #             if np.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)) < pixelDistanceSquared:
            #                 x = (x1 + x2)/2
            #                 y = (y1 + y2)/2
            #                 w = (w1 + w2)/2
            #                 h = (h1 + h2)/2
            #                 faces += ((x, y, w, h),)
            #                 print faces
            #             else:
            #                 faces += (side,)
                            # faces += 
            print("Found {0} faces!".format(len(faces)))
            time.sleep(0.3)
        except KeyboardInterrupt:
            print "feedback thread received keyboard interrupt, stopping..."
            # s.close()
            exit(0)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise







if __name__ == '__main__':
    run_event = threading.Event()
    run_event.set()

    streamurl = 'http://' + TCP_IP + ':8080/stream/video.mjpeg'
    stream = urllib.urlopen(streamurl)
    bytes=''

    t1 = threading.Thread(target = videothread, args=(stream, bytes, run_event))
    t1.start()
    print "video thread started"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    t2 = threading.Thread(target = feedbackthread, args=(s,run_event))
    t2.start()
    print "feedback thread started"

    t3 = threading.Thread(target = facedetectthread, args=(run_event,))
    t3.start()
    print "face detection thread started"

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        print "attempting to close threads."
        run_event.clear()
        t1.join()
        t2.join()
        t3.join()
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        stream.close()
        time.sleep(0.1) # wait a little for threads to finish
        print "threads successfully closed"




