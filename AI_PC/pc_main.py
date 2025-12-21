## CLIENT ##

import socket
from _thread import *
import os
import time
import cv2
import pyautogui
from PIL import Image
def read_memo(file_path):
    try:
        with open(file_path, "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print("메모 파일이 존재하지 않습니다.")
    return contents

# os.system("cd C:/yolov5/runs/detect")
# os.system("del /F /Q *.*")
HOST = '10.46.68.150' ## server에 출력되는 ip를 입력해주세요 ##
PORT = 9999
waiting_time = 10

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
def display_webcam():
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Create a window named 'Webcam Feed'
    cv2.namedWindow('Webcam Feed', cv2.WINDOW_NORMAL)  # WINDOW_NORMAL 속성으로 창 크기 조정 가능하도록 설정
    cv2.setWindowProperty('Webcam Feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # 최대화된 창으로 변경

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab a frame from the webcam.")
            break

        # Display the frame in the window named 'Webcam Feed'
        cv2.imshow('Webcam Feed', frame)
        # Exit the loop when the 'q' key is pressed
        screenshot = pyautogui.screenshot()
        screenshot.save('save.jpg')
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        pyautogui.click()
        pyautogui.typewrite('q')
    cap.release()
    cv2.destroyAllWindows()

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        data=data.decode()
        print("recive : ", data)
        if data=="run":
            display_webcam()
            os.system("python C:\yolov5\detect.py --weight \"C:/yolov5/runs/train/exp2/weights/best.pt\" --source \"C:/codepair/save.jpg\" --save-txt --save-conf --save-crop")
            memo=read_memo("C:/yolov5/runs/detect/exp/labels/save.txt")
            sp_values=memo.split()
            class_num=int(sp_values[0])
            conf=float(sp_values[-1])
            print(class_num,conf)
            if conf>0.5:
                class_num=str(class_num)
                client_socket.send(class_num.encode())

start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

while True:
    message = input()
    if message == 'quit':
        close_data = message
        break

    client_socket.send(message.encode())

client_socket.close()
