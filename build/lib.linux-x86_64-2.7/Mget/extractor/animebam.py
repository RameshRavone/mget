#!/usr/bin/env python3

# ULRhttp://animebam.com/embed/11236

import os, re
from .common import InfoExtractor

# http://www1.mp4upload.com:182/d/swxv2dsez3b4quuod6ub6jcwidplnz7jeq2xk4r274cqsdhshix7o7rg/video.mp4

class Animebam_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?(?:www\.)?animebam\.com/embed/([0-9]+)'
	_PATTERN = r'sources:[{file:"([^\s<>"]+.mp4)",'
	_PATTERN = r'file:"(http://oose.io/3edb86268524c186fd3a73f342f112d65e4c5715/video.mp4)"'
	_PATTERN = r'file: "(.+?)"'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info (self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'animebam')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)

		url = self.findall_regex(self._PATTERN, str(data['webpage']), 'animebam')

		if not url: return None

		url = self.remove_query(url)
		name, ext = self.getFilename(url).split('.')
		filename = "%s-%s.%s" % (name,video_id,ext)

		return {'url': url,
			'filename': filename}


