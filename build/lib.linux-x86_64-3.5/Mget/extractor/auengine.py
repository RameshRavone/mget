#!/usr/bin/env python3

import re
from .common import InfoExtractor
from ..utils import urlparse, std
from .auengine_io import Auengine_io_IE


# "http://s45.auengine.com/vod/g8IjH2gKpM513KF8Q1J2zw/1419486404/vYCW5yg.mp4"
class Auengine_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?(?:www\.)?auengine\.com/(?:.*)'
	_VALID_URL_1 = r'^(?:https?://)?(?:www\.)?auengine\.io/embed/(?:.*)'

	_PATTERN = r'video_link = \'(.+?)\''

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if re.match(self._VALID_URL_1, self.url):
			res = Auengine_io_IE(self.url,client=self.client,wpage=self.wpage)
			return  res._extract_info()

		if not re.match(self._VALID_URL, self.url): return None
		video_id = self.get_param(self.url, 'file')
		req_head = {'User-Agent':std.FUA}
		data = self._get_webpage(self.url, self.client, Req_head=req_head, wpage=self.wpage)
		url = self.findall_regex(self._PATTERN, str(data['webpage']), 'auengine')

		if not url: return None

		filename = self.file_name_html('title', str(data["webpage"]), video_id)
		return {'url': urlparse.unquote(url),
			'video_id': video_id,
			'filename': filename or self.getFilename(url)}
