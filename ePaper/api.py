# -*- encoding:utf8 -*-
import requests
import json
# from cookiejar import MozillaCookieJar
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

class api():
	opener = requests.Session()
	# opener.cookies=MozillaCookieJar()
	times=0
	headers={"Connection": "Keep-Alive","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
	def getHTML(self,url,method="GET",data=None):
		try:
			if method=="GET":
				page=self.opener.get(url,headers=self.headers)
				html=page.text
			elif method=="POST":
				page=self.opener.post(url,data=data,headers=self.headers)
				html=page.text
		except Exception as e:
			print (e)
			html="{'Error'='{e}'}"
		finally:
			return html
	def weatherHandler(self):
		code="101240201"
		url="http://aider.meizu.com/app/weather/listWeather?cityIds=%s"%code
		html = self.getHTML(url)
		jdata=json.loads(html)
		ret={}
		ret["aqi"]=jdata["value"][0]["pm25"]["aqi"]
		ret["city"]=jdata["value"][0]["city"]
		ret["temp"]="%s(%s)℃"%(jdata["value"][0]["realtime"]["temp"],jdata["value"][0]["realtime"]["sendibleTemp"])
		ret["weather"]=jdata["value"][0]["realtime"]["weather"]
		ret["time"]=jdata["value"][0]["realtime"]["time"][11:16]
		ret["wet"]=jdata["value"][0]["realtime"]["sD"]
		ret["wind"]="%s%s"%(jdata["value"][0]["realtime"]["wD"],jdata["value"][0]["realtime"]["wS"])
		ret["detail"]=[]
		for detail in jdata["value"][0]["weatherDetailsInfo"]["weather3HoursDetailsInfos"]:
			t={}
			# t["temp"]="%s/%s℃"%(detail["highestTemperature"], detail["lowerestTemperature"])
			t["temp"]="%s℃"%(detail["highestTemperature"])
			t["weather"]=detail["weather"]
			t["stime"]=detail["startTime"][11:16]
			ret["detail"].append(t)
		ret["future"]=[]
		for future in jdata["value"][0]["weathers"][0:3]:
			t={}
			t["date"]=future["date"]
			t["week"]=future["week"].replace("星期","周")
			t["weather"]=future["weather"]
			t["sunrise"]=future["sun_rise_time"]
			t["sunset"]=future["sun_down_time"]
			t["temp"]="%s/%s℃"%(future["temp_day_c"],future["temp_night_c"])
			t["wind"]="%s%s"%(future["wd"],future["ws"])
			ret["future"].append(t)
		return ret
	def oneHandler(self):
		url = "http://v3.wufazhuce.com:8000/api/onelist/idlist/?channel=wdj&version=4.0.2&uuid=ffffffff-a90e-706a-63f7-ccf973aae5ee&platform=android"
		html = self.getHTML(url)
		jdata=json.loads(html)
		self.oneList=jdata["data"]
		ret=[]
		for one in self.oneList:
			url2="http://v3.wufazhuce.com:8000/api/onelist/%s/0?cchannel=wdj&version=4.0.2&uuid=ffffffff-a90e-706a-63f7-ccf973aae5ee&platform=android"%one
			html2=self.getHTML(url2)
			jdata2=json.loads(html2)
			ret.append(jdata2["data"]["content_list"][0]["forward"])
		return ret
	def newWeatherCodeHandler(self,code):
		weathercode={0:u"晴",1:u"多云",2:u"阴",3:u"阵雨",4:u"雷阵雨",5:u"雷阵雨并伴有冰雹",6:u"雨夹雪",7:u"小雨",
		8:u"中雨",9:u"大雨",10:u"暴雨",11:u"大暴雨",12:u"特大暴雨",13:u"阵雪",14:u"小雪",15:u"中雪",16:u"大雪",
		17:u"暴雪",18:u"雾",19:u"冻雨",20:u"沙尘暴",21:u"小雨-中雨",22:u"中雨-大雨",23:u"大雨-暴雨",
		24:u"暴雨-大暴雨",25:u"大暴雨-特大暴雨",26:u"小雪-中雪",27:u"中雪-大雪",28:u"大雪-暴雪",29:u"浮沉",
		30:u"扬沙",31:u"强沙尘暴",32:u"飑",33:u"龙卷风",34:u"若高吹雪",35:u"轻雾",53:u"霾",99:u"未知"}
		return weathercode[int(code)]
	def windHandler(self,direction="",speed=""):
		if len(direction)!=0:
			direction = float(direction) 
			if direction>337.5 and direction<=360.0:
				d = u"北风"
			elif direction > 292.5:
				d = u"西北风"
			elif direction > 247.5:
				d = u"西风"
			elif direction > 202.5:
				d = u"西南风"
			elif direction > 157.5:
				d = u"南风"
			elif direction > 112.5:
				d = u"东南风"
			elif direction > 67.5:
				d = u"东风"
			elif direction > 22.5:
				d = u"东北风"
			elif direction<= 22.5 and direction>=0.0:
				d = u"北风"
			else:
				d = u""
		else:
			d=u""
		if len(speed)!=0:
			speed = float(speed)
			if speed <= 1.0 and speed >= 0.0:
				s=u"0级"
			elif speed <= 6.0:
				s=u"1级"
			elif speed <= 11.0:
				s=u"2级"
			elif speed <= 19.0:
				s=u"3级"
			elif speed <= 28.0:
				s=u"4级"
			elif speed <= 38.0:
				s=u"5级"
			elif speed <= 49.0:
				s=u"6级"
			elif speed <= 61.0:
				s=u"7级"
			elif speed <= 74.0:
				s=u"8级"
			elif speed <= 88.0:
				s=u"9级"
			elif speed <= 102.0:
				s=u"10级"
			elif speed >  102.0:
				s=u"飓风"
			else:
				s=""
		else:
			d=u""
		return "%s%s"%(d,s)
	def newWeatherHandler(self):
		code="101240201"
		url="https://weatherapi.market.xiaomi.com/wtr-v3/weather/all?latitude=29.721263&longitude=115.999853&isLocated=true&locationKey=weathercn:%s&days=15&appKey=weather20151024&sign=zUFJoAR2ZVrDy1vF3D07&romVersion=7.11.9&appVersion=102&alpha=false&isGlobal=false&device=ido&modDevice=ido_xhdpi&locale=zh_cn"%code
		if self.times>5 or self.times==0:
			html = self.getHTML(url)
			self.times=1
		else:
			self.times+=1
			return self.oldret
		try:
			jdata=json.loads(html)
			if jdata.has_key('Error'):
				return jdata
			ret={}
			ret["aqi"]=jdata["aqi"]["aqi"]
			ret["city"]="九江"
			ret["tempRaw"]=int(jdata["current"]["temperature"]["value"])
			ret["temp"]="%s(%d)℃"%(jdata["current"]["temperature"]["value"],float(jdata["current"]["feelsLike"]["value"]))
			ret["pressure"]="%shPa"%(jdata["current"]["pressure"]["value"])
			ret["weather"]=self.newWeatherCodeHandler(jdata["current"]["weather"])
			ret["time"]=jdata["current"]["pubTime"][11:16]
			ret["wet"]="%s"%jdata["current"]["humidity"]
			ret["wind"]=self.windHandler(jdata["current"]["wind"]["direction"]['value'],jdata["current"]["wind"]["speed"]['value'])
			ret["detail"]=[]
			ret["future"]=[]
			for i in range(0,34):
				t={}
				t["tempRaw"]=int(jdata["forecastHourly"]["temperature"]["value"][i])
				t["temp"]=u"%s℃"%(jdata["forecastHourly"]["temperature"]["value"][i])
				t["weather"]=self.newWeatherCodeHandler(jdata["forecastHourly"]["weather"]["value"][i])
				t["stime"]=jdata["forecastHourly"]["wind"]["value"][i]["datetime"][11:16]
				t["wind"]=self.windHandler("",jdata["forecastHourly"]["wind"]['value'][i]["speed"])
				t["windRaw"]=float(jdata["forecastHourly"]["wind"]['value'][i]["speed"])
				ret["detail"].append(t)
			tmp=[u"今天",u"明天",u"后天"]
			for j in range(0,3):
				t={}
				# forecastDaily
				t["date"]=jdata["forecastDaily"]["sunRiseSet"]["value"][j]["from"][5:10]
				t["week"]=tmp[j]
				t1=jdata["forecastDaily"]["weather"]["value"][j]["from"]
				t2=jdata["forecastDaily"]["weather"]["value"][j]["to"]
				if t1==t2:
					t["weather"]=self.newWeatherCodeHandler(t1)
				else:
					t["weather"]=u"%s转%s"%(self.newWeatherCodeHandler(t1),self.newWeatherCodeHandler(t2))
				t["sunrise"]=jdata["forecastDaily"]["sunRiseSet"]["value"][j]["from"][11:16]
				t["sunset"]=jdata["forecastDaily"]["sunRiseSet"]["value"][j]["to"][11:16]
				t["temp"]=u"%s/%s℃"%(jdata["forecastDaily"]["temperature"]["value"][j]["from"],jdata["forecastDaily"]["temperature"]["value"][j]["to"])
				t["wind"]=self.windHandler(jdata["forecastDaily"]["wind"]["direction"]['value'][j]["from"],jdata["forecastDaily"]["wind"]["speed"]['value'][j]["from"])
				ret["future"].append(t)
			self.oldret=ret
			return ret
		except Exception as e:
			if vars().has_key('html'):
				print (html)
			print (e)
			if vars().has_key('self.oldret'):
				return self.oldret
			else:
				return {"Error":u"请连接网络"}
