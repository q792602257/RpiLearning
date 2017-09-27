#encoding:utf8
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
	headers={"Connection":"Keep-Alive"}
	def getHTML(self,url,method="GET",data=None):
		if method=="GET":
			page=self.opener.get(url,headers=self.headers)
			html=page.text
		elif method=="POST":
			page=self.opener.post(url,data=data,headers=self.headers)
			html=page.text
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
		for detail in jdata["value"][0]["weatherDetailsInfo"]["weather3HoursDetailsInfos"][:3]:
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
a=api()
# print a.weatherHandler()["detail"][3]