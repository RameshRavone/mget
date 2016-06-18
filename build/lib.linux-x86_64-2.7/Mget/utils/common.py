#!/usr/bin/env python3

import os, sys
import locale
import platform
import subprocess 

from http.client import responses
from . import ( std,strip_site,_error,urlparse,write_string,_stderr,report,report_error,trouble )

FILE_EXIST = "\nThe file is already fully retrieved; nothing to do.\n"

def delimiter_caps (string, d = '_'):
	return " ".join("%s" % s.capitalize() for s in string.split(d))

def pref_encoding():
	try: pref = locale.getpreferredencoding(); u'MGet'.encode(pref)
	except: pref = 'UTF-8'
	return pref

def platform_name():
	result = platform.platform()
	if isinstance(result, bytes):
		result = result.decode(pref_encoding())

	assert isinstance(result, str)
	return result

def EXFilename(filename):

	idx = 1
	dirname = '.'
	name, ext = filename.rsplit('.', 1)
	names = [x for x in os.listdir(dirname) if x.startswith(name)]
	names = [x.rsplit('.', 1)[0] for x in names]
	suffixes = [x.replace(name, '') for x in names]

	suffixes = [x[2:-1] for x in suffixes if x.startswith('-(') and x.endswith(')')]
	indexes  = [int(x) for x in suffixes if set(x) <= set('0123456789')]
	if indexes: idx += sorted(indexes)[-1]
	return ('%s-(%d).%s' % (name, idx, ext))

def debug_info(info):
	report = []
	proxy_map = info.get('proxy') or ''
	report.append("Python Version %s %s" % (platform.python_version(),platform_name()))
	report.append("Proxy map %s" % {proxy_map})

	write_string("\n".join("[debug] %s" % x for x in report))

def write_info(info):
	result = []

	result.append("\n".join("%s" % x for x in info.get('report')))
	result.append("Python Version %s %s\n" % (platform.python_version(),platform_name()))
	result.append("Default Url\t: %s" % info.get('defurl'))
	result.append("Url\t\t: %s" % info.get('url'))
	result.append("Proxy\t\t: %s" % ({} if info.get('proxy') == None else info.get('proxy')))
	result.append("Status\t\t: %s" % info.get('status'))
	result.append("Type\t\t: %s" % info.get('type'))
	result.append("Filename\t: %s" % info.get('filename'))
	result.append("Filesize\t: %s" % info.get('filesize'))
	result.append("Headers\t\t: %s" % (dict(info.get('headers'))))

	data = "\n".join("%s" % x for x in result)

	log_filename = info.get('log_file')
	if os.path.exists(log_filename): log_filename = EXFilename(log_filename)
	with open(log_filename, 'w') as f:
		f.write(data)
		report('Done Writting information to %s\n' % info.get('log_file'))
	return True

def check_exe(exe, args=[]):
	try: subprocess.Popen( [exe] + args,\
				stdout = subprocess.PIPE, stderr = subprocess.PIPE ).communicate()
	except OSError: return False
	return exe

def mangafox_url (url, volume, chapter, page):
	sufix = "v%02d/c%03d/%d.html" % (volume or 1,chapter or 1,page or 1)

	if url[-1] != '/': url += '/'

	# http://mangafox.me/manga/tokyo_ghoul/v09/c084/1.html
	# Manga start page
	return {"url": url + sufix, "start-page": page}
