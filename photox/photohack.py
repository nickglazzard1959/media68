#!/usr/bin/env python
"""
photohack.py
============

Assist organizing random dumps of photographs, which probably include many
duplicates, in to something like a coherent, usable, "database". This file
implements basic "database" functions.

If run as a program, it can create, add to and/or summarize a "database"
from the command line.

The primary organizing principles are time (at which the photo was taken, from
Exif if it is present) and image file "signature", which is a number unique to
each image file.

Description
-----------

Images are characterized by a hash of the image file. This is stored along with
a certain amount of metadata (using Exif if present) as an image description.
If present, geolocation data in the Exif is extracted.
Duplicate images should have the same file hash, allowing them to be eliminated.

An image database is a file containing the set of unique hashes and the image metadata
found by examining every image in an input directory tree.

Once a database has been created, the original images in the input directory tree are
processed in to a set of unique thumbnails and corresponding unique full resolution
image files. These files are given unique time and hash based file names, which can be
generated directly from the metadata for each image in the database.

It is assumed that all processing takes place in a "home" directory (the current
directory). After processing, the "home" directory should contain this:

<"home"> ---+--- thumbnails (single directory containing all unique thumbnails)
            |
            +--- photos (single directory containing all unique full res JPEG images)
            |
            +--- raws (single directory containing all unique full res RAW images)
            |
            +--- <database_name>.photodb (the image database)
            |
            +--- saved (selected saved JPEG images)
            |
            +--- saved_raws (selected saved RAW files)
            |
            +--- <original image input tree 1> ---+--- ... NOTE: These could be anywhere
            |                                                    not just in <"home">
            +--- <original image input tree 2> ---+--- ...
            |
          (etc.)

Once they have been added to a database and the thumbnails and full res image copies
have been created, the original images in the input trees are no longer required. The
database file contains the name of the last input tree processed, but this is of no
importance.

NOTE: Although you can have multiple <database_name>.photodb files in a single "home"
      directory, photos and thumbnails are shared between *all* the .photodb files!
      Different database files can present different subsets of the images, but are
      probably not useful in practice. A single database file should be used.
      Since the purpose of this is really to build up a single, unique, collection
      of photographs, this is pretty much what is required. I think. Different
      collections, which are not intended to be merged, should be kept in separate
      "home" directories. Command line programs using this stuff should use any leading
      directory part of a database file name to determine the "home" directory and chdir()
      to that. A database is really the contents of a "home" directory.

.photodb file information:
--------------------------
These are pickle files containing:

* dirname : name of last image source directory processed. 
* hashes : list of all image file hashes.
* infotable : list of per photo information, one entry per photo.
   * infotable entry : dictionary, with the following keys: 
        info['filename'] : file name
        info['hashval'] : SHA1 hash of file contents
        info['tags'] : list of tag strings
        info['comment'] : JPEG comment string extracted from JPEG file
        info['bytes'] : file size in bytes
        info['date'] : date taken from EXIF (if possible)
        info['systime'] : Unix time version of date
        info['orient'] : orientation code
        info['width'] : width in pixels when displayed (accounts for orientation)
        info['height'] : height in pixels when displayed (accounts for orientation)
        info['maker'] : camera manufacturer name
        info['model'] : camera model name
        info['geotags'] : has where taken location information (True/False)
        info['lat'] : latitude of location (0 if unknown)
        info['long'] : longitude of location (0 if none)
        info['alt'] : altitude of location (0 if none)
        info['exif'] : has at least the basic EXIF data (True/False)
        -- Items which may or may not be present:
        info['rawfilename'] : associated raw file name. Not present if no RAW file exists.
        info['processor'] : last software that processed this image. Not present if camera original.
        info['whenprocessed'] : Unix time when processed version of image was created.
        -- Transient data used in photox program:
           * Note: this *is* stored in the DB file, so images can be selected in a GUI
             then processed by a script to do unusual things.
        info['hide'] : show/hide status
        info['selected'] : selection status
* deletedtable : list of photos that are not to be shown. Items are infotable entries
                 moved from the infotable list.

Nick Glazzard. February & April 2014, March 2015, November 2019.
----------------------------------------------------------------
"""

import os, shutil, argparse, fnmatch
import hashlib, time, pickle, string, sys

try:
    from PIL import Image
except:
    print("ERROR: photohack needs Python Imaging Library (Pillow).")
    sys.exit(9)

KSHOW = 0
KHIDE = 1
KUNHIDDEN = 2

def _bytestostr( ccharpin ):
    """
    Convert an array of 8 bit bytes, such as may be returned from C code
    using c_char_p arguments, to a string.
    """
    if ccharpin is None:
        return None
    else:
        return ccharpin.decode('utf-8')

def _bytestostr_ifnot( ccharpin ):
    """
    If ccharpin is NOT already a (wide) string, make it so.
    """
    if type(ccharpin) is str:
        return ccharpin
    else:
        return _bytestostr(ccharpin)

