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
camera.resolution = [640,480]
raw=PiRGBArray(camera)
# camera.framerate = 5
camera.awb_mode = 'auto'
sleep(1)
avg=None
write=False
change=False
# cascade=cv2.CascadeClassifier("/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml")
no=0
for frame in camera.capture_continuous(raw,format="bgr",use_video_port=False):
	# camera.capture(raw,format="rgb")
	# raw.truncate(0)
	dst=cv2.cvtColor(frame.array, cv2.COLOR_RGB2GRAY)
	dst = cv2.GaussianBlur(dst, (21, 21), 4)
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
	cv2.accumulateWeighted(dst, avg, 0.4)
	frameDelta = cv2.absdiff(dst, cv2.convertScaleAbs(avg))
	thresh = cv2.threshold(frameDelta, 32, 255,cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	now = datetime.datetime.now()
	for c in cnts:
		if cv2.contourArea(c) < 160:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		print "[DEBG] X: %s\tY: %s\tW: %s\tH:%s"%(x,y,w,h)
		cv2.rectangle(frame.array, (x, y), (x + w, y + h), (0, 255, 0), 2)
		change=True
	if change:
		no+=1
		change=False
	if no>5:
		write=True
		no=0
	if write:
		print "[DEBG] I: %s"%(now.strftime("%Y-%m-%d %H:%M:%S"))
		cv2.putText(frame.array, now.strftime("%Y-%m-%d %H:%M:%S"), (5, frame.array.shape[0] - 5), cv2.FONT_HERSHEY_SIMPLEX,0.55, (0, 0, 255), 1)
		cv2.imwrite("%s.jpg"%(now.strftime("%Y%m%d %H%M%S")),frame.array)
		write=False
	raw.truncate(0)
	sleep(1)
camera.close