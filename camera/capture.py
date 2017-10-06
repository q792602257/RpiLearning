from picamera import PiCamera
from picamera.array import PiRGBArray
import datetime
import io
from time import sleep
import numpy as np
import cv2

camera = PiCamera()
# camera.shutter_speed = 1000
# camera.iso = 1600
camera.resolution = [1280,800]
raw=PiRGBArray(camera)
# camera.framerate = 5
camera.awb_mode = 'auto'
sleep(1)
avg=None
# cascade=cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml")
no=0
for frame in camera.capture_continuous(raw,format="bgr",use_video_port=False):
	# camera.capture(raw,format="rgb")
	# raw.truncate(0)
	dst=cv2.cvtColor(frame.array, cv2.COLOR_RGB2GRAY)
	dst = cv2.GaussianBlur(dst, (21, 21), 0)
	if avg is None:
		print "[INFO] starting background model..."
		avg = dst.copy().astype("float")
		raw.truncate(0)
		continue
	# faces=cascade.detectMultiScale(dst)
	# print len(faces)
	# for (x,y,w,h) in faces:
	# 	print "%s\t%s\t%s\t%s"%(x,y,w,h)
	# 	cv2.rectangle( frame.array, ( x, y ), ( x + w, y + h ), ( 0, 255, 0 ), 2 )
	cv2.accumulateWeighted(dst, avg, 0.5)
	frameDelta = cv2.absdiff(dst, cv2.convertScaleAbs(avg))
	thresh = cv2.threshold(frameDelta, 32, 255,cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	no+=1
	for c in cnts:
		if cv2.contourArea(c) < 100:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		print "%s\t%s\t%s\t%s"%(x,y,w,h)
		cv2.rectangle(frame.array, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.imwrite("%s.jpg"%no,frame.array)
	print "---------------------------------"
	raw.truncate(0)
	# sleep(1)
camera.close