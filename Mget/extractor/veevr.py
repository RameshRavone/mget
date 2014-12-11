#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Veevr_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?(?:www\.)?veevr\.com/embed/([a-z-A-Z-0-9]+)'
	_PATTERN = r'file: "([^\s<>"]+)"'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'veevr')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		url = self.findall_regex(self._PATTERN, str(data['webpage']), 'veevr')

		if not url: return None

		return {'url': url,
			'filename': self.getFilename(url)}

