#!/usr/bin/env python3

import re
from .common import InfoExtractor

# "0://8.7.6.5:g/d/f/video.mp4"
# http://62.210.201.56:8080/d/qqg7fgin7ruynurbp5l23uoz5xr3c5txrsdc3vyi3agt4uth3fmunih2/v.mp4

class Videonest_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?([^\s<>"]+|www\.)?videonest\.net/embed-([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VIDEO_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_URL, self.url, 'videonest')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		d = self.search_regex(r"\'http(.+?)\'.split", str(data['webpage']), 'videonest')
		r = (d.split('|'))

#		z = r[0].split(',')
#		url = z[0].replace('0://', '')
#		url = url.strip('\.\-\:')

		for val in r:
			if len(val) > 50: token = val

		ip = "%s.%s.%s.%s" % (r[8], r[7], r[6], r[5])
		return {'url': "http://%s:%s/d/%s/video.mp4" % (ip,"8080",token),
			'filename': "v-%s.mp4" % (video_id)}

		(name, ext) = self.getFilename(url).split('.')
		filename = "%s-%s.%s" % (name,video_id,ext)

		return {'url': url,
			'video_id': video_id,
			'filename': filename}
