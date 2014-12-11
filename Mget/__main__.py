#!/usr/bin/env python3

import sys

if __package__ is None and not hasattr(sys, 'frozen'):
	import os.path

	path = os.path.realpath(os.path.abspath(__file__))
	sys.path.append(os.path.dirname(os.path.dirname(path)))

import Mget

if __name__ == '__main__':
	try: Mget.main()
	except KeyboardInterrupt:
		out = sys.stderr
		out.write('[MGet Info] Interrupted by user')
		out.flush()
		exit(1)
