# Media68 - Accessing media files with the help of Algol 68 Genie

These programs comprise a small project following on from the VCPGUI
project with the goal of again using Algol 68 Genie, this time to help 
access "media files" on a local area network and to play Internet
radio streams. The programs only work on Linux.

The programs fall into three categories:

- Selecting and playing media files that are accessible from the
  machine used for viewing them. The files must be either on 
  local disks or mounted from an SMB or NFS server (or similar).
  The `video68.sh` script starts a program to select appropriate files
  and run `mpv` to play them. The files are expected to be stored in
  a multi-level directory tree arrangement, perhaps starting with a 
  "category" (e.g. "movies" and "tv"), then "genre" then "title".
  This multi-level arrangement might be imposed on a less ordered
  arrangement using symbolic links (this is for the user to choose
  and implement). The `audio68.sh` script uses the 
  same program to choose audio files. These might be arranged by "artist
  name", then "album name" then "track name". The `books68.sh` script
  uses the same program again (`select68.a68`) to allow books, perhaps ordered
  by "category name", "author name" and "book title" to be chosen and
  presented (at present, only PDF format is used).
- Selecting and playing Internet audio streams described by `.m3u` files.
  This is done by `radio68.sh`, which uses `radio68.a68` to parse `.m3u`
  files and play streams slected from them (again, with `mpv`).
- Generating a static web site using the same file directory structures
  navigated by `select68.a68`, creating HTML files with HTML 5 contents
  that "mimic" the file tree containing the "media assets". The resulting
  web site can be used with a local web server (NGINX has been used so far)
  to allow a web browser on almost any modern mobile device to
  browse and play the same assets that can be accessed with `video68.sh`,
  `audio68.sh` and `books68.sh`. This will work so long as the mobile device
  is on the same LAN as the local web server, and screen sharing or Bluetooth
  on the mobile device can be used to present the material on large screen
  displays and high quality audio systems.
  
Recently (writing in October 2026), there has been a lot of interest in 
"locally hosted" media libraries. This seems to be a reaction to the "subscription
model" which has taken over so much over the last decade or so.

There are very sophisticated open source solutions available for these tasks,
such as "Jellyfin". In contrast, the programs here give a very basic experience with no
"eye candy" at all. But they do do what is *necessary* for their purpose.

Note that there are no programs here which try to deal with libraries of photographs.
Unlike the "media" these programs handle, photographs do not have "titles" which can
be used easily to identify them. I am looking into minimal approaches to browsing
image collections but it needs a lot more thought! (I wrote a Python program that 
did this in 2012 or thereabouts, but it used a database of sorts and isn't useful
for web browser based approaches -- it has its own OpenGL based GUI).

## Installation

You must first install (ideally from source) Algol 68 Genie. This can be downloaded
from Marcel van der Veer's website [here](https://algol68genie.nl/en/algol-68-genie).
This superb software can be built from source in under ten minutes, typically. See
the instructions that come with the source code for details of the build process.
Most Linux distributions have a pre-built package available, but they may have quite
old versions.

You may need to mount SMB shares on the machine(s) where you want to run `video68.sh`,
`audio68.sh` and `books68.sh`. This may require installing relevant packages
on your Linux system. For example, `smbclient` and `cifs-utils` are needed for
Debian (and Ubuntu).

You will need to install `mpv` for video and audio replay. 

If you want to use the static web site generation feature so you can access your media
from mobile devices (or any modern web browser) on your LAN, you will need to install
and configure a web server on some machine on your LAN. The NGINX server has been used
with this software during development, but any properly configured local server should 
work (probably).

Once the pre-requisites are installed, view and if necessary modify the `install.sh`
script. This installs essential script files in `/usr/local/bin` (unless modified)
and installs a configuration file for `mpv`.

Next, copy the file `scripts/select_vars.sh` and edit it. Change the line defining
`MEDIA68_HOME` to refer to the directory to which you have cloned the `media68`
Git repository. Change the lines defining `VIDEO68_MOUNT`, `AUDIO68_MOUNT` and
`BOOKS68_MOUNT` to refer to the top level directories of the file trees that contain
your video, audio and book media assets respectively.

These file trees may often be on a file server machine which exports them via SMB
shares. Example scripts that mount SMB shares for audio, video and book file trees
are provided in the `scripts` directory: `mountaudio.sh`, `mountvideo.sh` and
`mountbooks.sh`. Obviously, these will have to be modified for your purposes
(if they are used at all)!

## Basic Usage

The three shell scripts (`video68.sh`, `audio68.sh` and `books68.sh`) allow video,
audio and book asset file trees to be browsed and the assets played or viewed by using a 
minimal command line interface approach.

Each script opens a new detached command line window running the `select68.a68` program
with appropriate arguments for the three different tasks. When started, a list of
directories and relevant files in the top level directory is presented (or, in the
audio case, an "alphabetic tab list" which shows the letters of the alphabet used
as the first character of top level sub-directories, as the top level is likely to
contain too many files to conveniently navigate otherwise). 

An entry in the list is selected by typing its "index number", which preceeds each
file name in the list. This will be one or two digits long (almost always). When the
directory tree navigated in this way reaches a "terminal file" (a video data file,
audio data file or book data file), the "terminal file" is played by `mpv` or
displayed by a PDF reader,

In the case of audio data, the final directory typically contains all the audio files
for an "album". A special sorting scheme is used to make sure these files are presented
in the order they were meant to be played in the album. Responding with the option "p"
instead of an index number will play *all* the audio files in the directory, in the
order they are presented.

And that's it! A very bare bones approach to accessing media libraries ...

The static web site generator essentially makes this scheme work on mobile devices
through a web browser. It uses the same file trees as the `select68.a68` based
scripts use, transforming them into HTML files containing links to "terminal files"
or other HTML pages that present the next lower level directory names. Clicking
through these links navigates the file tree (or, rather, a "mimic" of the file tree)
in the same way as selecting list
index numbers does. The media assets are ultimately "played" by an appropriate
HTML 5 "player".

Detailed information on how to use the static web site generator program
(`files_to_html.a68`), along with examples and hints on how to configure the
web server which will host the generated web site, is given in the comment
block at the top of the program.

The `radio68.sh`/`radio68.a68` program implements a fixed two level "directory"
structure. The top level directory can contain any number of `.m3u` files, each
of which can define any number of Internet radio streams. The same list selection
model used by the other scripts (and implemented by `select68.a68`) first allows
the user to choose one of the `.m3u` files, then select one of the streams it
defines, which will start playing when selected. Being streams, these should
never come to an end (end of file), and, if they do as a result of some problem
somewhere, `mpv` is just restarted to continue trying to play the stream. If the
user ends `mpv` using the `q` key, a new stream or `.m3u` file can be chosen.

Note that it may be necessary to periodically update the `.m3u` files, as it
seems that links can change (well, it is said that the BBC radio station links
often do, and they also have very obscure names -- for reasons best known 
to the BBC). 
