#encoding:utf8
##
 #  @filename   :   main.cpp
 #  @brief	  :   2.7inch e-paper display demo
 #  @author	 :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare	 August 16 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##
import sys
import os
import signal
reload(sys)
sys.setdefaultencoding('utf8')

import epd2in7
import Image
import ImageFont
import ImageDraw
import datetime
import time
import RPi.GPIO as GPIO
from api import api

class display(api):
	epd = epd2in7.EPD()
	epd.init()
	WIDTH=epd2in7.EPD_WIDTH#176
	HEIGHT=epd2in7.EPD_HEIGHT#264
	warning=False
	message=False
	stop=False
	threads=[]
	times=0

	def newImage(self):
		self.image = Image.new('1', (self.WIDTH, self.HEIGHT), 255)
		self.draw = ImageDraw.Draw(self.image)
	def main(self):
		self.newImage()
		self.imgRender()
		self.messageRender()
		self.warningRender()
		self.show(self.image)
	def warningRender(self):
		if self.warning and self.info:
			pass
	def messageRender(self):
		if self.message and self.info:
			fontB=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/Dengb.ttf', 24)
			self.draw.rectangle(( 0, 0, self.WIDTH, 100), fill = 0)
			self.draw.text((0,28),self.info,font=fontB,fill=255)
	def show(self,image):
		self.epd.display_frame(self.epd.get_frame_buffer(self.image),True)
		return True
	def menuRender(self,draw,menu1= u"刷新",menu2=u"上页",menu3=u"下页",menu4=u"关机"):
		fontM=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/simfang.ttf', 17)
		self.draw.rectangle(( 0, self.HEIGHT-18, 41, self.HEIGHT), fill = 0)
		self.draw.rectangle((44, self.HEIGHT-18, 86, self.HEIGHT), fill = 0)
		self.draw.rectangle((89, self.HEIGHT-18, 131, self.HEIGHT), fill = 0)
		self.draw.rectangle((134, self.HEIGHT-18, 176, self.HEIGHT), fill = 0)
		self.draw.text((4, self.HEIGHT-18), menu1, font = fontM, fill = 255)
		self.draw.text((48, self.HEIGHT-18), menu2, font = fontM, fill = 255)
		self.draw.text((93, self.HEIGHT-18), menu3, font = fontM, fill = 255)
		self.draw.text((138, self.HEIGHT-18), menu4, font = fontM, fill = 255)
	def datetimeRender(self,draw):
		now = datetime.datetime.now()
		fontB = ImageFont.truetype('/root/ePaper/pixelmix.ttf', 56)
		self.draw.text((0, 0), now.strftime("%H:%M"), font = fontB, fill = 0)
		fontM= ImageFont.truetype('/root/ePaper/pixelmix.ttf',20)
		self.draw.rectangle((0, 60, 176, 80), fill = 0)
		self.draw.text((1, 60), now.strftime(u"%y-%m-%d"), font = fontM, fill = 255)		
	def contentRender(self,draw):
		self.weatherRender()
	def imgRender(self):
		self.datetimeRender(self.draw)
		self.contentRender(self.draw)
		self.menuRender(self.draw)
	def tRun(self,thread):
		pass
	def tStop(self,id):
		pass
	def error(self):
		pass
	def quit(self):
		self.message=True
		self.info=u"已退出"
		self.main()
		print "Quit"
	def shutdown(self,confirm=False):
		if confirm:
			self.message=True
			self.info=u"已退出"
			self.main()
			os.system("halt")
		else:
			self.main(True,u"confirm")
	def weatherRender(self):
		if self.times > 10 or self.times==0:
			self.weather=self.weatherHandler()
			self.times = 0
		fontxB=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/Dengb.ttf', 36)
		fontB=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/Dengb.ttf', 26)
		fontM=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/Dengb.ttf', 22)
		fontS=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyh.ttc', 12)
		fontxS=ImageFont.truetype('/root/ePaper/pixelmix.ttf', 8)
		fontSb=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 14)
		self.draw.text((0,84),self.weather["temp"],font=fontSb,fill=0)
		self.draw.text((80,84),self.weather["weather"],font=fontxB,fill=0)
		self.draw.text((0,100),self.weather["wind"],font=fontS,fill=0)
		self.draw.rectangle((60,87,82,99),outline=0,fill=255)
		self.draw.text((61,85),self.weather["aqi"],font=fontS,fill=0)
		self.draw.text((58,110),self.weather["time"],font=fontxS,fill=0)
		y=120
		x=1
		for detail in self.weather["detail"]:
			self.draw.text((x,y),detail["stime"],font=fontxS,fill=0)
			self.draw.text((x,y+4),detail["temp"],font=fontS,fill=0)
			self.draw.text((x+26,y+4),detail["weather"],font=fontS,fill=0)
			x+=58
		y+=24
		for future in self.weather["future"]:
			self.draw.text((0,y),future["temp"],font=fontSb,fill=0)
			self.draw.text((58,y),future["week"],font=fontS,fill=0)
			self.draw.text((82,y+4),self.weather["weather"],font=fontB,fill=0)
			y+=15
			self.draw.text((0,y),future["wind"],font=fontS,fill=0)
			self.draw.text((58,y),future["sunrise"],font=fontxS,fill=0)
			self.draw.text((58,y+8),future["sunset"],font=fontxS,fill=0)
			y+=15
		self.times +=1
class buttom(display):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(5,GPIO.IN)
	GPIO.setup(6,GPIO.IN)
	GPIO.setup(13,GPIO.IN)
	GPIO.setup(19,GPIO.IN)
	confirm=0
	def buttomHandler(self):
		pass
	def confirmHamdler(self):
		pass

d=display()
def signalHandle(signal, frame):
	d.quit()
	sys.exit(0)
signal.signal(signal.SIGINT, signalHandle)
if __name__ == '__main__':
	while True:
		d.main()
		time.sleep(45)
		# break

