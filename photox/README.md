#  Media68 and PhotoX - Additions to access still photographs

Before continuing, you might want to look at `Immich` or something similar ...
I have never used it, but it might be a better solution for you!

The "Media68 approach" to accessing media assets is not as good
a fit for photographs as it is for books, music and videos because
photographs have no textual titles by which they can be referred.

Without using a "full database approach", there needs to be a single
organising principle that can be applied to "order" the assets and
assign what amounts to a textual title to each of them.

The only feasible approach is to use the time the photograph was
taken to refer to it. Fortunately, the EXIF data contained in
almost all digital photographs makes this possible. When scanned film
images are involved, a "time" must be assigned manually to each of them.

There are multiple stages in the process of moving photographs from a
digital camera or smart phone (more usually the latter these days) to
a form that can be accessed by Media68.

The process relies on software I wrote in Python, originally in 2014
as a learning exercise. This grew and was moved to Python 3 in 2019.
It should work with any newish Python 3 version (3.12 certainly works).
This software is known as PhotoX.

The overall scheme is:

- Copy images from the camera or mobile device to a directory on the
  computer being used to process data for Media68.
- Add the new images to a PhotoX database (or create a new one).
- Convert the PhotoX database to a link tree. This can be used by Select68
  to view images on computers where this link tree is mounted (typically
  it will be shared by SMB).
- Convert the link tree to a static web site and serve it to the LAN
  with a web server such as NGINX.
  
Alternatively, check out `Immich` ...


## Copy the images to a directory on the machine running Media68/PhotoX

This is usually trivial with a "real" digital camera, as they mostly implement
PTP (Picture Transfer Protocol) or can appear as a standard "disk" device when
attached to a computer via USB. No special device drivers or camera manufacturer
supplied proprietary software is needed. I believe Android based smart phones also
support PTP or a more flexible similar thing called MTP (Media Transfer Protocol).

Apple devices need specific software to be installed for images to be accessed
from Linux, however. These are needed to communicate with Apple File Conduit (AFC) 
on the Apple device. For Debian Linux, you need to install the following:
```
sudo apt install libimobiledevice-utils ifuse
```

These will allow you to mount the mobile device as a file system (which exposes
a limited view of the device's file system, including the photographs taken
with the device's cameras).

Next, create a mount point directory for the device. For example:
```
mkdir ~/iphone
chmod 777 ~/iphone
```

Attach the device to the computer with a USB cable. Then tell the device
to "trust this computer" by responding to the popup that will be displayed
on the device when the USB cable is attached.

Next, mount the device on the computer:
```
ifuse ~/iphone
```

The camera images will then be available in `~/iphone/DCIM/100APPLE/` etc.
The file formats will be `.HEIC` and `.JPG`. Recent iOS versions store camera
images as `.HEIC` by default. This may be useful, as other applications may store "receipts"
as images in `.JPG`. You generally do not want to transfer these "receipt" images.

Then create an "image source directory" on the computer and copy the camera images
into it:
```
mkdir ~/source_images
cd ~/source_images
cp `~/iphone/DCIM/100APPLE/*.HEIC .
```

Next, convert the `.HEIC` images to `.JPG` using ImageMagick. Use:
```
magick mogrify -format jpg -quality 92 *.HEIC
```
If using the older ImageMagick 6 version, omit the`magick` part of the command.
You may want to examine the new images using operating system tools and discard
ones you don't want at this stage.

## Add new images to PhotoX database

A PhotoX database consists of a directory containing a Python Pickle file and
and three (or more) subdirectories. The Pickle file contains information on
each of the images in the database. The subdirectories are:

- `photos`: This contains the full resolution images in `.JPG` format.
- `thumbnails`: This contains thumbnail versions with a width of 300 pixels in `.JPG` format.
- `raws`: This contains the RAW versions of the `photos` images, where they exist, in whatever format
  the original camera uses.

PhotoX cannot work with RAW images only. It can handle JPEG+RAW though. These subdirectories are created by the software
as needed.

As the PhotoX programs use Python, it is necessary to activate the Python Virtual Environment (venv) created on
installation before they can be used:
```
source ~/photoxenv/bin/activate
```
See the installation instructions below to see where `photoxenv` comes from.

To "import" all the images in a source images directory, the `photohack` program can be used. A single command will
create a database Pickle file if it doesn't exist and the relevant subdirectories (there will be no RAW files from
the process described above, though). Create a directory for the new database and "import" the new source images into it as
follows:
```
mkdir masterphdb
cd masterphdb
python .../media68/photox/photohack.py -v all ~/source_images
```
where `...` indicates where you cloned `media68` to. A message will be printed as each image is added. 

Once a database exists, its contents can be explored using the `PhotoX` program. This is a GUI program (based on Qt and OpenGL)
that shows the position of every image on a 2D "time plane". Clicking on this "time plane" will display the nearest (in time) image 
in a thumbnail and information window. Using the `V` hotkey moves to a full resolution display of the image. This full resolution
display can be zoomed (with the mouse wheel or by selecting a zoom box with the right mouse button) and panned (with the middle
mouse button). The next image can be chosen with the `N` hotkey and the previous with `P`. There are many more capabilities, but
these will not be described here. To run `PhotoX`, use:
```
python .../media68/photox/photox.py
```

## Convert the PhotoX database to a link tree for Media68 programs to use

```
a68g photox_to_tree.a68 -- -r .../masterphdb/photos -o photolib
```

This creates another set of thumbnails (!) as well as symbolic links to terminal full resolution 
image files in the PhotoX database.
The new thumbnails are 200 pixels wide, which seems to work better in CSS "light tables" created
by the static web site generator for photograph data. Unfortunately, generating the thumbnails
(with ImageMagick, currently) can take significant time.

The contents of `photolib` can then be shared via SMB for use on other machines on the LAN using
the `photo68.sh` script (see below).

## Convert the link tree to a static web site.

This can be done with the `scripts/rebuild_photo_site.sh` script. Internally, this uses `files_to_html.a68`.
This script as supplied creates the web site in a directory called `photo_site`. The contents of this can be
"uploaded" (or copied) to a local web server, as described in the main project `README`.

## Installing the PhotoX programs

Because these are written in Python, it is best to create a Python Virtual Environment specifically
for them. This avoids the packages installed for them interfering with other Python programs you may
use (and ensures the right versions of the things PhotoX needs are available).

```
cd ~
python3 -m venv photoxenv
source ~/photoxenv/bin/activate
cd .../media68/photox
pip install -r requirements.txt
```

You must activate this environment before attempting to use the PhotoX programs in future.
```
source ~/photoxenv/bin/activate
```
