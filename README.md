# Media68 - Accessing media files with the help of Algol 68 Genie

These programs comprise a small project following on from the VCPGUI
project with the goal of again using Algol 68 Genie, this time to help 
access "media files" on a local area network and to play Internet
radio streams. **These programs only work on Linux**.

Recently (writing in October 2026), there has been renewed interest in 
"locally hosted" media libraries. This seems to be a negative reaction to the 
"subscription model" which has taken over so much in the last decade or so.

In addition to growing dissatisfaction with streaming services (many people
believe "ensh--tification" is very real), there may be another motive for making
a local media server: the media reflect *your* choices, the artists *you* chose to
support by buying their work, the things *you* like. 
Keeping those choices alive as the original
physical media become less accessible (devices to play them are becoming scarcer)
may necessitate a "computer based solution" of some kind.

There are very sophisticated open source solutions available for this,
such as "Jellyfin". In contrast, the programs here give a very basic experience with no
"eye candy" at all. But they do do what is *necessary* for their purpose.


## Introduction

The key idea on which this project builds is that "media files" can
be organised into a hierarchy represented by a directory tree. The lowest
level directories contain "terminal files" which are either the media files
themselves, or symbolic links to those files (the latter is often a better
solution, as media files tend to be large and keeping multiple copies
of them is wasteful). The higher level directories divide the media collection
appropriately with each lower level being a finer division of its parent
level.

The number of levels in a tree may vary by media type and different
branches in a single tree may have a different number of levels. 
A suitable tree may
already exist (many "CD ripping" programs create one as they work),
or it may have to be created and maintained by hand. Sometimes, this
work maybe at leat partially auomated.

Once such a tree exists and has been "made available" on a machine on
which Media68 has been installed, it can be "navigated" by the
`select68.a68` program. This is essentially a special purpose (and very
limited) "file browser" program. It lets the tree be "navigated" by
presenting lists of sub-directories and/or terminal files at each
level of a tree branch, with an "index number" which can be used to
select the sub-directory or terminal file. Selecting a sub-directory
descends into it. Selecting a terminal file carries out a media type
specific operation on it, which will "play" or "display" the terminal
file appropriately. It "knows" how to "present" `.mp4` files for videos,
`.flac`, `.mp3` and `.wav` files for audio and `.pdf` files for
"printed documents". It can also be told to run an arbitrary shell
script to process a terminal file if the "built in handlers" are not
appropriate.

**The directory tree is effectively a "library" for a type of media.**

For use by `select68.a68`, the tree  must be either on 
local disks or mounted from an SMB or NFS server (or similar).
Video and audio files are "played" using the `mpv` program.
Documents are "presented" with a PDF viewer -- the exact program
is specified with an environment variable, as what is available
varies between Linux desktop environments.

In order to allow "mobile devices" to access these "media libraries",
another program called `files_to_html.a68` exists. This is basically
a static web site generator that converts a "library" tree to a set
of HTML files. These contain HTML 5 that "mimics" the file tree containing 
the "media assets" and provides appropriate "players" for the
terminal files. The resulting web site can be used with a local web 
server (NGINX has been used so far) to allow a web browser on almost any 
modern mobile device to "navigate" and "present" the assets, reproducing
the behaviour of `select68.a68`.

Screen sharing or Bluetooth on the mobile device can be used to present 
the material on large screen displays (e.g. televisions) or listen to it
on high quality audio systems.

The "media types" that are "understood" by `select68.a68` and `files_to_html.a68`
are "videos", "music" and "books". There are Bash shell scripts which run
`select68.a68` with arguments suitable for these "media types". These are
"configured" through environment variables established in the file:
`select_vars.sh` (in the `scripts` sub-directory). This needs to be
"sourced" before the script files are used.

These shell scripts are:

- **Videos**: The `video68.sh` script "navigates" the "media library" tree whose root is
  set by the `VIDEO68_MOUNT` environment variable. It looks for `.mp4` terminal files.
- **Music**:  The `audio68.sh` script "navigates" the "media library" tree whose root is
  set by the `AUDIO68_MOUNT` environment variable. It looks for `.flac`,`.mp3` and `.wav` 
  terminal files.
- **Books**: The `books68.sh` script "navigates" the "media library" tree whose root is
  set by the `BOOKS68_MOUNT` environment variable. It looks for `.pdf` terminal files.
  The program it uses to display these files is set with the `BOOKS68_VIEWER` environment
  variable.
  
