#!/usr/bin/env python3

__all__ = ['strip_site','std','client','common','MGet','VideoConv','ExtractorError','DownloadError',
'PostProcessError', 'ContentTooShortError','FormatTrace','sock_timeout','sock_error']

import re
import urllib.request as urllib
import urllib.parse as urlparse
import http.cookiejar as cookiejar
from html.parser import HTMLParser
from socket import ( timeout as sock_timeout, error as sock_error )

from mgetsys import MGet

_SITE_LIST = [	'mp4upload.com', 'trollvid.net', 'anivids.tv', 'auengine.com', 'auengine.io',
		'aniupload.com', 'yourupload.com', 'videonest.net', 'videodrive.tv', 'ftwcdn.com',
		'playpanda.net', 'veevr.com', 'video44.net', 'play44.net', 'bzoo.org', 'animebam.com']

def write_string(s,newline=True):
	if not newline and s[:1] == '\n': s = s[1:]
	MGet.write_string(str(s).encode('utf-8'))

def _error(msg = "", status = 0): MGet._error(str(msg).encode(), status)

_stderr = lambda msg: write_string('\n' + str(urlparse.unquote(str(msg))))
report = lambda msg: write_string('[MGet Info] ' + str(urlparse.unquote(str(msg))))
report_error = lambda msg: write_string('\n[MGet Error] ' + str(urlparse.unquote(str(msg))))
trouble = lambda msg: write_string('\nWARNING: ' + str(urlparse.unquote(str(msg))))

def strip_site(url):
	url = urlparse.urlparse(url).hostname

	try: hostname = re.match(r'(?:\w*://)?(?:.*\.)?([a-z-A-Z-0-9]*\.([a-z]*))', url).groups()[0]
	except: report_error("URL Not Valid!"); exit(1)

	return hostname, hostname.split('.')[0]

class Default(object): pass

std = Default()
std.UA = "Mozilla/5.0 (X11; Linux x86_64; rv:1.3) MGet/1.3 (MSSG3R 0.6.4)"
std.FUA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0"
std.headers = {	'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
std.share_site_list = [ 'animeram.eu','animewaffles.tv','cc-anime.com']
std.site_list = _SITE_LIST
std.MANGA_URL = r'^(?:https?://)?(?:www\.)?mangafox\.me/manga/(.+?)/v([-0-9-a-z-A-Z-.]+)/c([0-9-.]+)/([0-9]+\.html)'
std.EG_URL = "http://mangafox.me/manga/v${01}/c${001}/${1}.html"

from .exception import *
from .handlers import *
from .avconv import VideoConv
from ..downloader import client