######################
# File manipulations #
######################

def all_files( root, patterns='*', single_level=False, yield_folders=False ):
    """
    Find all files matching pattern, starting at root.
    """
    patterns = patterns.split( ';' )
    for path, subdirs, files in os.walk( root ):
        if yield_folders:
            files.extend( subdirs )
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch( name, pattern ):
                    yield os.path.join( path, name )
                    break
        if single_level:
            break

def delete_file_if_exists( path ):
    """
    Delete a file if it exists.
    """
    if os.access( path, os.F_OK ):
        try:
            os.remove( path )
            return True
        except:
            print('ERROR: Cannot remove %s' % path)
            return False
    else:
        return True

def create_folder_if_not_exists( path ):
    """
    Create a folder if it does not exist.
    """
    if not os.access( path, os.F_OK ):
        try:
            os.mkdir( path )
            return True
        except:
            print('ERROR: Cannot create folder %s' % path)
            return False
    else:
        return True

def sha1_file(filepath):
    """
    Return the SHA1 hash of filepath.
    """
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

####################
# Time conversions #
####################

def exif_to_time(ts):
    """
    Convert Exif date ('2005:10:20 23:22:28') to Unix time.
    Unix time is defined to be UTC. This takes Exif date, taken to be ** a local time value **
    and converts it to UTC Unix time.
    """
    tpl = time.strptime(ts, '%Y:%m:%d %H:%M:%S') # No time zone: does not modify time. Result is local time.
    return time.mktime(tpl) # Modifies time from local time to UTC.

def time_to_exif(fdt):
    """
    Convert Unix time to Exif string datetime. Used for image files with no Exif and for explicit time changes.
    The Unix time here often comes from file status st_mtime, which is defined to be in UTC. 
    Return ** a local time value **.  
    It is debateable whether this is best or not, but since we lack timezone data in many cases,
    it isn't clear what to do. At least: time_to_exif( exif_to_time(ts) ) == ts using this.
    """
    return time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(fdt))

def exif_to_time_tuple(ts):
    """
    Convert Exif date to (year, month, day, hour, min, sec) tuple (numbers).
    """
    tpl = time.strptime(ts, '%Y:%m:%d %H:%M:%S')
    return( tpl[0], tpl[1], tpl[2], tpl[3], tpl[4], tpl[5])

def time_tuple_to_time(tpl):
    """
    Convert a (year, month, day, hour, min, sec) tuple to Unix time.
    The tuple is taken to be ** a local time value **.
    """
    fulltpl = (tpl[0], tpl[1], tpl[2], tpl[3], tpl[4], tpl[5], 0, 1, -1)
    return time.mktime(fulltpl) # Modifies time from local time to UTC.

def time_tuple_to_exif(tpl):
    """
    Convert a (year, month, day, hour, min, sec) tuple to an Exif string datetime.
    """
    return time_to_exif(time_tuple_to_time(tpl))


#######################
# Metadata extraction #
#######################

def get_jpeg_comment(picname):
    """
    Try getting a JFIF comment field out of the first 2K or so of the file.
    It seems that just about anything can be (and is) put in the comment field. We
    only want human readable text comments.
    """
    comment = ''
    blocksize = 2048 # Bytes at the file start to check through.
    maxtextlength = 512 # Comment sizes bigger than this are unlikely to be text?
    try:
        fin = open(picname, 'rb')
        block = fin.read(blocksize)
        # Look for the start of a comment block (which will be at least 5 bytes long).
        for i in range(0,len(block)-5):
            v = ord(block[i])
            if v == 255:
                if ord(block[i+1]) == 254:
                    # Yes: block[i] is the start of a comment field. Get the size of it.
                    size = 256 * ord(block[i+2]) + ord(block[i+3])
                    # If it looks too big, ignore it.
                    if size < maxtextlength:
                        for j in range(0,size-2):
                            k = j + i + 4
                            if k > (blocksize-1):
                                break
                            newchar = chr(ord(block[k]))
                            # If the first character is not printable, skip the whole thing.
                            if (j == 0) and not (newchar in string.printable):
                                break
                            comment += newchar
                    fin.close()
                    # Strip out all non printable characters.
                    comment = _list_to_string([x for x in comment if x in string.printable])
                    return comment
        fin.close()
        return comment
    except:
        return comment

def _list_to_string(charlist):
    ret = ''
    for c in charlist:
        ret += c
    return ret

