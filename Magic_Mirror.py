#coding:utf-8
"""
Created on Fri Nov 23 16:28:48 2018

@author: Aaron
"""
import os
import sys
import time
import urllib3
import json
import base64
import numpy as np
import cv2
import urllib,urllib.request
import imp
import pygame
import random
from aip import AipSpeech

APP_ID='14590965'
API_KEY= '0HoOwa6hiW9K776yiEviMPn2'
SECRET_KEY='lCOlp135b5ccTsm3IxzMNxOG6zP1aq4Q '
client=AipSpeech(APP_ID, API_KEY, SECRET_KEY)

API_KEY_TU = 'b47d6e8f5b5c4c3ba0d1a00f3259037f'
raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY_TU

window_name='Magic Mirror'
wenhou="你好,我是魔镜"#wenhou.mp3
luyin="请说话"#luyin.mp3

imp.reload(sys)
urllib3.disable_warnings()

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
 
#===================================================================  
#语音合成播放
def TTS_PLAY(text_str):
    result= client.synthesis(text_str,'zh',1,{ 'vol': 15,'per':4,'spd':5 })

    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
    os.system('omxplayer  auido.mp3')

#===================================================================
#录音&识别
def Luyin_ASR():    
    os.system('arecord -D "plughw:1,0" -f S16_LE -d 10 -r 16000 /home/pi/Desktop/10.wav')
    #os.system('aplay /home/pi/Desktop/10.wav')

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    
    result_json = client.asr(get_file_content('10.wav'),'wav',16000,{'dev_pid':1536})
    if result_json['err_no']==3301:#speech quality error
        return " ",0,0
    else:
        result_input = result_json['result'][0].replace("，", "")
        if result_input.find("唱一首歌")==-1:
            return result_input,1,0
        else:
            return result_input,1,1
        

#=================================================================
#图灵聊天
def Tuling_result(queryStr):
    TULINURL = "%s%s" % (raw_TULINURL,urllib.request.quote(queryStr))
    req = urllib.request.Request(url=TULINURL)
    result = urllib.request.urlopen(req).read()
    hjson=json.loads(result.decode('utf-8'))
    length=len(hjson.keys())
    content=hjson['text']
    return content


#================================================================
 
#主程序开始
while True:
    #显示待机图片
    #img=cv2.imread('cover.jpg',cv2.IMREAD_COLOR)# 读入彩色图片
    img=cv2.imread('cover.png',cv2.IMREAD_COLOR)# 读入彩色图片
    cv2.imshow(window_name,img)#建立窗口显示图片

    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    faceCascade.load('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')      
    
    while True:
        #人脸检测，唤醒成功
        ret,img = cap.read()
        # img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,     
                    minSize=(30, 30)
        )

        if len(faces)!=0:
            break
        k1 = cv2.waitKey(20) & 0xff
        if k1 == 32: # press 'SPACE' to quit
            break
    
    #人脸检测，显示切换，结果显示
    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    eyeCascade.load('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
    smileCascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    smileCascade.load('/usr/local/share/OpenCV/haarcascades/haarcascade_smile.xml')
  
    N=0
    M=0
    os.system('omxplayer  wenhou.mp3')#播放问候语
        
    while True:
        ret,img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 8)
        N=N+1
        M=M+1

        for (x,y,w,h) in faces:
            N=0
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            cv2.putText(img,"Face Detected",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            
            eyes = eyeCascade.detectMultiScale(roi_gray)
            smile = smileCascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.putText(img,"Eyes Detected",(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

            for (ex,ey,ew,eh) in smile:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cv2.putText(img,"Mouth Detected",(10,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        cv2.imshow(window_name,img)
        
        if M==50:
            os.system('omxplayer  luyin.mp3')#启动录音
            chat_input,quality,music=Luyin_ASR()
            if quality==1:
                chat_output=Tuling_result(chat_input)
                TTS_PLAY(chat_output)
                if music==1:
                    index=random.randint(1,10)
                    mp3_file="/home/pi/"+str(index)+".mp3"
                    os.system('omxplayer '+mp3_file)
            M=0
             
        k2 = cv2.waitKey(20) & 0xff
        if k2 == 32: # press 'SPACE' to quit
            break
        if N==50:
            break
        
    k3 = cv2.waitKey(100) & 0xff
    if k3 == 27: # press 'ESC' to quit
        break        
  
cap.release()
cv2.destroyAllWindows()

######################################
