#!/usr/bin/env python3

import sys
import socket
import traceback
from . import urllib

def FormatTrace(exc_info):
	ex_type = exc_info[0]
	ex_value = exc_info[1]
	tb = traceback.extract_tb(exc_info[2])

	etype = ex_type.__name__
	emodule = ex_type.__module__

	if emodule not in ('__main__', 'builtins'):
		etype = etype + '.' + emodule

	r = [	"File: %s, line %s, <module> %s" % (tb[0], tb[1], tb[2]),
		"With: %s" % tb[3],
		"%s: %s"% (etype, ex_value)]

	return ''.join("[debug] %s\n" % x for x in r)

class ExtractorError(Exception):
	def __init__(self, msg, excepted=False, cause=None, exc_info=None):
		if sys.exc_info()[0] in (urllib.URLError, socket.timeout): excepted = True
		if not excepted:
			msg = msg + " please report this issue to mssg3r@gmail.com. Be sure to call mget with the --verbose and include its complete output. Make sure you are using the latest version."

		super(ExtractorError, self).__init__(msg)
		self.msg = str(msg)
		self.exc_info = exc_info
		self.cause = cause

	def __str__(self): return self.msg
	def _trace(self): return FormatTrace(self.exc_info) if self.exc_info != None else "None"

class DownloadError(Exception):
	def __init__(self, msg, exc_info=None):
		super(DownloadError, self).__init__(msg)
		self.msg = str(msg)
		self.exc_info = exc_info

	def __str__(self): return self.msg
	def _trace(self): return FormatTrace(self.exc_info) if self.exc_info != None else "None"

class ContentTooShortError(Exception):
	def __init__(self, downloaded=None, expected=None):
		self.msg = "Content too short"
		self.downloaded = downloaded
		self.expected = expected

	def __str__(self): return 'Expected: %s, Recived: %s\r' % (self.expected,self.downloaded)
	def _trace(self): return 'None'

PostProcessError = DownloadError
