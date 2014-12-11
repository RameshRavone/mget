#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Ftwcdn_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?([^\s<>"]+|www\.)?ftwcdn\.com/([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'ftwcdn')
		url = self.get_embed_url (self.url, self.client, self.wpage, pat='source')
#		url = self.findall_regex(r'', str(data['webpage']), '')
		filename = self.getFilename(url)

		return {'url': url,
			'filename': filename}

