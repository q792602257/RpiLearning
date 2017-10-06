#encoding:utf8

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
	containerID=0
	confirm=None
	menuL=[u"刷新",u"上页",u"下页",u"关机"]
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
			self.draw.rectangle(( 0, 0, self.WIDTH, self.HEIGHT), fill = 0)
			self.draw.text((0,28),self.info,font=fontB,fill=255)
			self.message=None
			self.info=None
	def show(self,image):
		self.epd.display_frame(self.epd.get_frame_buffer(self.image),True)
		return True
	def menuRender(self,draw):
		fontM=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/simfang.ttf', 17)
		x=1
		for i in self.menuL:
			self.draw.rectangle((x, self.HEIGHT-18, x+42, self.HEIGHT), fill = 0)
			self.draw.text((x+5, self.HEIGHT-18), i, font = fontM, fill = 255)
			x+=44
	def datetimeRender(self,draw):
		now = datetime.datetime.now()
		fontB = ImageFont.truetype('/root/ePaper/pixelmix.ttf', 56)
		self.draw.text((0, 0), now.strftime("%H:%M"), font = fontB, fill = 0)
		fontM= ImageFont.truetype('/root/ePaper/pixelmix.ttf',18)
		self.draw.rectangle((0, 60, 176, 80), fill = 0)
		self.draw.text((2, 60), now.strftime(u"%y-%m-%d %a"), font = fontM, fill = 255)
	def contentRender(self,draw):
		if self.containerID==0:
			self.weatherRender()
		elif self.containerID==1:
			pass
		elif self.containerID==2:
			pass
		elif self.containerID==3:
			pass
		elif self.containerID==4:
			pass
		elif self.containerID==5:
			pass
		elif self.containerID==6:
			pass
	def imgRender(self):
		self.datetimeRender(self.draw)
		self.contentRender(self.draw)
		self.menuRender(self.draw)
	def weatherRender(self):
		self.weather=self.newWeatherHandler()
		y=82
		fontxB=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/Dengb.ttf', 40)
		fontB=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 30)
		fontM=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 22)
		fontN=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 18)
		fontS=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyh.ttc', 12)
		fontxS=ImageFont.truetype('/root/ePaper/pixelmix.ttf', 8)
		fontSb=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 20)
		fontMb=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 24)
		fontxSb=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/msyhbd.ttc', 14)
		try:
			self.draw.text((0,y),self.weather["weather"],font=fontxB,fill=0)
			self.draw.text((96,y-3),self.weather["wind"],font=fontS,fill=0)
			self.draw.rectangle((153,y,self.WIDTH-1,y+12),outline=0,fill=255)
			self.draw.text((154,y-2),"%3s"%self.weather["aqi"],font=fontS,fill=0)
			y+=13
			self.draw.text((150,y),self.weather["time"],font=fontxS,fill=0)
			self.draw.text((96,y),self.weather["pressure"],font=fontxS,fill=0)
			self.draw.text((106,y+5),u"24h温度走势",font=fontS,fill=0)
			y+=20
			self.draw.text((0,y),self.weather["temp"],font=fontSb,fill=0)
			x=104
			y+=20
			self.draw.text((106,y+20),u"24h风力走势",font=fontS,fill=0)
			for detail in self.weather["detail"]:
				if u"雨" in detail["weather"] or u"雪" in detail["weather"]:
					tmpvar1 = 0
				else:
					tmpvar1 = 255
				self.draw.rectangle((x,y,x+3,y-(detail["tempRaw"]-self.weather["tempRaw"])*1.6),outline=0,fill=tmpvar1)
				ty=y+72
				self.draw.rectangle((x,ty,x+3,ty-(detail["windRaw"])/1.2),outline=0,fill=tmpvar1)
				x+=3
			y+=10
			x=0
			for future in self.weather["future"]:
				if len(future["weather"])>3:
					tmpvar =fontxSb
				else:
					tmpvar =fontN
				self.draw.text((26,y),future["temp"],font=fontxSb,fill=0)
				self.draw.text((0,y),future["week"],font=fontS,fill=0)
				y+=15
				self.draw.text((26,y-2),future["weather"],font=tmpvar,fill=0)
				# self.draw.text((0,y),future["wind"],font=fontS,fill=0)
				self.draw.text((0,y),future["sunrise"],font=fontxS,fill=0)
				self.draw.text((0,y+8),future["sunset"],font=fontxS,fill=0)
				y+=17
		except Exception as e:
			self.error=True
			if weather["Error"]:
				self.einfo=weather["Error"]
			else:
				self.einfo=u"未知错误"
			self.error()
	def errorRender(self):
		if self.einfo and self.error:
			fontB=ImageFont.truetype('/usr/share/fonts/truetype/msfontscn/Dengb.ttf', 28)
			self.draw.rectangle(( 0, 0, self.WIDTH, self.HEIGHT), fill = 0)
			self.draw.text((0,50),self.info,font=fontB,fill=255)
			self.error=False
			self.einfo=None			
	def quit(self):
		self.message=True
		self.info=u"已退出"
		self.main()
		print "Quit"
	def shutdown(self):
		if confirm:
			self.message=True
			self.info=u"已关机"
			self.main()
			os.system("halt")
			sys.exit()
		else:
			self.main()
class buttom(display):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(5,GPIO.IN)
	GPIO.setup(6,GPIO.IN)
	GPIO.setup(13,GPIO.IN)
	GPIO.setup(19,GPIO.IN)
	cIDmax=2
	def buttomHandler(self):
		while True:
			if GPIO.input(5)==0:
				self.main()
			elif GPIO.input(6)==0:
				self.cIDm()
			elif GPIO.input(13)==0:
				self.cIDp()
			elif GPIO.input(19)==0:
				self.shutdown()
				self.confirmHamdler()
	def confirmHamdler(self):
		while True:
			if GPIO.input(5)==0:
				self.main()
			elif GPIO.input(19)==0:
				self.confirm=1
				self.shutdown()
	def cIDp(self):
		self.containerID+=1
		if self.containerID>self.cIDmax:
			self.containerID=0
		self.main()
	def cIDm(self):
		self.containerID-=1
		if self.containerID<0:
			self.containerID=self.cIDmax
		self.main()

d=display()
def tRun(self,thread):
	pass
def tStop(self,id):
	pass

def signalHandle(signal, frame):
	d.quit()
	sys.exit(0)
signal.signal(signal.SIGTERM, signalHandle)
signal.signal(signal.SIGINT, signalHandle)
if __name__ == '__main__':
	while True:
		d.main()
		time.sleep(60)
		# break

