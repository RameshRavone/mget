#!/usr/bin/env python3

import os, sys
import subprocess

from . import common, PostProcessError

class postProcessor(object):
	def __init__ (self, params):
		self.params = params

	def run (self, info):
		return (None, info)

class AVconvProcess (postProcessor):
	def __init__ (self, info):
		self.info = info
		self.exes = self.detect_exe();

	def detect_exe (self):
		progs = ['avconv', 'ffmpeg']
		return dict(( prog, common.check_exe(prog, ['-version']) ) for prog in progs)

	def get_executer (self):
		if self.info.get("prefer_ffmpeg", False):
			return self.exes['ffmpeg'] or self.exes['avconv']

		return self.exes['avconv'] or self.exes['ffmpeg']

	def run_avconv (self, infile, outfile, opts = []):
		cmd = ( [self.get_executer(), '-y'] + ['-i', infile] + opts \
			+ [self._fname_arg(outfile)])
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = p.communicate()
		if p.returncode != 0:
			stderr = stderr.decode()
			msg = stderr.strip().split("\n")[-1]
			raise PostProcessError("Working")
		return True

	def processCodecs (self, ext):
		if ext in ['mp4', 'flv', 'avi', 'mkv']: return ["-c", "copy"]
		else: return []

	def _fname_arg (self, name):
		if name.startswith("-"): return "./" + name
		return name

class VideoConv (AVconvProcess):
	def __init__ (self, details=False, format_to=None):
		AVconvProcess.__init__(self, details)
		self._format_to = format_to

	def run (self, info):
		path = info.get("filepath")
		prefix, sep, ext = path.rpartition('.')
		outpath = prefix + sep + self._format_to

		if info["ext"] == self._format_to:
			common.report( "%s formated video already exists in this path" \
					% self._format_to )
			return (True, info)

		common.report ( "Converting video from %s to %s, To destination: " \
				% (info.get("ext"), self._format_to) + outpath )
		self.run_avconv (path, outpath, self.processCodecs (self._format_to))
		return (True, info)
