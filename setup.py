#!/usr/bin/env python3 

__version__ = '1.4.6'

import glob
import os, warnings
from setuptools import setup, find_packages, Extension
from Cython.Distutils import build_ext

root = os.path.dirname(os.path.abspath(__file__))

userconf = os.path.join(os.path.expanduser('~'), '.config')
cpy_src = os.path.join(root, './Mget/utils/CPPMGET/')

ext_modules = [	Extension( "mgetsys",
		[cpy_src + 'cpycode.pyx', cpy_src + 'main.cpp', cpy_src + 'common.cpp'],
		extra_compile_args=["-std=c++11"], language="c++")]

files_spec = [	('share/doc/mget', ['README.md']),
		('', glob.glob('*.so')),
		(userconf, ['mget.conf'])]
data_files = []

for dirname, files in files_spec:
	resfiles = []
	for fn in files:
		if not os.path.exists(fn): warnings.warn('Skipping file %s.' % fn)
		else: resfiles.append(fn)
	data_files.append((dirname, resfiles))

params={'data_files': data_files,
	'entry_points': {'console_scripts': ['mget = Mget:main']}}
setup(
	name='mget',
	version=__version__,
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules,
	description='HTTP file/video downloader',
	long_description='Small command-line program to download videos from  mp4upload.com & video sharing site and other http urls. Written in Python3 and cython3 `Install using pip3`',
	author='Ramesh Mani Maran',
	author_email='mssg3r@gmail.com',
	packages=find_packages(),
	classifiers=[
	"Development Status :: 5 - Production/Stable",
	"Environment :: Console",
	"License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
	"Operating System :: POSIX :: Linux",
	"Topic :: Internet",
	"Programming Language :: Cython",
	"Programming Language :: Python :: 3.4",
	],
	keywords='download mget http file downloader video mp4upload',
	setup_requires = 'Cython',
	**params)

