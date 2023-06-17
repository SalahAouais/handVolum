import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480

# Create an instance of the HandTrackingModule
detector = htm.HandDetector()

# Get the default audio endpoint volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol = volume.GetVolumeRange()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip coordinates
        x2, y2 = lmList[8][1], lmList[8][2]  # Index finger tip coordinates
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Midpoint between thumb and index finger

        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    
    cv2.imshow("Hand Tracking", img)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
