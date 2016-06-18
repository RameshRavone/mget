#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Videodrive_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?([^\s<>"]+|www\.)?videodrive\.tv/embed/([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)


	def _extract_info(self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'videonest')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		url = self.findall_regex(r'file: "(.+?)"', str(data['webpage']), 'videonest')

		if not url: return None

		name, ext = self.getFilename(url).split('.')
		filename = "%s-%s.%s" % (name,video_id,ext)
		return {'url': url,
			'filename': filename}