def get_photo_info(picname,doingprocessed=False):
    """
    Get a minimum amount of vital information about a photograph.
    Try to use Exif data. If that fails use image and filesystem data.
    Always characterize the file with a hash. The information is stored
    in a dictionary.
    """
    info = {}
    try:
        # Open the image file.
        filedata = os.stat(picname)
        #print filedata
        img = Image.open(picname)
        info['filename'] = picname
        info['hashval'] = sha1_file(picname) # Hash
        info['tags'] = []
        info['comment'] = get_jpeg_comment(picname) # Comment field. If any ...
        info['bytes'] = filedata.st_size
        info['hide'] = KSHOW
        info['selected'] = False

        # See if there is an associated RAW file. Do this just by looking at file names.
        known_raw_extensions = ['.dng','.DNG',  # Adobe Digital NeGative. Commonly used for smartphone RAWs.
                                '.raf','.RAF',  # Fujifilm
                                '.nef','.NEF',  # Nikon
                                '.cr2','.CR2',  # Canon
                                '.arw','.ARW',  # Sony
                                '.dpx','.DPX'   # Home made film scanner (density data)
                                ]
        picname_stem,picname_ext = os.path.splitext(picname)
        for rawext in known_raw_extensions:
            raw_name_maybe = picname_stem + rawext
            if os.path.exists(raw_name_maybe):
                info['rawfilename'] = raw_name_maybe
                break

        # Find and parse Exif data if at all possible.
        try:
            # Get generally present Exif data.
            # We want (need) a certain set of data. If any part of that isn't there, treat it
            # as if none of it was there (no Exif case).
            # ALTHOUGH: we now do try to deal with bits of this being missing.
            exif_data = img._getexif()
            info['date'] = exif_data[36867].strip() # Original date
            info['systime'] = exif_to_time(info['date']) # Unix time version of date
            try:
                info['orient'] = exif_data[274] # Orientation: E.g. 1=usual horizontal, 6=usual vertical.
            except:
                info['orient'] = 1
            try:
                num_pixels = exif_data[40962]  # Pixels
                num_lines = exif_data[40963] # Lines
            except:
                num_pixels = 0
                num_lines = 0
            # Well, Apple iPhones report these as 0. Why? Use the image data instead.
            if (num_pixels == 0) or (num_lines == 0):
                num_pixels = img.size[0]
                num_lines = img.size[1]
            # Account for orientation.
            if info['orient'] > 4: # Vertical orientations.
                info['height'] = num_pixels
                info['width'] = num_lines
            else:  # Horizontal orientations.
                info['width'] = num_pixels
                info['height'] = num_lines
            try:
                info['maker'] = _list_to_string([x for x in exif_data[271].strip() if x in string.printable])  # Make of camera
                info['model'] = _list_to_string([x for x in exif_data[272].strip() if x in string.printable])  # Model
            except Exception as e:
                #print('EXIF get maker/model exception. Reason:',e)
                info['maker'] = 'unknown'
                info['model'] = 'unknown'
            try:
                # Get location data, if it is present. It usually isn't.
                # If not, that is OK - use the Exif data we have got and don't worry.
                gpsdir = exif_data[34853] # GPS (geolocation) data directory (array).
                #print gpsdir
                # It seems it exists. Decode it to latitude, longitude (degrees) and altitude (metres).
                lat_sign = 1
                if gpsdir[1] != 'N': # Convention is North is positive, South negative.
                    lat_sign = -1
                secs_north = gpsdir[2][2][0] / float(gpsdir[2][2][1])
                mins_north = gpsdir[2][1][0] / float(gpsdir[2][1][1])
                degs_north = gpsdir[2][0][0] / float(gpsdir[2][0][1])
                long_sign = -1
                if gpsdir[3] != 'W': # Convention is East is positive, West negative.
                    long_sign = 1
                secs_west = gpsdir[4][2][0] / float(gpsdir[4][2][1])
                mins_west = gpsdir[4][1][0] / float(gpsdir[4][1][1])
                degs_west = gpsdir[4][0][0] / float(gpsdir[4][0][1])
                alt_sign = 1
                if gpsdir[5] == 1: # Below sea level if 1. Convert to negative altitude.
                    alt_sign = -1
                alt_sea = gpsdir[6][0] / float(gpsdir[6][1])
                info['lat'] = lat_sign * (degs_north + mins_north/60.0 + secs_north/3600.0)
                info['long'] = long_sign * (degs_west + mins_west/60.0 + secs_west/3600.0)
                info['alt'] = alt_sign * alt_sea
                info['geotags'] = True
            except Exception as e:
                # No GPS data found. Or something horrible happened.
                #print('EXIF location parse exception. Reason:',e)
                info['geotags'] = False
                info['lat'] = 0.0
                info['long'] = 0.0
                info['alt'] = 0.0
            # If this is a supposedly processed file, get the name of the software that processed it.
            if doingprocessed:
                try:
                    info['processor'] = exif_data[305].strip()
                    processed_tag = "".join(info['processor'].split())
                    info['tags'].append(processed_tag)
                except:
                    info['processor'] = 'unknown'
                info['tags'].append('processed')    
                info['whenprocessed'] = filedata.st_mtime
            # We got at least the basic Exif data.
            info['exif'] = True
            
        except Exception as e:
            # No Exif data. Or something unexpected about it. Try using the file data.
            # This often means the image is not a camera original.
            #print('EXIF general parse exception. Reason:',e)
            info['systime'] = filedata.st_mtime
            # Due to Linux not actually keeping a creation time (yeah - it is more complicated
            # than that, but for all practical purposes, it doesn't) 'date' may well be useless.
            # This is *very bad news* in this application.
            info['date'] = time_to_exif(info['systime'])
            info['width'] = img.size[0]
            info['height'] = img.size[1]
            info['orient'] = 1
            info['maker'] = 'unknown'
            info['model'] = 'unknown'
            info['geotags'] = False
            info['lat'] = 0.0
            info['long'] = 0.0
            info['alt'] = 0.0
            info['exif'] = False
            
    except:
        # Could not open the image file.
        # All data is invalid apart from the filename (set to 'ERROR').
        info['filename'] = 'ERROR'
    return info

