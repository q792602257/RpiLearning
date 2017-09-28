#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib2 , re , requests , os , urllib , glob , MySQLdb
import sys , json , http.cookiejar , time , threading
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

class MySQL():
	def __init__(self):
		self.conn= MySQLdb.connect(
			host='www.himei.top',
			port = 3306,
			user='root',
			passwd='cc1123yhq',
			db ='Images',
			charset="utf8",
			)
		self.sql=self.conn.cursor()
	def SQLAdd(self,col,val):
		self.sql.execute('INSERT INTO `eh` (%s) VALUES (%s)'%(col,val.encode("utf-8")))
		print "MySQL Add OK"
		self.sql.close()
		self.conn.commit()
		return True
	def SQLQuery(self,col,where):
		a = self.sql.execute('select %s from `eh` %s'%(col,where))
		data=self.sql.fetchall()
		self.sql.close()
		self.conn.commit()
		return data
	def SQLUpdate(self,col,val,id):
		self.sql.execute('UPDATE `eh` (%s) VALUES (%s) where id=%s'%(col,val.encode("utf-8"),id))
		print "MySQL Add OK"
		self.sql.close()
		self.conn.commit()
		return True
class eHentai(MySQL):
	page=0
	opener = requests.Session()
	opener.cookies = http.cookiejar.MozillaCookieJar()
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
			'Accept-Encoding':'gzip, deflate',
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Referer": "https://e-hentai.org/",
			"Connection": "keep-alive",}
	def eLogin(self):
		url = u'https://forums.e-hentai.org/index.php?act=Login&CODE=01'
		data= {"CookieDate":1,"UserName":"yxzyxz123456","PassWord":"yxzyxz123456"}
		page= self.opener.post(url,data=data,headers=self.headers)
		if page.text.find("yxzyxz123456") >= 0:
			print "login Success"
			return True
		else:
			print "Login Failed"
			return False
	def getHtml(self,url,data=None):
		time.sleep(5)
		page = self.opener.get(url,headers=self.headers)
		html = page.text
		return html
	def Downloader(self,url):
		if not os.path.exists(os.path.join("eH",self.id)):
			os.makedirs(os.path.join("eH",self.id))
		if not os.path.exists(os.path.join("eH",self.id,"%s.jpg"%self.q)):
			page = self.opener.get(url,headers=self.headers,timeout=15)
			data = page.content
			with open(os.path.join("eH",self.id,"%s.jpg"%self.q),"wb") as f:
				f.write(data)
	def resume(self):
		res=self.SQLQuery("url,id,q","where continue=1")
		for each in res:
			print 'continue Download'
			self.id = each[1]
			self.q=int(each[2])
			self.url=each[0]
			self.imgHandler(self.url)
	def imgHandler(self,url1):
		self.q += 1
		print "\t%s"%self.q
		html = self.getHtml(url1)
		soup = BeautifulSoup(html,"html.parser")
		try:
			url2 = soup.select("div#i3 > a")[0]["href"]
			if url1 != url2:
				self.url = url2
				imgu=soup.select("div#i3 > a > img")[0]["src"]
				self.Downloader(imgu)
				self.imgHandler(url2)
			else:
				return True
		except Exception as e:
			print e
			return False
	def listHandler(self):
		ret=[]
		while True:
			html = self.getHtml("https://e-hentai.org/?page=%s"%self.page)
			asoup = BeautifulSoup(html,"html.parser")
			try:
				threads=asoup.select("div.ido > div > table.itg")[0].find_all(class_=re.compile("gtr."))
				for thread in threads:
					t={}
					t["cata"] = thread.select("td.itdc > a > img")[0]["alt"]
					t["title"]= thread.select("td.itd > div > div.it5 > a")[0].get_text()
					t["url"]  = thread.select("td.itd > div > div.it5 > a")[0]["href"]
					t["id"]=t["url"].split("/")[-3]
					ret.append(t)
			except Exception as e:
				print e
				return False
			self.threadHandler(ret)
			print "Wait For 5 Minute\t",
			self.page+=1
			time.sleep(300)
			print "And Continue"
	def threadHandler(self,ret):
		for thread in ret:
			if not self.SQLQuery("id","where id=%s"%thread['id']):
				bhtml = self.getHtml(thread['url'])
				bsoup = BeautifulSoup(bhtml,"html.parser")
				if len(bsoup.find_all(class_="gdtl")) != 0:
					burl = bsoup.find_all(class_="gdtl")[0].select("a")[0]["href"]
				elif len(bsoup.find_all(class_="gdtm")) != 0:
					burl = bsoup.find_all(class_="gdtm")[0].select("a")[0]["href"]
				else:
					print bsoup.get_text()
					continue
				self.imgHandler(burl)					
			else:
				print "Exist:\t%s\n%s"%(thread["id"],thread["title"])
				continue

	def main(self):
		self.eLogin()
		try:
			self.resume()
			self.listHandler()
		except Exception as e:
			print e
			print "\nWait 2 Minute..."
			time.sleep(120)
			print "And Retry"
			self.main()
e=eHentai()
e.main()