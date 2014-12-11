#!/usr/bin/env python3

import io
import zlib
from . import (std, urllib, urlparse, common)

class RedirectHandler(urllib.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		if "location" in headers: newurl = headers["location"]
		elif "uri" in headers: newurl = headers["uri"]
		else: return

		urlparts = urlparse.urlparse(newurl)
		if urlparts.scheme not in ('http', 'https', ''):
			raise HTTPError(newurl, code,\
				 "%s - Redirection to url '%s' is not allowed" % (msg, newurl),\
				headers, fp)

		if not urlparts.path:
			urlparts = list(urlparts)
			urlparts[2] = "/"

		newurl = urlparse.urlunparse(urlparts)
		newurl = urlparse.urljoin(req.full_url, newurl)

		common.report("Status code: %s %s" % (code, common.responses[code]))
		common.report("Following: %s" % (newurl))

		new = self.redirect_request(req, fp, code, msg, headers, newurl)
		if new is None: return

		if hasattr(req, 'redirect_dict'):
			visited = new.redirect_dict = req.redirect_dict
			if (visited.get(newurl, 0) >= self.max_repeats or 
				len(visited) >= self.max_redirections):
				raise HTTPError(req.full_url, code, self.inf_msg + msg, headers, fp)
		else:
			visited = new.redirect_dict = req.redirect_dict = {}
			visited[newurl] = visited.get(newurl, 0) + 1

		fp.read()
		fp.close()

		return self.parent.open(new, timeout=req.timeout)

	http_error_301 = http_error_303 = http_error_307 = http_error_302

class MGetDLHandler(urllib.HTTPHandler):

	@staticmethod
	def decompress(data, deflate):
		d = zlib.decompressobj(-zlib.MAX_WBITS if deflate else 16+zlib.MAX_WBITS)
		return d.decompress(data)

	@staticmethod
	def addInfourl(fileObj, headers, url, code):
		if hasattr(urllib.addinfourl, 'getcode'):
			return urllib.addinfourl(fileObj, headers, url, code)
		ret = urllib.addinfourl(fileObj, headers, url)
		ret.code = code
		return ret

	def http_request(self, req):
		for k, v in std.headers.items():
			if k in req.headers: del req.headers[k]
			req.add_header(k, v)
		if 'No-encoding' in req.headers:
			if 'Accept-encoding' in req.headers: del req.headers['Accept-encoding']

		return req

	def http_response(self, request, response):
		_resp = response
		enc_type = response.headers.get('content-encoding', '')

		if enc_type in ('gzip', 'deflate'):
			gz = io.BytesIO(self.decompress(response.read(), True if enc_type == 'deflate' else False))
			response = self.addInfourl(gz, _resp.headers, _resp.url, _resp.code)
			response.msg = _resp.msg
		return response

	https_request = http_request
	https_response = http_response