Often, the "media library" trees will be stored on a "server" machine on the network and
accessed on other "client" machines on the LAN using a file sharing mechanism. Perhaps the
easiest way to set this up is with SMB (using a `Samba` server on the machine storing the "libraries").

Examples of script files which mount "libraries" from an SMB "server" on a "client" are:

- `mountvideo.sh` which mounts a share `//nuc1/videolib` on `/mnt/videolib`
- `mountaudio.sh` which mounts a share `//nuc1/audiolib` on `/mnt/audiolib`
- `mountbooks.sh` which mounts a share `//nuc1/booklib` on `/mnt/booklib`

Obviously, at least the machine name, user name and SMB server password will need to be
changed for use at other sites.

The `smb.conf` file for `Samba` on the "server" machine will need to be configured to
provide these shares (mapped to wherever the "trees" are actually stored on the "server"
machine).

It is quite possible to use different "server" machines for different libraries. The
`mountaudio.sh` example shows that the "music" library tree is to be found on the machine
with host name "music" (which is a Raspberry Pi 3B running the Moode player software).
The video and books libraries are served by host "nuc1" (an Intel NUC running Debian Linux).

In addition to accessing local "media libraries", there is a further program, `radio68.a68`,
run via the shell script `radio68.sh`, which lets you play Internet radio streams. This uses
the same  style of interface as `select68.a68` to present known radio streams, select one
of them, and play it (again with `mpv`). The streams are defined in `.m3u` files in a directory
assigned to the environment variable `RADIO68_LISTS`. The `radio68.a68` presents a fixed two level
hierarchy -- at the top level, a `.m3u` file is chosen, and the second level allows one
of the streams in that file to be played.

The other obvious type of "media" that could usefully be accessed are photographs.
Unlike the "media" the above programs handle, photographs do not have "titles" which can
be used easily to identify them. A "solution" to that is included here, but I do not
really recommend it. It serves my needs, but must be considered "idiosyncratic" at best.
The organising principle is the time at which the photograph was taken, extracted from
EXIF data for digital images (times must be manually assigned to scanned film images).
Time is divided into years, then months, then weeks of the month. Photos which fall
into these "week buckets" are grouped together for selection.
Browsing photographs can be performed with `photo68.sh`, which works in much the same
way as `video68.sh` and friends. Thumbnails for the photos in a "week bucket" are
presented for selection. This is done with the `nsxiv` image viewing program for
`photo68.sh`. The static web site presentation uses a CSS "light table" to present
a grid of thumbnails for selection.

The facilities provided for photographs are further described in the README in the
`photox` subdirectory if they are of interest. In addition to Algol 68 Genie,
Python 3 is required for the `photox` programs.


## Installation

You must first install (ideally from source) Algol 68 Genie. This can be downloaded
from Marcel van der Veer's website [here](https://algol68genie.nl/en/algol-68-genie).
This superb software can be built from source in under ten minutes, typically. See
the instructions that come with the source code for details of the build process.
Most Linux distributions have a pre-built package available, but they may have quite
old versions.

You may need to mount SMB shares on the "client" machine(s) 
where you want to run `video68.sh`, `audio68.sh` and `books68.sh`. 
This may require installing relevant packages
on your Linux system. For example, `smbclient` and `cifs-utils` are needed for
Debian (and Ubuntu).

You will need to install `mpv` for video and audio replay. This is essential.

If you want to use the static web site generation feature so you can access your media
from mobile devices (or any modern web browser) on your LAN, you will need to install
and configure a web server on some machine on your LAN. The NGINX server has been used
with this software during development, but any properly configured local server should 
work (probably).

Installing `pandoc` is also useful for maintaining a top level index file for all
media types using Markdown. This lets the user start by choosing between the video, 
audio and book media assets.

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

After mounting your "library trees", if necessary, and sourcing the modified
`select_vars.sh` file, you should be ready to use the `video68.sh`, `audio68.sh` 
and `books68.sh`shell scripts to explore your local media collections.

You may want to edit your `~/.bashrc` file to source the modified `select_vars.sh` file
whenever you start a new desktop terminal.

If mobile devices are to be served, a local web server must be installed and
configured somewhere on the LAN. The output of the static web site generator,
`files_to_html.a68`. must be copied to the default directory served up by this
server. More details on this (for the NGINX server) are given below.


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
in the order they were meant to be played in the album. Responding with the option `p`
instead of an index number will play *all* the audio files in the directory, in the
order they are presented. It is possible to start at an arbitrary "track" using `p<n>`
where `<n>` is a decimal digit (e.g. `p3` will start at "track" 3).

