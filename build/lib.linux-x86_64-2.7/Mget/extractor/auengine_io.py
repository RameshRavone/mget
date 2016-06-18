#!/usr/bin/env python3

import re
from ..utils import std
from .common import InfoExtractor

class Auengine_io_IE(InfoExtractor):
	#http://www.auengine.io/embed/C7Y9vrGocfXngLaFn01y
	_VALID_URL = r'^(?:https?://)?(?:www\.)?auengine\.io/embed/(?:.*)'
	_VIDEO_URL = r'^(?:https?://)?(?:www\.)?auengine\.io/embed/([a-z-A-Z-0-9]+)'
	_PATTERN = r'file: \'(http://s[0-9]+\.auengine\.io/[^\s<>"]+.mp4)\''

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VALID_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'auengine_io')
		data = self._get_webpage(self.url, self.client,\
					Req_head = {'User-Agent':std.FUA}, wpage=self.wpage)

		url = self.findall_regex(self._PATTERN, str(data['webpage']), 'auengine_io')

		if not url: return None

		filename = self.file_name_html('title',str(data["webpage"]), video_id)
		return {'url': url,
			'filename': filename or self.getFilename(url)}