def get_creation_date(picname):
    """
    Try to get just the creation date out of the EXIF for a picture.
    This isn't normally used, but it can be useful for special fix up programs.
    """
    try:
        img = Image.open(picname)
        exif_data = img._getexif()
        date_string = exif_data[36867].strip() # Original date
        unixtime = exif_to_time(date_string) # Unix time version of date
        return (unixtime, date_string)
    except Exception as e:
        print('ERROR: get_creation_date() failed. Error was:',e)
        return (0,' ')

def get_any_exif_tag(picname,tagnumber,verbose=False):
    """
    Get the value of an arbitrary tag number.
    Caller must deal with the data type returned appropriately.
    Return None if that tag is not present or for any other problem.
    """
    try:
        img = Image.open(picname)
        exif_data = img._getexif()
        item = exif_data[tagnumber]
        return item
    except Exception as e:
        if verbose:
            print('ERROR: get_any_exif_tag() failed. Error was:',e)
        return None

#######################
# Database generation #
#######################

def add_photos(dirname, infotable, hashes, verbose=False, callback=None, taglist=None,
               maker=None, model=None, doingprocessed=False, unixtime=None):
    """
    Look at all JPEG files starting at dirname and add information for
    each one that is not already known to infotable. "Already known" means
    its hash is in hashes. As each image is added to infotable, update
    hashes.
    """
    errors = 0
    added = 0
    numproc = 0
    hwm = len(infotable)
    if verbose:
        print('add_photos(): dirname=',dirname)
    for imagename in all_files(dirname, '*.jpg;*.JPG'):
        numproc += 1
        if verbose:
            print('... Input image:',imagename)
        else:
            if (numproc%20) == 0 and (callback == None):
                print('... Processed:',numproc,'input images so far.')
        info = get_photo_info(imagename, doingprocessed)
        if info['filename'] == 'ERROR':
            print('WARNING: Did not understand:',imagename)
            errors += 1
        else:
            if taglist is not None:
                for newtag in taglist:
                    if not newtag in info['tags']:
                        info['tags'].append( newtag.strip() )
            if (maker is not None) and (model is not None):
                info['maker'] = maker.strip()
                info['model'] = model.strip()
            if unixtime is not None:
                info['systime'] = unixtime
                info['date'] = time_to_exif(info['systime'])
            if not (info['hashval'] in hashes):
                hashes.append(info['hashval'])
                infotable.append(info)
                added += 1
        if callback != None:
            callback(numproc)
    return errors, added, hwm

def save_photo_data(outname, dirname, infotable, hashes, deletedtable):
    """
    Save the accumulated photo data.
    """
    try:
        fout = open(outname,'wb')
        pickle.dump(dirname,fout,2)
        pickle.dump(infotable,fout,2)
        pickle.dump(hashes,fout,2)
        pickle.dump(deletedtable,fout,2)
        fout.close()
        return True
    except:
        print('ERROR: Failed to save photo data to:',outname)
        return False

def load_photo_data(inname):
    """
    Load saved photo data.
    """
    try:
        fin = open(inname,'rb')
        dirname = pickle.load(fin)
        infotable = pickle.load(fin)
        hashes = pickle.load(fin)
        try:
            deletedtable = pickle.load(fin)
        except:
            deletedtable = []
        fin.close()
        return (dirname, infotable, hashes, deletedtable)
    except:
        print('ERROR: Failed to load photo data from:',inname)
        return ('ERROR',[],[],[])

def make_time_file_name(info,prefix,intime=None,inext=None,usehashdigits=12):
    """
    Return a filename, based on the date/time field of info.
    Add prefix character: P for full photos, T for thumbnails, R for raw files.
    NOTE: This function is CRITICALLY IMPORTANT. All image data stored in the database
    uses the names created by this function using info['systime'] or intime. The original
    image filenames are irrelevant after they have been added, even though they are stored 
    in info['filename'].
    """
    if intime == None:
        basename = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime(info['systime']))
    else:
        basename = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime(intime))
    if inext is not None:
        filename = '{0}_{1}_{2}{3}'.format(prefix,basename,info['hashval'][0:usehashdigits],inext)
    else:
        filename = '{0}_{1}_{2}.jpg'.format(prefix,basename,info['hashval'][0:usehashdigits])
    return filename

