#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Playlist_IE(InfoExtractor):
	_VIDEO_URL = r'^(?:https?://)?([^\s<>"]+|www\.)?(mp4upload|animeram|cc-anime)\.(tv|com|eu)/([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)
		self.site = kwargs.pop('site', None)

	def _extract_info(self, **kwargs):
		if not re.match (self._VIDEO_URL, self.url): return None
		video_id = self.search_regex (self._VIDEO_URL, self.url, 'playlist_url')
		data = self._get_webpage (self.url, self.client, wpage=self.wpage)
		urls = self.findall_urls (str(data['webpage']))
		if self.wplaylist:
			try: 
				with open(video_id, 'w') as fileObj:
					urls = "\n".join("%s" % url for url in urls)
					fileObj.write(urls)
			except IOError:
				common.report ("Urls written to file: " + video_id)
				return False

		return {'urls': urls}

	def findall_urls (self, webpage):
		pass