Other allowed entries are `u` to ascend one level and `q` to exit immediately.

When `mpv` is playing an item, `q` will stop the play back and return to the current
level's menu.

And that's it! A very bare bones approach to accessing media libraries ...

The static web site generator essentially makes this scheme work on mobile devices
through a web browser. It uses the same file trees as the `select68.a68` based
scripts use, transforming them into HTML files containing links to "terminal files"
or other HTML pages that present the next lower level directory names. Clicking
through these links navigates the file tree (or, rather, a "mimic" of the file tree)
in the same way as selecting list
index numbers does. The media assets are ultimately "played" by an appropriate
HTML 5 "player".

Accessing the "libraries" on a mobile device can be done with any web browser.
Start by entering the URL for the local web server. E.g.:
```
http://myserver.mynetwork.net/index.html
```
(with obvious modifications as needed for your site).


## Building the libraries

All "local media servers" have the problem of compiling and organising the
"assets" to be served. This is probably the most labour intensive and time
consuming aspect of this type of project. It took me over 2.5 years of occasional
spare time work to digitise our quite modest (~300) CD collection! You could do
it a lot faster if you worked on it "full time", of course, but that's only likely
to be possible after retirement! (And it would become quite tedious quite quickly,
I think, as a full time job). Video assets from DVD and BluRay are even worse,
in my opinion (I never found a really reliable "video ripping" program and often resorted
to HDMI capture ... you may have better luck). There may be some "time
pressure" to digitise optical media sooner rather than later, though, as it seems
optical disk drives are no longer being manufactured (at least, not by the
traditional "big" manufacturers)!

For use with the Media68 programs, you must create a directory tree, dividing
up the assets in a way that makes sense for their type. The divisions I use
for the types are:

- **Video**: 
    - Top level: `movies`, `tv`, `music`, `other`
    - movies: `b-movies`, `british`, ... `scifi` (terminal `.mp4` files are in these directories).
    - tv: `<series name>` e.g. `The_Human_Jungle` with lower levels of `Disk_n` then `Episode`s.
- **Music**:
    - Top level: `<artist name or composer name>`
    - `<artist name>`: `<album name or work>` (usually terminal `.flac`, `.mp3` 
    or `.wav` files are in these directories)
- **Books**:
    - Top level: `Factual`, `Fiction` (major categories).
    - `<major category>`: `<author name>`
    - `<author name>`: Terminal `.pdf` files for each book, typically.
    
There are no hard rules for how to divide up the media assets, though.

Some "ripping" programs may produce a suitable tree automatically. I found
this was largely the case for the CD "rippers" I used.

On the other hand, the video assets were mostly just a lot of `.mp4` files
dumped in a single directory. The only way to deal with these seemed to be
to write a shell script by hand to make a tree with symbolic links to
the assets. Here is a small part of such a script:
```
#!/bin/bash
#
# Given a lot of videos files with mysterious names in a single level
# (or two level) tree, create a tree of symbolic links which orgaanises them
# into categories and gives them meaningful names.
#
SOURCE=/massbackup/contents/videos
LISTS=/massbackup/contents/videolib
LINK="ln -s -f"
#
# Ensure lists root exists.
mkdir -p ${LISTS}
#
# Remove top level category trees.
rm -rf ${LISTS}/movies
rm -rf ${LISTS}/tv
rm -rf ${LISTS}/music
rm -rf ${LISTS}/other
#
# Create category directories.
mkdir -p ${LISTS}/movies
mkdir -p ${LISTS}/tv
mkdir -p ${LISTS}/music
mkdir -p ${LISTS}/other
mkdir -p ${LISTS}/movies/hammer
mkdir -p ${LISTS}/movies/horror
mkdir -p ${LISTS}/movies/scifi
mkdir -p ${LISTS}/movies/b-movies
mkdir -p ${LISTS}/movies/hollywood
mkdir -p ${LISTS}/movies/independent
mkdir -p ${LISTS}/movies/british
mkdir -p ${LISTS}/movies/foreign-language
#
# Begin creating links.
${LINK} ${SOURCE}/2001_comp.mp4 ${LISTS}/movies/scifi/2001_A_Space_Odyssey.mp4
#
${LINK} ${SOURCE}/aap_experimental_tape_1989_comp.mp4 ${LISTS}/other/Array_Productions_1989.mp4
#
${LINK} ${SOURCE}/abominable_comp.mp4 ${LISTS}/movies/hammer/Abominable_Snowman.mp4
#
mkdir -p ${LISTS}/tv/Partners_In_Crime
${LINK} ${SOURCE}/ac-partners-d1_comp.mp4 ${LISTS}/tv/Partners_In_Crime/Disk1.mp4
${LINK} ${SOURCE}/ac-partners-d2_comp.mp4 ${LISTS}/tv/Partners_In_Crime/Disk2.mp4
${LINK} ${SOURCE}/ac-partners-d3_comp.mp4 ${LISTS}/tv/Partners_In_Crime/Disk3.mp4
...
```
Perhaps there are other approaches to this which could partially automate the process,
but I couldn't think of any.

