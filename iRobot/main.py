from face import AipFace
from put_to_server import *
import base64
import cv2
import RPi.GPIO as GPIO
import time
from Config import *
detector_path = "./data/haarcascade_frontalface_alt2.xml"
client = AipFace()
detector = cv2.CascadeClassifier(detector_path)
server = Server()
def draw_box(frame, result):
    face_num = result["result"]["face_num"]
    for i in range(face_num):
        location = result["result"]["face_list"][i]["location"]
        x, y, w, h = int(location["left"]), int(location["top"]), int(location["width"]), int(location["height"])
        try:
            if result["result"]["face_list"][i]["user_list"][0]["score"] > 60:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Accept", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 255, 0), thickness=1, lineType=2)
                set_low()
                print('识别成功')
                time.sleep(1)

            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "UnKnown", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 0, 255), thickness=1, lineType=2)
                set_high()
        except:
            pass
    cv2.imwrite('./data/1.jpg', frame)
    server.upload_img()


def detect_unknown(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, "UnKnown", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (0, 0, 255), thickness=1, lineType=2)
    #cv2.imshow('face', frame)
    set_high()
    cv2.imwrite('./data/1.jpg', frame)
    server.upload_img()
def set_low():  #开门
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IO_PORT,GPIO.OUT)
    GPIO.output(IO_PORT,GPIO.LOW)
def set_high(): #关门
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IO_PORT,GPIO.OUT)
    GPIO.cleanup()

video_capture = cv2.VideoCapture(-1)
set_high()
while True:
    set_high()
    ret, frame = video_capture.read() 
    image = cv2.imencode('.jpg', frame)[1]
    image64 = str(base64.b64encode(image), 'utf-8')
    result = client.multiSearch(image=image64, image_type='BASE64',
                                group_id_list="iRobot", options={"max_face_num": 3})
    if result["error_code"] == 222207:  # 识别出陌生人
        detect_unknown(frame)
    elif result["error_code"] == 0:
        draw_box(frame, result)
    else:
        set_high()
        #cv2.imshow('face', frame)
        #cv2.imwrite('./data/1.jpg', frame)
        #server.upload_img()
        print(result["error_msg"])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()

GPIO.cleanup()