def generate_thumbnail(sourcename, thumbname, width):
    """
    Read image sourcename and write image thumbname, width pixels wide.
    """
    try:
        inimg = Image.open(sourcename)
        twidth = width
        theight = int( float(inimg.size[1])/float(inimg.size[0]) * width )
        thumb = inimg.resize((twidth,theight),Image.Resampling.LANCZOS)
        thumb.save(thumbname)
        return True
    except Exception as e:
        print('ERROR: Failed to create thumbnail:',thumbname)
        print('... Reason:', e)
        return False

def create_thumbnails(infotable, thumbsdir, verbose=False, callback=None, userarg=None, hwm=0):
    """
    Create thumbnails for all known images in thumbsdir - but only if
    they do not already exist.
    """
    errors = 0
    newthumbs = 0
    numproc = 0
    if not create_folder_if_not_exists( thumbsdir ):
        return -1
    for i in range(hwm,len(infotable)):
        entry = infotable[i]
        thumbname = make_time_file_name(entry,'T')
        thumbpath = os.path.join(thumbsdir,thumbname)
        if not os.access( thumbpath, os.F_OK ):
            if verbose:
                print('... Created:',thumbpath)
            if not generate_thumbnail(entry['filename'],thumbpath,300):
                errors += 1
            else:
                newthumbs += 1
        else:
            if verbose:
                print('... Skipped:',thumbpath)
        numproc += 1
        if (not verbose) and ( (numproc%20) == 0 ) and (callback == None):
             print('... Processed:',numproc,'thumbnails so far.')
        if callback != None:
            callback(numproc,userarg)
    return errors, newthumbs

def copy_photo(sourcename, photoname):
    """
    Copy photo sourcename to photoname.
    """
    try:
        shutil.copy2(sourcename,photoname)
        return True
    except:
        print('ERROR: Failed to copy to:',photoname)
        return False

def create_images(infotable, photosdir, verbose=False, callback=None, userarg=None, hwm=0):
    """
    Copy all known images to photosdir with time based names - but only if
    they do not already exist.
    """
    errors = 0
    newimages = 0
    numproc = 0
    if not create_folder_if_not_exists( photosdir ):
        return -1
    for i in range(hwm,len(infotable)):
        entry = infotable[i]
        photoname = make_time_file_name(entry,'P')
        photopath = os.path.join(photosdir,photoname)
        if not os.access( photopath, os.F_OK ):
            if verbose:
                print('... Created:',photopath)
            if not copy_photo(entry['filename'],photopath):
                errors += 1
            else:
                newimages += 1
        else:
            if verbose:
                print('... Skipped:',photopath)
        numproc += 1
        if (not verbose) and ( (numproc%20) == 0 ) and (callback == None):
             print('... Processed:',numproc,'full images so far.')
        if callback != None:
            callback(numproc,userarg)
    return errors, newimages

def construct_raw_file_path(entry,rawsdir='raws'):
    """
    Make a raw file name with the appropriate extension.
    """
    original_raw_name = entry['rawfilename']
    original_raw_name_stem,original_raw_name_ext = os.path.splitext(original_raw_name)
    rawname = make_time_file_name(entry,'R',inext=original_raw_name_ext)
    rawpath = os.path.join(rawsdir,rawname)
    return (rawname, rawpath)

def create_raws(infotable, rawsdir, verbose=False, callback=None, userarg=None, hwm=0):
    """
    Copy all known RAW images to rawsdir with time based names - but only if
    they do not already exist.
    """
    errors = 0
    newimages = 0
    numproc = 0
    if not create_folder_if_not_exists( rawsdir ):
        return -1
    for i in range(hwm,len(infotable)):
        entry = infotable[i]
        if 'rawfilename' in entry:
            rawname, rawpath = construct_raw_file_path(entry, rawsdir)
            if not os.access( rawpath, os.F_OK ):
                if verbose:
                    print('... Created:',rawpath)
                if not copy_photo(entry['rawfilename'],rawpath):
                    errors += 1
                else:
                    newimages += 1
            else:
                if verbose:
                    print('... Skipped:',rawpath)
            numproc += 1
            if (not verbose) and ( (numproc%20) == 0 ) and (callback == None):
                 print('... Processed:',numproc,'raw files so far.')
            if callback != None:
                callback(numproc,userarg)
        
    return errors, newimages
    

##########################
# Database manipulations #
##########################

def select_all(infotable):
    """
    Set all the selected flags.
    """
    for i in range(0,len(infotable)):
        infotable[i]['selected'] = True

def unselect_all(infotable):
    """
    Clear all the selected flags.
    """
    for i in range(0,len(infotable)):
        infotable[i]['selected'] = False

