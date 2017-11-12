from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime
import time
import sys
import os
from api import api


class display(api):
	WIDTH = 176
	HEIGHT = 264
	warning = False
	message = False
	stop = False
	threads = []
	containerID = 0
	confirm = None
	menuL = [u"设置", u"上页", u"下页", u"关机"]

	def newImage(self):
		self.image = Image.new('1', (self.WIDTH, self.HEIGHT), 255)
		self.draw = ImageDraw.Draw(self.image)

	def main(self):
		self.newImage()
		self.menuRender(self.draw)
		self.settingShow(self.draw)
		self.show(self.image)

	def show(self, image):
		image.show()
		return True

	def menuRender(self, draw):
		fontM = ImageFont.truetype(
			'C:/Windows/Fonts/simfang.ttf', 17)
		x = 1
		for i in self.menuL:
			self.draw.rectangle((x, self.HEIGHT - 18, x + 42, self.HEIGHT), fill=0)
			self.draw.text((x + 5, self.HEIGHT - 18), i, font=fontM, fill=255)
			x += 44

	def smallTimeRender(self, draw,text="My Rpi ePaper"):
		now = datetime.datetime.now()
		fontS = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 12)
		self.draw.text((148, -1), now.strftime("%H:%M"), font=fontS, fill=0)
		self.draw.text((116, -1), now.strftime(u"%m-%d"), font=fontS, fill=0)
		self.draw.text((0, -1),text, font=fontS, fill=0)
		self.draw.line((0,14,self.WIDTH,14),fill=0)

	def settingShow(self,draw):
		self.smallTimeRender(self.draw,"设置")
		fontB = ImageFont.truetype('C:/Windows/Fonts/Dengb.ttf', 32)
		fontS = ImageFont.truetype('C:/Windows/Fonts/Dengb.ttf', 16)
		y=17
		self.draw.text((0, y), "设置界面", font=fontB, fill=0)
		y+=33
		self.draw.line((0,y, self.WIDTH, y), fill=0)
		y+=2
		settings=[
			"系统设置",
			"Wi-Fi设置",
			"监控设置",
			"其他设置",
			"shezhi设置"]
		for i in range(len(settings)):
			self.draw.text((0, y), "%d.%s"%(i,settings[i]), font=fontS, fill=0)
			y+=18

	def contextShow(self,draw):
		fontS = ImageFont.truetype('C:/Windows/Fonts/Dengb.ttf', 16)
		self.draw.text((0,20),"人生就像一场戏\n因为有缘才相聚\nTest",font=fontS,fill=0)
	def datetimeRender(self,draw):
		now = datetime.datetime.now()
		fontB = ImageFont.truetype('ePaper/pixelmix.ttf', 56)
		self.draw.text((0, 0), now.strftime("%H:%M"), font=fontB, fill=0)
		fontM = ImageFont.truetype('ePaper/pixelmix.ttf', 18)
		self.draw.rectangle((0, 60, 176, 80), fill=0)
		self.draw.text((2, 60), now.strftime(u"%y-%m-%d %a"), font=fontM, fill=255)

	def quit(self):
		self.message = True
		self.info = u"已退出"
		self.main()
		print ("Quit")


display().main()
