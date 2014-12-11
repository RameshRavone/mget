#!/usr/bin/env python3

import re
from ..utils import std
from .common import InfoExtractor

class Auengine_io_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?(?:www\.)?auengine\.io/embed/(?:.*)'
	_VIDEO_ID = r'^(?:https?://)?([^\s<>"]+|www\.)?auengine\.io/embed/([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VALID_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_ID, self.url, 'videonest')
		data = self._get_webpage(self.url, self.client,\
					Req_head = {'User-Agent':std.FUA}, wpage=self.wpage)
		url = self.findall_regex(r'file: \'(.+?)\'', str(data['webpage']), 'videonest')

		if not url: return None

#		filename = self.file_name_html('head/title',str(data["webpage"]))
		return {'url': url,
			'filename': self.getFilename(url)}
