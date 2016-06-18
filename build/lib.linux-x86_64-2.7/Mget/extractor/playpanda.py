#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Playpanda_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?([^\s<>"]+|www\.)?playpanda\.net/(?:.*)'
	_PATTERN = r'url: \'([^\s<>"]+{}[^\s<>"]+)\''

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VALID_URL, self.url): return None
		filename = self.url.split('/')[-1]
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		url = self.findall_regex(self._PATTERN.format(filename), str(data['webpage']), 'playpanda')

		if not url: return None

		return {'url': url,
			'filename': filename}
