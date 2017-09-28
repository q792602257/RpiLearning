from picamera import PiCamera
from picamera.array import PiRGBArray
import datetime
import io
from time import sleep
import numpy

camera = PiCamera()
camera.shutter_speed = 6000000
camera.iso = 800
camera.resolution = [1600,1200]
camera.awb_mode = 'auto'
camera.framerate = 5
sleep(1)
camera.start_recording("1.mp4",format='h264', quality=20)
camera.wait_recording(15)
camera.stop_recording()
camera.capture("/root/1.jpg")
# raw=PiRGBArray(camera)
# camera.capture(raw,format="rgb")
# print raw.array()