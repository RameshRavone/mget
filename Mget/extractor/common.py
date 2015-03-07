#!/usr/bin/env python3

import re
import os, sys
import xml.etree.ElementTree as ET
from ..utils import strip_site, common, urlparse
from ..downloader import client, MyHTMLParser

class InfoExtractor(object):
	@staticmethod
	def _get_webpage(url, client, **kwargs):
		site = strip_site(url)
		wpage = kwargs.pop('wpage', False)
		Req_head = kwargs.pop('Req_head', {})

		urllibObj, req = client.urlopen(url,req_head=Req_head)
		con_type = urllibObj.info().get('Content-Type')
		charset = con_type.split('=')[1] if '=' in con_type else 'ISO-8859-1'
		webpage = urllibObj.read().decode(charset)
#		webpage = re.sub('\s+', '', webpage)
		if wpage:
			filename = site[0] + '.dump'
			with open(filename, 'w') as f:
				f.write(webpage)
				common.report("Webpage writtern to %s" % filename)

		if ("File was deleted" in webpage): return None
		return {'webpage': webpage,
			'urllibObj': urllibObj,
			'request': req}

	@staticmethod
	def search_regex(pattern, string, name, flags=0):
		mObj = re.search(pattern, string, flags)
		if mObj: return next(s for s in mObj.groups() if s is not None)
		return None

	@staticmethod
	def findall_regex(pattern, string, name):
		mObj = re.findall(pattern, string)
		if mObj: return next(s for s in mObj if s is not None)
		return None

	@staticmethod
	def get_param(url, param):
		query = urlparse.urlparse(url).query
		query = query.split('&')
		for i in query:
			if i.startswith(str(param + '=')): return i.split('=')[1]
		return None

	@staticmethod
	def getFilename(url):
		url = urlparse.unquote(url)
		filename = os.path.basename(urlparse.urlparse(url).path)

		if len(filename.strip(" \n\t.")) == 0: return None
		return urlparse.unquote_plus(filename)

	@staticmethod
	def get_embed_url(url, client, wpage, pat="iframe"):
		host = urlparse.urlparse(url).hostname
		data = InfoExtractor._get_webpage(url, client, wpage=wpage, hostname=host)
		p = MyHTMLParser(str(data['webpage']))
		return p.get_result(pat, 'src') or p.get_result('embed', 'src')

	@staticmethod
	def file_name_html(tag, data, video_id):
		titleRe = re.compile("<" + tag + ">(.+?)</"+ tag +">")
		title = titleRe.search(data).group(1)
		if title.endswith(".mp4"):
			title = title[:-4] + "-" + video_id + ".mp4"
			return title
		else: return None

	@staticmethod
	def remove_query(url):
		urlparts = urlparse.urlparse(url)

		if urlparts.query:
			urlparts = list(urlparts)
			urlparts[4] = ''

		return urlparse.urlunparse(urlparts)

	def gen_manga_urls (self, url, client, **kwargs):
		urls = []
		wpage = kwargs.pop("wpage", False)

		host = urlparse.urlparse(url).hostname
		data = InfoExtractor._get_webpage(url, client, wpage=wpage, hostname=host)

		totalPages = self.search_regex(r'total_pages=([0-9]+);',str(data['webpage']),'manga')
		series = self.search_regex(r'series_code="(.+?)";',str(data['webpage']),'manga')
		chapter = self.search_regex(r'current_chapter="(.+?)";',str(data['webpage']),'manga')
		furl = self.search_regex(r'this.src=\'(.+?)\'',str(data['webpage']),'manga')

		prefix_url = furl[:-7]

		for i in list(range(1, int(totalPages)+1)): 
			urls.append(prefix_url + "%03d.jpg" % i)

		return {"urls": urls,
			"series": common.delimiter_caps(series),
			"chapter": chapter,
			'tot_download': totalPages}

# from  html file "title" tag