def next_selected_index(infotable,curindex,direction):
    """
    Return the next selected index from curindex, forwards if direction +ve
    or backwards if -ve. Return curindex if nothing (else) is selected.
    """
    if direction > 0:
        for newindex in range(curindex+1,len(infotable)):
            if infotable[newindex]['selected']:
                return newindex
        return curindex
    else:
        for newindex in range(curindex-1,-1,-1):
            if infotable[newindex]['selected']:
                return newindex
        return curindex

def next_index(infotable,curindex,direction):
    """
    Return the next index from curindex (ignoring selection), forwards if direction +ve
    or backwards if -ve. Return curindex if nothing (else) is selected.
    """
    if direction > 0:
        return min(curindex+1,len(infotable)-1)
    else:
        return max(curindex-1,0)

def make_selected_subset(infotable):
    """
    Return a table which is that subset of infotable which is selected.
    Entries in the returned table have an additional field: 'orgindex' which
    is the index of the selected entry in infotable.
    """
    seltable = []
    for i in range(0,len(infotable)):
        entry = infotable[i]
        if entry['selected']:
            entry['orgindex'] = i
            seltable.append(entry)
    return seltable

def hide_entry(infotable,index):
    """
    Hide an entry at index.
    """
    if index >= 0 and index < len(infotable):
        infotable[index]['hide'] = KHIDE

def unhide_entry(infotable,index):
    """
    Unhide an entry. Remember it was hidden though.
    """
    if index >= 0 and index < len(infotable):
        if infotable[index]['hide'] == KHIDE:
            infotable[index]['hide'] = KUNHIDDEN

def stats(infotable):
    """
    Return some statistics on the database.
    """
    totalsize = 0.0
    num_exif = 0
    num_geotagged = 0
    num_commented = 0
    num_cameraed = 0
    num_vert = 0
    num_raws = 0
    num_processed = 0
    first_time = 0
    last_time = 0
    first_item = True
    for entry in infotable:
        totalsize += float(entry['bytes'])
        if entry['exif']:
            num_exif += 1
        if entry['geotags']:
            num_geotagged += 1
        if len(entry['comment']) > 0:
            num_commented += 1
        if entry['maker'] != 'unknown':
            num_cameraed += 1
        if entry['orient'] > 4:
            num_vert += 1
        if 'rawfilename' in entry:
            num_raws += 1
        if 'processor' in entry:
            num_processed += 1
        if first_item:
            first_time = last_time = entry['systime']
            first_item = False
        else:
            if entry['systime'] < first_time:
                first_time = entry['systime']
            if entry['systime'] > last_time:
                last_time = entry['systime']
    return (totalsize, num_exif, num_geotagged, num_commented, num_cameraed, num_vert, first_time, last_time, num_raws, num_processed)

def camera_full_name(entry):
    """
    Concatenate maker and model to get a single camera name string.
    """
    maker = entry['maker']
    maker = maker[0].upper() + maker[1:]
    model = entry['model']
    model = model[0].upper() + model[1:]
    return (maker + ' ' + model)

def camera_list(infotable):
    """
    Return a list of camera/model names found in the database.
    """
    camera_names = []
    for entry in infotable:
        if entry['maker'] != 'unknown' and entry['model'] != 'unknown':
            full_name = camera_full_name(entry)
            if not full_name in camera_names:
                camera_names.append(full_name)
    return sorted( camera_names, key=str.casefold )

def add_tag(entry,tag):
    """
    Add tag to the tag list of entry.
    """
    if len(tag) > 0:
        if not (tag in entry['tags']):
            entry['tags'].append(tag)

def remove_tag(entry,tag):
    """
    Remove tag from entry's tag list.
    """
    if len(tag) > 0 and len(entry['tags']) > 0:
        if tag in entry['tags']:
            entry['tags'].remove(tag)

def remove_all_tags(entry):
    """
    Remove all tags for entry.
    """
    entry['tags'] = []

def find_all_tags(infotable):
    """Return a list of all unique tags in infotable."""
    alltags = []
    for info in infotable:
        if len(info['tags']) > 0:
            for tag in info['tags']:
                if not (tag in alltags):
                    alltags.append(tag)
    return sorted(alltags, key=str.casefold)

