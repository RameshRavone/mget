#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Hentaistar_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?([^\s<>"]+|www\.)?hentaistar\.net/(?:.*)'
	_PATTERN = r'\'file\': \'(.+?)\''

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VALID_URL, self.url): return None

		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		url = self.findall_regex(self._PATTERN, str(data['webpage']), 'hentaistar')
		filename = url.split('/')[-1]

		if not url: return None

		return {'url': url,
			'filename': filename}
