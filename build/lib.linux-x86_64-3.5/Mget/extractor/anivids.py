#!/usr/bin/env python3

import re
from .common import InfoExtractor

#  http://178.162.201.96:8777/t2kfw4m73stp37l57bvdvinsuhbuvbwimjpagrbrutrkbr2knko454vrwiba/v.mp4

class Anivids_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?(?:www\.)?anivids\.tv/embed-([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'anivids')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		d = self.search_regex(',\'(.+?)\'.split', str(data['webpage']), 'anivids')
		r = (d.split('|')[2:])

		for val in r:
			if len(val) > 50: token = val

		return {'url': "http://%s:%s/%s/video.mp4" % ("178.162.201.96","8777",token),
			'filename': "video-%s.mp4" % (video_id)}