In the same way, the "books" tree was constructed by hand. Automating that
(at least partially) is probably feasible, though.

Once the library trees have been created, the static web site generator program
(`files_to_html.a68`) can create an equivalent of them which can be accessed
on mobile devices (or any modern web browser).

There are example script files which regenerate the static web sites for
each class of media: `rebuild_audio_site.sh`, `rebuild_book_site.sh` and 
`rebuild_video_site.sh`. These put their output in `audio_site`, `book_site`
and `video_site` respectively. To update the web site, the contents of those
directories simply need to be copied to the directory served by the web server.
For example, with the NGINX web server running on the same machine the `_site`
directories are created on:
```
cd audio_site; sudo cp * /var/www/html/; cd ..
```
There is also an example top level index file for all types of media
collections in `index.md`. This can be converted to HTML using:
```
pandoc index.md -o index.html
```
then the HTML can be "uploaded" to the web server. All the collections can
be accessed through this index file.

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


## SMB server configuration conssiderations

The machine that holds the library trees on its local disks will often need
to run an SMB server (Samba) so that other machines on the LAN can access the
libraries.

The only "unusual" consideration that is likely to apply here is that symbolic
links must be allowed. There are two parts to this, which must be addressed in
the Samba configuration file (`/etc/samba/smb.conf`).

- In the "authentication" section, ensure this line is present:
  ```
     allow insecure wide links = yes
  ```
- In each share definition, ensure these lines are present:
  ```
    follow symlinks = yes
    wide links = yes
  ```
  
Here is an example of a complete share definition:
```
[videolib]
  comment = Movie and video library.
  path = /massbackup/contents/videolib
  available = yes
  read only = no
  browsable = yes
  public = yes
  writeable = yes
  follow symlinks = yes
  wide links = yes
```

You will need to restart the SMB service after chaning `smb.conf`. E.g:
```
sudo systemctl restart smbd nmbd
```
  
Most problems with SMB shares (i.e. inaccessible files) are due to permissions problems.
All elements of a path must have the "correct" permissions and the *targets* of symbolic
links must also have the "correct" permissions. When the symbolic links appear to have the
right permissions but the target files do not, things can get very confusing.


## Webserver configuration considerations

The NGINX web server has been used in the development of this project, so the
details shown are relevant to that, but similar issues will need to be addressed
with other servers, probably.

The main configuration file for NGINX is `/etc/nginx/nginx.conf` and this can be
left as shipped. The "default site" configuration file 
is `/etc/nginx/sites-available/default`
and this will almost certainly need to be modified.

The problem is that terminal files tend to be large and the library 
file tree may be on a remote machine ((i.e. not the machine running the
web server), and mounted by SMB or NFS. This poses a problem for web servers,
which, by default, only serve files from their own HTML tree
(e.g. `/var/www/html/...`) for "security" reasons. For example, an SMB share on another machine
on the LAN may be mounted at `/mnt/videolib`. The static web site generator
(run on this library tree) will need to have links to terminal files on the remote 
machine. To make this work, the terminal files must be referenced
with a root explicitly declared to the web server as an *alias*.

As an example, we will alias `/mnt/videolib/...` to `/external-files/...`
The terminal file names must have their
true roots (here `/mnt/videolib`) replaced by `/external-files` in all the generated
HTML, and this is done by the static web site generator program. 

The `/etc/nginx/sites-available/default` must be edited to define this alias for the 
NGINX web server:

```
	root /var/www/html;

	location /external-files/ {
		 alias /mnt/videolib/;
	}
```

Similar procedures must be used for each library tree to be served up by the web server.
The example web site rebuild scripts (`rebuild_video_site.sh`, etc.) show how
this can be done.

You will need to restart NGINX (etc.) after making configuration changes. E.g.:
```
sudo systemctl restart nginx
```
