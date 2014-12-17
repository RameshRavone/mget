MGet - Download from video sharing sites and MGet is a file downloader which currently support HTTP.

# Sorry, Implementing cython from 1.1.2 > *.
	If you need fully python based 

# SYNOPSIS
mget [OPTIONS] URL [URL...]

# INSTALLATION

To install it right away for all UNIX users (Linux, OS X, etc.), type:

    sudo wget http://mssg3r.cz.cc/downloads/latest/mget -O /usr/local/bin/mget
    sudo chmod a+x /usr/local/bin/mget

# DESCRIPTION
**MGet** is a small command-line program to download videos from
Mp4upload and a few more sites. It requires the Python interpreter, version
3.+, and it is not platform specific. It should work on
your Unix box, on Windows or on Mac OS X. It is released to the public domain,
which means you can modify it, redistribute it or use it however you like.

# Now Download videos from youtube as well (Experimental)

# OPTIONS
usage: 	mget [options..] URL [URL..]

optional arguments:
  -h, --help             show this help message and exit
  --version              show program's version number and exit

General arguments:
  -e, --list-extractors  Print supported Video sharing sites.
  -I, --ignore-errors    continue on download errors, e.g. to skip unavailable videos in urlfile.
  -m, --mirror           Download from mirror link.
  --ignore-config        Do not read configuration files (~/.config/mget.conf).
  -p PERCENT             How much percent to download default: (100.0).
  -U USER-AGENT          User Agent to use.

Download arguments:
  -T INT, --timeout INT  set timeout values in SECONDS.
  --no-resize-buffer     Do not resize the downloading buffer size.
  --retry-error          Retry on DownloadError and ContentTooShort Error's.
  --buffer SIZE          Download buffer size (--buffer 3) default 1 [1024].
  --waitretry SECONDS    Wait 1..SECONDS between retries of a retrieval.
  --proxy PROXY          Use the specified HTTP/HTTPS proxy.
  -f FORMAT              video format code for youtube: "-f 18" By default, MGet will pick the best quality.

Simulate arguments:
  -q, --quiet            activates quiet mode.
  -g, --get-url          Print Download url and exit.
  -G, --get-embed-url    Print embed url form the webpage, (Supported: animeram.eu, animewaffles.tv, cc-anime.com).
  -j, --dump-info        simulate, but print information.
  -v, --verbose          print various debugging information.
  --dump-user-agent      Print User-Agent in use.
  --dump-headers         Print Headers recived form server.
  --write-info           simulate, and write information to 'mget_info'.
  --newline              output progress bar as new lines.
  --write-page           Write downloaded pages to files in the current directory to debug.
  --debug                Print error debugging information.

Filesystem arguments:
  -c, --continue         Fource to resume download.
  --restart              Do not resume partially downloaded files (restart from beginning).
  --default-page PAGE    Change the default page name (normally this is `index.html'.).
  --log-file FILENAE     Filename to write the MGet log (Default is 'mget.log').
  --cookies FILE         file to read cookies from and dump cookie jar in.
  -i FILE                File with list of url to download.
  -O FILENAME            File name to save the output..

Download file with ease! Send your request to r4v0n3@gmail.com.

Examples:
    #Download Embed video
    mget [options..] http://animewaffles.tv/Player-Mahouka-Koukou-no-Rettousei-Episode-1-English-Subbed-41888

    #Download some amount(Percent%) of file only
    mget [options..] -p 90 <URL>

    #Download File buffer size (KB)
    mget [options..] --buffer 3 <URL>

    #Download list of files from a file
    mget [options..] -i <file>

    #Download with proxy
    mget [options..] --proxy IP:PORT <URL>

    # Check mget -h for more options

# FAQ

## How to get embed url?

use mget -G option to automatically extract embed url from page (Supported: `animewaffle.tv`, animeram.eu, cc-anime.com).
MGet 1.1.2 > * does't need this it's default.

### I get HTTP error 402 when trying to download a video. What's this?

Apparently Some site requires some clearance before downloading, So please point the url to browser and export the cookie-file use that file to pass the clearance

### I have downloaded a video but how can I play it?

Once the video is fully downloaded, use any video player, such as [vlc](http://www.videolan.org) or [mplayer](http://www.mplayerhq.hu/).

## Read Source ##

MGet is packed as an executable zipfile, simply unzip it (might need renaming to `mget.zip` first on some systems). If you modify the code, you can run it by executing the `__main__.py` file. To recompile the executable, run `./install.sh`.

####################################################################################################

Send your Request to r4v0n3@gmail.com.