def change_time(entry,unixtime):
    """
    Change entry to have time unixtime. This is a significant
    operation: (1) set entry['systime'], (2) set entry['date'],
    (3) rename thumbnail, (4) rename photo. To ensure
    consistency, the database file should be saved after this
    operation completes successfully.
    Note that unixtime should be in UTC (by definition).
    """
    current_thumb =  os.path.join('thumbnails',make_time_file_name(entry,'T'))
    current_photo =  os.path.join('photos',make_time_file_name(entry,'P'))
    if 'rawfilename' in entry:
        original_raw_name = entry['rawfilename']
        original_raw_name_stem,original_raw_name_ext = os.path.splitext(original_raw_name)
        current_rawname = make_time_file_name(entry,'R',inext=original_raw_name_ext)
    entry['systime'] = unixtime
    entry['date'] = time_to_exif(entry['systime'])
    new_thumb =  os.path.join('thumbnails',make_time_file_name(entry,'T'))
    new_photo =  os.path.join('photos',make_time_file_name(entry,'P'))
    if 'rawfilename' in entry:
        new_rawname = make_time_file_name(entry,'R',inext=original_raw_name_ext)
    print( 'change_time():' )
    print( '... current_thumb =',current_thumb )
    print( '... current_photo =',current_photo )
    print( '... new_thumb =',new_thumb )
    print( '... new_photo =',new_photo )
    if 'rawfilename' in entry:
        print( '... current_rawname =',current_rawname )
        print( '... new_rawname =',new_rawname )
    if os.access( current_thumb, os.F_OK ) and os.access( current_photo, os.F_OK ):
        if (not os.access( new_thumb, os.F_OK )) and (not os.access( new_photo, os.F_OK )):
            os.rename( current_thumb, new_thumb )
            os.rename( current_photo, new_photo )
            if 'rawfilename' in entry:
                if os.access( current_rawname, os.F_OK ) and (not os.access( new_rawname, os.F_OK )):
                    os.rename( current_rawname, new_rawname )
    
def in_time_range(entry, startunixtime, endunixtime):
    """
    See if entry lies in a specified time range.
    """
    phototime = entry['systime']
    return( phototime >= startunixtime and phototime <= endunixtime )

def unselect_by_time_range(infotable, startunixtime, endunixtime):
    """
    Unselect entries not in the specified time range.
    """
    for i in range(0,len(infotable)):
        if not in_time_range(infotable[i], startunixtime, endunixtime):
            infotable[i]['selected'] = False

def delete_selected(infotable,deletedtable):
    """
    Remove selected entries from infotable and place them on a deleted list.
    """
    newinfotable = []
    deletedhashes = []
    deltag = 'del_' + time.strftime("%Y:%m:%d:%H:%M:%S", time.localtime())
    for i in range(0,len(deletedtable)):
        delentry = deletedtable[i]
        if delentry['hashval'] not in deletedhashes:
            deletedhashes.append( delentry['hashval'] )

    for i in range(0,len(infotable)):
        entry = infotable[i]
        if entry['selected']:
            if entry['hashval'] not in deletedhashes:
                entry['tags'].append( deltag )
                deletedtable.append( entry )
        else:
            newinfotable.append( entry )

    return (newinfotable, deletedtable)

def undelete(infotable,deletedtable):
    """
    Move all entries from the deleted list to infotable.
    Empty the deleted list.
    """
    return ((infotable + deletedtable), [])

##########################
# Database visualization #
##########################

def image_coord(info):
    """
    Return an x,y coordinate in time for an image.
    """
    timetuple = time.localtime(info['systime'])
    x = timetuple[1] + float(timetuple[2]) / 31.0
    y = ( timetuple[0] - 2000 ) + float(timetuple[3]) / 50.0
    return (x,y)

def image_coord_axes(infotable):
    """
    Find axis ranges
    """
    (x,y) = image_coord(infotable[0])
    ymin = ymax = y
    for info in infotable:
        (x,y) = image_coord(info)
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    return [0, 14, 0, ymax+1]

########################
# Command line utility #
########################

