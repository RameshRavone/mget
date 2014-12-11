MGet - Download from video sharing sites, manga from mangafox and MGet is also a file downloader which currently support HTTP/HTTPS.

# Implementing cython from 1.1.2 > *.

# SYNOPSIS
mget [OPTIONS] URL [URL...]

# INSTALLATION
New Feature - Manga download from mangafox.me
To install it right away for all UNIX users (Linux, OS X, etc.), type:
	# Install using pip:
	pip3 install mget (or) pip3 install --upgrade mget

	# Install from source:
	python3 setup.py install

# DESCRIPTION
**MGet** is a small command-line program to download videos from
Mp4upload and a few more sites. It requires the Python interpreter, version
3.+, and it is not platform specific. It should work on
your Unix box, on Windows or on Mac OS X. It is released to the public domain,
which means you can modify it, redistribute it or use it however you like.

Download file with ease! Send your request to mssg3r@gmail.com.

Examples:

    # TEST:
    mget [options..] <URL>

    #Download Embed video
    mget -G <URL>

    #Download some amount(Percent%) of file only
    mget -p 90 <URL>

    #Change download File buffer size (KB)
    mget --buffer 3 <URL>

    #Download list of urls from a file
    mget -i <file>

    #Download with proxy
    mget --proxy IP:PORT <URL>

    #Post-process converting video formats
    mget --recode-video FORMAT <url> // which will recode the downloaded video into given format

    #Download manga
    mangafox url = "http://mangafox.me/manga/${series}/v01/c001/1.html"
    mget <mangafox url> 
    mget --start-page <mangafox url>

    # Check mget -h for more options

# FAQ

## How to get embed url?

use mget -G option to automatically extract embed url from page (Supported: `animewaffle.tv`, animeram.eu, cc-anime.com).
MGet 1.1.2 > * does't need this it's default.

### I get HTTP error 402 when trying to download a video. What's this?

Apparently Some site requires some clearance before downloading, So please point the url to browser and export the cookie-file use that file to pass the clearance

### I have downloaded a video but how can I play it?

Once the video is fully downloaded, use any video player, such as [vlc](http://www.videolan.org) or [mplayer](http://www.mplayerhq.hu/).

####################################################################################################

Send your Request to mssg3r@gmail.com.
