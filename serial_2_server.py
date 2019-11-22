#! /bin/python3
import serial
import time
import requests
import json
#__anthor__=RCHes
# 打开串口
# ser = serial.Serial("/dev/ttyUSB0", 9600)

def main():
    num = 0
    recv = b'B'
    flag = 0
    ser = serial.Serial("/dev/ttyUSB0",9600)
    pydict = {"temp":"20","humi":"50","fire":"0","CO":"0"}
    while True:
# -*- coding: utf-8 -*
# -*- coding: utf-8   
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回
            recv = ser.read(count)
            ser.write(recv)
            #print(recv)
            # 解析将byte转str
            recv =recv.decode('utf-8')
            print(recv)
        #开始接收
        if recv == 'A':
            num = 1
            flag = 0
            #print('num = 1111')
        elif num == 4:
            pydict['CO'] = recv
            flag = 1
            num = 0
            print("4---")
            #print('num=1')
        elif num == 3:
            print("3---")
            pydict['fire'] = recv
            num = num +1
        elif num == 2:
            print("2----")
            pydict['temp'] = recv
            num = num +1
        elif num == 1:
            print("1----")
            pydict['humi'] = recv
            num = num +1
        if num >4:
            num = 0
            flag = 0
        if flag == 1:
            # 字典转json
            pyload = json.dumps(pydict)
            # post数据到服务器
            print('post to 111.230.59.85:10088')
            requests.post("http://111.230.59.85:10088/report_data",data=pyload)
            # print(pydict)
            #print('json为')
            #time.sleep(1)
            print(pyload)
            flag = 0
        # 清空接收e缓冲区
        ser.flushInput()
        # 必要的软件延时 与STM32适配
        time.sleep(1)
    
if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            if ser != None:
                ser.close()
