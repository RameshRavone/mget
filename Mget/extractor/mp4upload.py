#!/usr/bin/env python3

import os, re
from .common import InfoExtractor

# http://www1.mp4upload.com:182/d/swxv2dsez3b4quuod6ub6jcwidplnz7jeq2xk4r274cqsdhshix7o7rg/video.mp4

class Mp4upload_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?(?:www\.)?mp4upload\.com/embed-([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info (self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'mp4upload')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		webpage = re.sub('\s+', '', str(data['webpage']))
		url = self.findall_regex(r'clip:{url:\'(.+?)\',', webpage, 'mp4upload')

#		d = self.search_regex(',\'(.+?)\'.split', str(data['webpage']), 'mp4upload')
#		r = (d.split('|')[2:])

#		for val in r:
#			if len(val) > 50: token = val

#		url = "http://www4.mp4upload.com:182/d/{}/video.mp4".format(token);
		if not url: return None

		url = self.remove_query(url)
		name, ext = self.getFilename(url).split('.')
		filename = "%s-%s.%s" % (name,video_id,ext)

		return {'url': url,
			'filename': filename}


