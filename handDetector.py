import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

cap = cv2.VideoCapture(0)
wCam,hCam = 640, 480
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw = False)
    if len(lmList) != 0:
        length = math.hypot(x2 - x1,y2 - y1)

        vol = np.interp(length,[50,300],[mivVol,maxVol])
        volBar = np.interp(length,[50,300],[400,150])
        volPer = np.interp(length,[50,300],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)
        if length < 50 :
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