if __name__ == '__main__':
    infotable = []
    hashes = []
    deletedtable = []
    testing = False

    # Command line utility program.
    # Open (if the file exists) or create (if it doesn't) a database.
    # Process an input tree adding to the database.
    # Save the database.
    # Generate (additional) unique thumbnail and full res images.
    print('==========================================================================')
    print('photohack.py - Create, Add to and/or Summarize a Photohack Image Database.')
    print('==========================================================================')
    parser = argparse.ArgumentParser()
    parser.add_argument("database_name", help="Name of the database to create or append to.")
    parser.add_argument("input_tree", help="Directory (tree) containing images to add to the database.")
    parser.add_argument("-v", "--verbose", help="Display detailed progress information.", action="store_true")
    parser.add_argument("-n", "--nomodify", help="Do not add anything to the database.", action="store_true")
    parser.add_argument("-t", "--tags", help="Comma separated list of tags to apply to newly added photos")
    parser.add_argument("-c", "--camera", help="Maker,Model of camera set for this image set. For images from film cameras.")
    args = parser.parse_args()
    #print args.database_name, args.input_tree
    start_time = time.time()

    if args.tags is not None:
        new_tag_list = args.tags.split(',')
    else:
        new_tag_list = None

    if args.camera is not None:
        maker,model = args.camera.split(',')
    else:
        maker = model = None

    # Split the database name in to a leading directory part (if any - specifies the "home"
    # directory location) and the database file name part.
    dbhomedir, dbname = os.path.split( args.database_name )
    photodbname =  dbname + '.photodb'
    if dbhomedir != '':
        try:
            os.chdir( dbhomedir )
        except:
            print('FATAL: Cannot change working directory to database home:', dbhomedir)
            sys.exit(9)  

    # Check the input tree exists. If not, give up. Unless --nomodify, when we don't care.
    dirname = args.input_tree
    if not args.nomodify:
        if not os.access( dirname, os.F_OK ):
            print('FATAL: Input directory (tree) does not exist:', dirname)
            sys.exit(9)

    # See if the database file exists. If so, read it in.
    print('INFO: Database home directory:', os.getcwd())
    if os.access( photodbname, os.F_OK ):
        print('INFO: Reading existing database:',photodbname)
        (last_dirname, infotable, hashes, deletedtable) = load_photo_data(photodbname)
        print('INFO: Total of',len(hashes),'image infos loaded.')
        if len(hashes) == 0:
            print('FATAL: Could not load:', photodbname)
            sys.exit(9)
        print('INFO: Last tree added was:',last_dirname)
    else:
        print('INFO: Creating new database:',photodbname)

    # Add the new images from the input tree *unless* told not to.
    if not args.nomodify:

        # Phase 1: Add the photos to the database and save the database.
        print('Phase 1: Adding new unique photos to the database.')
        errors, added, hwm = add_photos(dirname, infotable, hashes, args.verbose, None, new_tag_list, maker, model)
        print('INFO: Total of',len(hashes),'unique images in the database so far.')
        print('INFO: Added',added,'new images this time.')
        if errors > 0:
            print('WARNING: Encountered', errors,'errors when adding photos.')
        if not save_photo_data(photodbname, dirname, infotable, hashes, deletedtable):
            print('FATAL: Failed to save updated database.')
            sys.exit(9)

        # Phase 2: Generate new unique thumbnails and image copies.
        print('Phase 2: Generating new unique thumbnails and image copies.')
        errors, newthumbs = create_thumbnails(infotable,'thumbnails',args.verbose)
        if errors < 0:
            print('FATAL: Failed to create thumbnails directory.')
            sys.exit(9)
        print('INFO: Added',newthumbs,'new, unique, thumbnail images.')
        if errors > 0:
            print('WARNING: Encountered', errors,'errors when generating thumbnails.')
        errors, newimages = create_images(infotable,'photos',args.verbose)
        if errors < 0:
            print('FATAL: Failed to create photos directory.')
            sys.exit(9)
        print('INFO: Added',newimages,'new, unique, full images.')
        if errors > 0:
            print('WARNING: Encountered', errors,'errors when copying images.')
        errors, newraws = create_raws(infotable,'raws',args.verbose)
        if errors < 0:
            print('FATAL: Failed to create raws directory.')
            sys.exit(9)
        print('INFO: Added',newraws,'new, unique, RAW images.')
        if errors > 0:
            print('WARNING: Encountered', errors,'errors when copying images.')

    # Selected flags?
    for info in infotable:
        if info['selected']:
            if False: print('Selected:',info['filename'])

    # Phase 3: Show statistics.
    totalsize,\
    num_exif,\
    num_geotagged,\
    num_commented,\
    num_cameraed,\
    num_vert,\
    first_time,\
    last_time,\
    num_raw, \
    num_processed = stats( infotable )
    num_images = len(infotable)
    print('INFO: Full image disk usage =',int(totalsize/1000000.0),'MBytes.')
    if num_images > 0:
        print('      Number of images with Exif =',num_exif,' (',int((1000.0*num_exif)/num_images)/10.0,')%')
        print('      Number of images with RAW version =',num_raw,' (',int((1000.0*num_raw)/num_images)/10.0,')%')
        print('      Number of processed images =',num_processed,' (',int((1000.0*num_processed)/num_images)/10.0,')%')
        print('      Number of deleted images =',len(deletedtable))
        print('      Number of images geotagged =',num_geotagged,' (',int((1000.0*num_geotagged)/num_images)/10.0,')%')
        print('      Number of images with JFIF comment =',num_commented,' (',int((1000.0*num_commented)/num_images)/10.0,')%')
        print('      Number of camera originals =',num_cameraed,' (',int((1000.0*num_cameraed)/num_images)/10.0,')%')
        print('      Number with vertical orientation =',num_vert,' (',int((1000.0*num_vert)/num_images)/10.0,')%')
        print('      Date of earliest image in database =',time_to_exif(first_time))
        print('      Date of latest image in database =',time_to_exif(last_time))

        if args.verbose:
            cameras = camera_list( infotable )
            print('INFO: Number of camera types =',len(cameras))
            for camera in sorted(cameras, key=str.casefold):
                print('     ',camera)

            all_tags = find_all_tags( infotable )
            print('INFO: Total number of unique tags =',len(all_tags))
            for tag in sorted(all_tags, key=str.casefold):
                print('     ',tag)
            
    # Finished.
    elapsed_time = time.time() - start_time
    elapsed_mins = int(elapsed_time) // 60
    elapsed_secs = elapsed_time - ( 60 * elapsed_mins )
    print('INFO: Processing took:',elapsed_mins,'minutes',int(10.0*elapsed_secs)/10.0,'seconds.')
    print('Done.')
