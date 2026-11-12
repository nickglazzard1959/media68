#!/usr/bin/env python3
"""
   photox.py - Photo database, browsing and tag editing.
   =====================================================

   Aid to maintaining a coherent database of photos, eliminating duplicates, adding
   tags, selecting in various ways, with a decent image display facility.

   The primary idea is that photos are organized by time, and initially a time chart
   showing the distribution of photos in time (based on Exif if at all possible) is
   displayed. Picking on the time chart shows the image with information in a small
   display. It can then be displayed in a large format, amongst other things.

   The images in the database are never changed, but associated metadata stored in a
   database file can be modified to set the (correct) orientation, amongst other things.

   I wrote this because myself and my wife have several cameras and phones, and
   we periodically dump the photos on them to disk when they get full or when
   we worry they might be lost if a device fails. This has led to lots of duplication
   of images and a pretty much total lack of order. So much so that we couldn't find
   anything anymore! Also, many devices do not know the image orientation, so they
   need to be turned around as required. Actually turning the pictures around and saving
   the modified image didn't seem like the ideal solution ...

   There may be existing tools that do all that we need and more, but this does
   *just* what we need (and not much more). We can add things to it as needed later.
   It may or may not be useful to anyone else, and it probably shouldn't be trusted
   too much! (Although it never deletes or changes the photographs themselves, so
   only metadata would be lost if there was an error).

   This is one part of the system. The other is "photohack.py" which should seen for
   an explanation of the "database structure" (such as it is). That handles most
   of the "database" side of things and can be used to build other, special purpose,
   tools to fix things up. If run as a main program, it can create, add to or summarize
   a "database" from the command line.

   Now modified for Qt5. (April 2017). Hopefully, not too many new bugs.

   Converted to Python 3 and PySide2 in November 2019.
   Added support for RAW files associated with JPEGs and many other improvements.

   Now modified for Qt6 / PySide6 in November 2026.
   Some very minor changes (such as export directories can be manually typed in).

   Nick Glazzard. February & April 2014, March 2015, May 2016, April 2017, November 2019, November 2026.
   -----------------------------------------------------------------------------------------------------
"""

# Imports ... Lots of them!
import sys

try:
    from OpenGL.GL import GL_ALPHA
    from OpenGL.GL import GL_BLEND
    from OpenGL.GL import GL_CLAMP
    from OpenGL.GL import GL_CLAMP_TO_BORDER
    from OpenGL.GL import GL_COLOR_BUFFER_BIT
    from OpenGL.GL import GL_FALSE
    from OpenGL.GL import GL_FLAT
    from OpenGL.GL import GL_LINEAR
    from OpenGL.GL import GL_LINEAR_MIPMAP_LINEAR
    from OpenGL.GL import GL_LINES
    from OpenGL.GL import GL_LINE_LOOP
    from OpenGL.GL import GL_MAX_TEXTURE_SIZE
    from OpenGL.GL import GL_MODULATE
    from OpenGL.GL import GL_NEAREST
    from OpenGL.GL import GL_ONE_MINUS_SRC_ALPHA
    from OpenGL.GL import GL_POINTS
    from OpenGL.GL import GL_PROJECTION
    from OpenGL.GL import GL_QUADS
    from OpenGL.GL import GL_RGB
    from OpenGL.GL import GL_SRC_ALPHA
    from OpenGL.GL import GL_TEXTURE_2D
    from OpenGL.GL import GL_TEXTURE_BORDER_COLOR
    from OpenGL.GL import GL_TEXTURE_ENV
    from OpenGL.GL import GL_TEXTURE_ENV_MODE
    from OpenGL.GL import GL_TEXTURE_MAG_FILTER
    from OpenGL.GL import GL_TEXTURE_MIN_FILTER
    from OpenGL.GL import GL_TEXTURE_WRAP_S
    from OpenGL.GL import GL_TEXTURE_WRAP_T
    from OpenGL.GL import GL_TRIANGLE_STRIP
    from OpenGL.GL import GL_UNPACK_ALIGNMENT
    from OpenGL.GL import GL_UNSIGNED_BYTE
    from OpenGL.GL import glBegin
    from OpenGL.GL import glBindTexture
    from OpenGL.GL import glBlendFunc
    from OpenGL.GL import glClear
    from OpenGL.GL import glClearColor
    from OpenGL.GL import glColor4f
    from OpenGL.GL import glDepthMask
    from OpenGL.GL import glDisable
    from OpenGL.GL import glEnable
    from OpenGL.GL import glEnd
    from OpenGL.GL import glFlush
    from OpenGL.GL import glGenTextures
    from OpenGL.GL import glGenerateMipmap
    from OpenGL.GL import glGetInteger
    from OpenGL.GL import glLineWidth
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import glOrtho
    from OpenGL.GL import glPixelStorei
    from OpenGL.GL import glPointSize
    from OpenGL.GL import glShadeModel
    from OpenGL.GL import glTexCoord2f
    from OpenGL.GL import glTexEnvi
    from OpenGL.GL import glTexImage2D
    from OpenGL.GL import glTexParameterf
    from OpenGL.GL import glTexParameterfv
    from OpenGL.GL import glVertex2f
    from OpenGL.GL import glViewport
    from OpenGL.GLU import GLfloat
except ImportError:
    print("Photox needs PyOpenGL.")
    sys.exit(9)

try:
    from PySide6.QtCore import QCoreApplication
    from PySide6.QtCore import QDateTime
    from PySide6.QtCore import QEvent
    from PySide6.QtCore import QRect
    from PySide6.QtCore import Qt
    from PySide6.QtCore import __version__ as pyside_version
 
    from PySide6.QtGui import QCursor
    from PySide6.QtGui import QFont
    from PySide6.QtGui import QIcon
 
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QComboBox
    from PySide6.QtWidgets import QDateTimeEdit
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QDialogButtonBox
    from PySide6.QtWidgets import QFileDialog
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget
except ImportError:
    print("Photox needs PySide6.")
    sys.exit(9)

try:
    from PIL import Image
    from PIL import ImageDraw
except ImportError:
    print("Photox needs Python Imaging Library (Pillow).")
    sys.exit(9)

try:
    import numpy
except ImportError:
    print("Photox needs Numpy.")
    sys.exit(9)

try:
    import webbrowser
except ImportError:
    print("Photox needs webbrowser.")
    sys.exit(9)

import photohack
import json
import math
import time
import datetime
import bisect
import os
import shutil
import subprocess

# Version number of PhotoX. Just do this manually now.
current_version_string = "0.6"

# Display modes
TIME_ONLY = 0
TIME_THUMB = 1
PHOTO_ONLY = 2
INFO_DISPLAY = 3

# View select modes
VIEW_NOPICK = 0
VIEW_PICK = 1
VIEW_UNPICK = 2

# Tagging modes
K_TAG_1 = 0
K_TAG_1_MOVE = 1
K_TAG_SELECTED = 2


class PhotoxWidget(QOpenGLWidget):
    """
    Display a visualization of photos in time. Allow browsing by picking points
    on the visualization.
    """
    def __init__(self,parent=None):
        super(PhotoxWidget,self).__init__(parent)
        self.parent = parent
        self.width_pixels = 900 # Initial drawing area size.
        self.height_pixels = 600
        self.user = None
        # Widget state.
        self.setMinimumSize(self.width_pixels,self.height_pixels)
        self.setFocusPolicy(Qt.ClickFocus)
        self.havefocus = False
        self.viewport = (self.width_pixels,self.height_pixels)
        self.ctrl = False
        self.shift = False
        self.alt = False
        self.draw_big = True
        # Mouse position tracking.
        self.oldmouse_x = 0
        self.oldmouse_y = 0
        # Debugging.
        self.debuglevel = 0 #2
        # Read character to texture location data, then read the texture
        # image containing the character glyphs.
        self.fast_graphics = True
        self.is_macos = sys.platform.startswith('darwin')
        if self.is_macos:
            ourfontdata = '/Applications/photox.app/Contents/Resources/mainfonttexture'
        else:
            ourfontdata = '/usr/local/applications/photox/mainfonttexture'
        if not os.path.isfile( ourfontdata+'.jsn' ):
            ourfontdata = 'mainfonttexture'
        self.loadCharDefinitions(ourfontdata)
        # Layout control
        self.current_year = datetime.datetime.now().year
        self.current_month = datetime.datetime.now().month
        self.current_day = datetime.datetime.now().day
        self.year_delta_lines = 100
        self.month_offset = 0
        self.month_scale = 1
        self.year_offset = 0
        # Graphical selection and image viewing
        self.draw_sel_box = False
        self.valid_when = False
        self.start_month = 0
        self.start_year = 0
        self.end_month = 0
        self.end_year = 0
        self.cur_month = 0
        self.cur_year = 0
        self.disp_mode = TIME_THUMB
        self.saved_disp_mode = self.disp_mode
        self.old_disp_mode = -1
        self.pbox_cur_x = 0
        self.pbox_start_x = 0
        self.pbox_end_x = 0
        self.pbox_cur_y = 0
        self.pbox_start_y = 0
        self.pbox_end_y = 0
        self.do_zoom = False
        self.zoom_scale = 1.0
        self.zoom_tx = 0.0
        self.zoom_ty = 0.0
        self.zoom_tx_start = 0.0 # Zoom shifts at the start of panning.
        self.zoom_ty_start = 0.0
        self.panning = False
        self.have_zoom_box = False
        self.reread_image = False
        self.view_image_select = VIEW_NOPICK
        self.thumb_rect = (0.0,0.0,20.0,20.0)
        self.pickedset = []
        self.point_size = 4
        self.pil_photo_image = None
        # Photo database
        self.dirname = ''
        self.dbname = ''
        self.dbfolder = ''
        self.infotable = []
        self.hashes = []
        self.deletedtable = []
        self.sortedinfotable = []
        self.sortedsystimes = []
        self.sortedhashes = []
        self.cameras = []
        self.selected_photo = -1
        self.last_selected_photo = -1
        self.info_message = ''
        self.subselect = False
        self.sub_sortedsystimes = []
        self.starting_dir = os.getcwd()
        self.script_name = os.path.join(self.starting_dir,__file__)
        self.dont_trust_orient = True  # If true, when saving photos, always flip them to orientation 1.
        # Save (export) JPEGs and RAWs.
        self.outjpegpath = None
        self.outrawpath = None
        # Import processed versions.
        self.inprocpath = None

    def setUser(self,user):
        """
        Keep track of the object using me.
        """
        self.user = user

    def month_to_xpos(self,month):
        """
        Convert a month to an x position.
        """
        xdelta = (self.width_pixels * self.month_scale) // 13
        xpos = xdelta * (month - self.month_offset)
        return xpos

    def xpos_to_month(self,xpos):
        """
        Convert an x position to a month.
        """
        xdelta = (self.width_pixels * self.month_scale) // 13
        month = float(xpos) / xdelta + self.month_offset
        if month >= 13.0:
            month = 12.9999
        return month

    def month_day_to_xpos(self,imonth,iday):
        """
        Convert integer month and day to an x position.
        """
        return self.month_to_xpos(imonth+float(iday)/31.0)

    def ypos_to_year(self,ypos):
        """
        Convert a y position to a year.
        """
        year = float(ypos) / self.year_delta_lines
        return self.current_year - year - self.year_offset + 1

    def year_to_ypos(self,year,glcoord=False):
        """
        Convert a year to a y position.
        """
        ypos = -(year - 1 + self.year_offset - self.current_year) * self.year_delta_lines
        if glcoord:
            ypos = self.height_pixels - ypos
        return ypos

    def year_hms_to_ypos(self,yint,hint,mint,sint,glcoord=True):
        """
        Convert integer year, hours, mins secs to a y position.
        """
        ypos = self.year_to_ypos(yint,glcoord)
        ypos += 0.8 * self.year_delta_lines * (float(hint) + float(mint)/60.0 + float(sint)/3600.0)/24.0
        return ypos       

    def year_to_time(self,year):
        """
        Convert the fractional part of the year coordinate to hours,mins,secs.
        """
        (yfrac,yint) = math.modf(year)
        hours = min(24, 24 * 1.25 * yfrac)
        (hfrac,hint) = math.modf(hours)
        mins = 60 * hfrac
        (mfrac,mint) = math.modf(mins)
        sint = int(60*mfrac)
        return(int(yint),int(hint),int(mint),int(sint))

    def month_to_day(self,month):
        """
        Convert the fractional part of a month to a valid day.
        """
        monthdays=[31,28,31,30,31,30,31,31,30,31,30,31]
        (monfrac,monint) = math.modf(month)
        dayint = min( int(31*monfrac), monthdays[int(monint)-1]-1 )
        if monint < 1:
            monint = 1
            dayint = 0
        return(int(monint),int(dayint)+1)

    def unix_time_to_year_month(self,unixtime):
        """
        Convert a Unix time (seconds from midnight 1-JAN-1970) to a year,month time.
        """
        dt = datetime.datetime.fromtimestamp(unixtime)
        month = dt.month + float(dt.day)/31.0
        year = dt.year + (float(dt.hour) + float(dt.minute)/60.0 + float(dt.second)/3600.0)/24.0
        return(year,month)

    def unix_time_to_position(self,unixtime):
        """
        Convert a Unix time (seconds from midnight 1-JAN-1970) to an (x,y) position.
        """
        dt = datetime.datetime.fromtimestamp(unixtime)
        x = self.month_day_to_xpos(dt.month,dt.day)
        y = self.year_hms_to_ypos(dt.year,dt.hour,dt.minute,dt.second,True)
        return(x,y)

    def year_month_to_unix_time(self,year,month):
        """
        Convert a year + fractional time and a month + fractional day to
        a Unix time.
        """
        (imonth,iday) = self.month_to_day(month)
        (iyear,ihour,imin,isec) = self.year_to_time(year)
        time_tuple = (iyear,imonth,iday,ihour,imin,isec,0,1,0)
        return time.mktime(time_tuple)       

    def current_position_to_unix_time(self):
        """
        Convert current position to a Unix time.
        """
        return self.year_month_to_unix_time(self.cur_year,self.cur_month)

    def ensure_fwd_time(self,sy,sm,ey,em):
        """
        Ensure (sy,sm) preceeds (or equals) (ey,em). Return the possibly swapped
        times.
        """
        sut = self.year_month_to_unix_time(sy,sm)
        eut = self.year_month_to_unix_time(ey,em)
        if sut > eut:
            return ey,em,sy,sm
        else:
            return sy,sm,ey,em

    def formatwhenstring(self,year,month):
        """
        Format our year/month times in to an Exif compatible string.
        """
        if month == 0 and year == 0:
            return ' '
        else:
            (yint,hint,mint,sint) = self.year_to_time(year)
            (monint,dayint) = self.month_to_day(month)
            if hint >= 24:
                hint = 23
                mint = 59
                sint = 59
            if monint > 12:
                monint = 12
            if yint < 1970:
                yint = 1970
            whenstring = '{0:04d}:{1:02d}:{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(yint,monint,dayint,hint,mint,sint)
            return whenstring

    def makewhenstring(self):
        """
        Make a readable date string to display current time.
        """
        return self.formatwhenstring(self.cur_year,self.cur_month)

    def makewhenboxstring(self):
        """
        Use the current selected time range to generate a string.
        """
        if not self.valid_when:
            return ' '
        else:
            (sy, sm, ey, em) = self.ensure_fwd_time(self.start_year,self.start_month,self.end_year,self.end_month)
            whenstart = self.formatwhenstring(sy,sm)
            whenend = self.formatwhenstring(ey,em)
            return '{0} > {1}'.format(whenstart,whenend)

    def draw_months(self,ypos):
        """
        Draw the month labels.
        """
        months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        xdelta = (self.width_pixels * self.month_scale) // 13
        xpos = (1.5 - self.month_offset) * xdelta
        glColor4f(0.1,0.1,0.3,1.0) # Dark blue
        for month in months:
            if xpos > 0.5*xdelta:
                self.draw_string_cent((xpos,ypos),month)
            xpos += xdelta

    def draw_month_verticals(self):
        """
        Draw month start markers
        """
        xdelta = (self.width_pixels * self.month_scale) // 13
        xpos = (1.0 - self.month_offset) * xdelta
        glDepthMask( GL_FALSE )
        glLineWidth(2)
        glColor4f(1.0,1.0,1.0,1.0)
        for i in range(0,13):
            glBegin(GL_LINES)
            glVertex2f(xpos,0.0)
            glVertex2f(xpos,self.height_pixels)
            glEnd()
            xpos += xdelta

    def draw_day_verticals(self):
        """
        Draw day start markers. Each month has 31 days, with some disabled.
        """
        monthdays=[31,28,31,30,31,30,31,31,30,31,30,31]
        xdelta = (self.width_pixels * self.month_scale) // 13
        xdaydelta = xdelta // 31
        glLineWidth(1)
        xpos = (1.0 - self.month_offset) * xdelta
        for m in range(0,12):
            xdaypos = xpos
            for d in range(0,31):
                if d < monthdays[m]:
                    glColor4f(0.3,0.8,0.3,1.0)
                else:
                    glColor4f(0.8,0.3,0.3,1.0)
                glBegin(GL_LINES)
                glVertex2f(xdaypos,0.0)
                glVertex2f(xdaypos,self.height_pixels)
                glEnd()
                xdaypos += xdaydelta
            xpos += xdelta

    def draw_weekish_verticals(self):
        """
        Draw quarter month start markers.
        """
        xdelta = (self.width_pixels * self.month_scale) // 13
        xweekdelta = xdelta // 4
        glColor4f(0.3,0.8,0.3,1.0)
        glLineWidth(1)
        xpos = (1.0 - self.month_offset) * xdelta
        for m in range(0,12):
            xweekpos = xpos
            for d in range(0,31):
                glBegin(GL_LINES)
                glVertex2f(xweekpos,0.0)
                glVertex2f(xweekpos,self.height_pixels)
                glEnd()
                xweekpos += xweekdelta
            xpos += xdelta

    def draw_years(self,thisyear):
        """
        Draw the year labels.
        """
        xpos = 20
        ypos = self.height_pixels - self.year_delta_lines + 25
        glColor4f(0.1,0.1,0.3,1.0) # Dark blue
        while ypos > 0:
            self.draw_string_cent((xpos,ypos),str(thisyear))
            ypos -= self.year_delta_lines
            thisyear -= 1

    def draw_year_horizontals(self):
        """
        Draw year start markers.
        """
        ypos = self.height_pixels - self.year_delta_lines
        glDepthMask( GL_FALSE )
        glLineWidth(2)
        glColor4f(1.0,1.0,1.0,1.0)
        while ypos > 0:
            glBegin(GL_LINES)
            glVertex2f(0.0,ypos)
            glVertex2f(self.width_pixels,ypos)
            glEnd()
            ypos -= self.year_delta_lines

    def draw_box(self):
        """
        Draw a selection box.
        """
        x1 = self.month_to_xpos(self.start_month)
        y1 = self.year_to_ypos(self.start_year,True)
        x2 = self.month_to_xpos(self.end_month)
        y2 = self.year_to_ypos(self.end_year,True)
        glLineWidth(1)
        glColor4f(1.0,0.0,0.0,1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1,y1)
        glVertex2f(x2,y1)
        glVertex2f(x2,y2)
        glVertex2f(x1,y2)
        glEnd()

    def draw_pbox(self):
        """
        Draw a photo selection box.
        """
        x1 = self.pbox_start_x
        y1 = self.height_pixels - self.pbox_start_y
        x2 = self.pbox_end_x
        y2 = self.height_pixels - self.pbox_end_y
        glLineWidth(1)
        glColor4f(1.0,0.0,0.0,1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1,y1)
        glVertex2f(x2,y1)
        glVertex2f(x2,y2)
        glVertex2f(x1,y2)
        glEnd()
        glColor4f(1.0,1.0,1.0,1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1-1,y1+1)
        glVertex2f(x2+1,y1+1)
        glVertex2f(x2+1,y2-1)
        glVertex2f(x1-1,y2-1)
        glEnd()

    def draw_now_patch(self):
        """
        Make the current time clear.
        """
        x1 = self.month_to_xpos(self.current_month+float(self.current_day)/31.0)
        y1 = self.year_to_ypos(self.current_year,True)
        x2 = self.month_to_xpos(12.9999)
        y2 = self.year_to_ypos(self.current_year+1,True)
        glLineWidth(1)
        glColor4f(0.5,0.5,0.5,1.0)
        glBegin(GL_TRIANGLE_STRIP)
        glVertex2f(x1,y1)
        glVertex2f(x1,y2)
        glVertex2f(x2,y1)
        glVertex2f(x2,y2)
        glEnd()

    def draw_whenstring(self):
        """
        Draw the date & time for the current mouse position.
        """
        if self.valid_when:
            when = self.makewhenstring()
            whenlen = self.string_length(when)
            fixdelta = min(0, (self.width_pixels - (self.oldmouse_x+whenlen)))
            glLineWidth(2)
            glColor4f(1.0,0.0,1.0,1.0) # Magenta
            glBegin(GL_LINES)
            glVertex2f(self.oldmouse_x-5,self.height_pixels-self.oldmouse_y)
            glVertex2f(self.oldmouse_x+5,self.height_pixels-self.oldmouse_y)
            glVertex2f(self.oldmouse_x,self.height_pixels-self.oldmouse_y-5)
            glVertex2f(self.oldmouse_x,self.height_pixels-self.oldmouse_y+5)
            glEnd()
            glColor4f(0.1,0.1,0.3,1.0) # Dark blue
            self.draw_string((self.oldmouse_x+fixdelta,self.height_pixels-self.oldmouse_y),when)

    def make_tag_string(self,tag_list):
        """
        Make a string representation of a tag list.
        """
        ret = ''
        if len(tag_list) == 0:
            ret = '<None>'
        else:
            ret = tag_list[0]
            for i in range(1,len(tag_list)):
                ret += ', '+tag_list[i]
        return ret

    def texco_orient(self,orient):
        """
        Return the correct set of texture coords at the 4 vertices of a
        quad for the orientation orient. If delta, convert to correct axis deltas
        about a position (for zooming).
        """
        texcodict={1:[(0,1),(1,1),(1,0),(0,0)], # 0,1,2,3 Horizontal *normal*
                   2:[(1,1),(0,1),(0,0),(1,0)], # 1,0,3,2 Horizontal, Mirror left-right
                   3:[(1,0),(0,0),(0,1),(1,1)], # 2,3,0,1 Horizontal, Rotate 180
                   4:[(0,0),(1,0),(1,1),(0,1)], # 3,2,1,0 Horizontal, Mirror top-bottom
                   5:[(1,0),(1,1),(0,1),(0,0)], # 2,1,0,3 Mirror left-right, Rotate 270 cw
                   6:[(1,1),(1,0),(0,0),(0,1)], # 1,2,3,0 Rotate 90 cw
                   7:[(0,1),(0,0),(1,0),(1,1)], # 0,3,2,1 Mirror left-right, Rotate 90 cw
                   8:[(0,0),(0,1),(1,1),(1,0)]} # 3,0,1,2 Rotate 270 cw
        return texcodict[orient]

    def draw_image(self,photo_texture,qwidth,qheight,wmargin,hmargin,orient,xshift):
        """
        Draw an RGB image as a textured quad. The image must already have been
        converted (bound) to a texture.
        """
        # Get the quad vertex texture coords, dealing with all possible orientations.
        texco = self.texco_orient(orient)
        # Draw the quad with the image textured on it.
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,photo_texture)
        if self.havefocus:
            glColor4f(1,1,1,1)
        else:
            glColor4f(1,1,1,1)
        glBegin(GL_QUADS)
        glTexCoord2f(texco[0][0],texco[0][1])
        glVertex2f(xshift+wmargin,hmargin)
        glTexCoord2f(texco[1][0],texco[1][1])
        glVertex2f(xshift+qwidth+wmargin,hmargin)
        glTexCoord2f(texco[2][0],texco[2][1])
        glVertex2f(xshift+qwidth+wmargin,qheight+hmargin)
        glTexCoord2f(texco[3][0],texco[3][1])
        glVertex2f(xshift+wmargin,qheight+hmargin)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def draw_image_full(self,photo_texture,qwidth,qheight,orient):
        """
        Draw the full resolution image.
        """
        # Get the image texture coordinates, accounting for orientation.
        texco = self.texco_orient(orient)
        # Find the corners of the quad in window space.
        cqx = 0.5 * self.width_pixels
        cqy = 0.5 * self.height_pixels
        qxl = cqx - self.zoom_scale * qwidth * (0.5 + self.zoom_tx)
        qyl = cqy - self.zoom_scale * qheight * (0.5 + self.zoom_ty)
        qxh = cqx + self.zoom_scale * qwidth * (0.5 - self.zoom_tx)
        qyh = cqy + self.zoom_scale * qheight * (0.5 - self.zoom_ty)
        # Draw the quad with the image textured on it.
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,photo_texture)
        if self.havefocus:
            glColor4f(1,1,1,1)
        else:
            glColor4f(0.5,0.5,0.5,0.2)
        glBegin(GL_QUADS)
        glTexCoord2f(texco[0][0],texco[0][1])
        glVertex2f(qxl,qyl)
        glTexCoord2f(texco[1][0],texco[1][1])
        glVertex2f(qxh,qyl)
        glTexCoord2f(texco[2][0],texco[2][1])
        glVertex2f(qxh,qyh)
        glTexCoord2f(texco[3][0],texco[3][1])
        glVertex2f(qxl,qyh)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        # Test window to image coordinate transformations and pixel lookups.
        # This is in support of imageviewwidget.
        if False:
            xw,yw = self.norm_image_to_window(0.0,0.0,qwidth,qheight)
            xn,yn = self.window_to_norm_image(xw,yw,qwidth,qheight)
            xi,yi = self.window_to_image(xw,yw,qwidth,qheight,orient)
            print('(qxl,qyl) =',qxl,qyl,' (0,0)image ->',xw,yw,'->',xn,yn,'-> pix/line',xi,yi)
            xw,yw = self.norm_image_to_window(1.0,1.0,qwidth,qheight)
            xn,yn = self.window_to_norm_image(xw,yw,qwidth,qheight)
            xi,yi = self.window_to_image(xw,yw,qwidth,qheight,orient)
            print('(qxh,qyh) =',qxh,qyh,' (1,1)image ->',xw,yw,'->',xn,yn,'-> pix/line',xi,yi)
            print('oldmouse:',self.oldmouse_x, self.oldmouse_y)
            if self.pil_photo_image != None:
                xi,yi = self.window_to_image(self.oldmouse_x,self.height_pixels-self.oldmouse_y,qwidth,qheight,orient)
                if( xi >= 0 and xi < self.pil_photo_image.size[0] and yi >= 0 and yi < self.pil_photo_image.size[1] ):
                    print('(xi,yi) =',xi,yi,'data:',self.pil_photo_image.getpixel((xi,yi)))

    def norm_image_to_window(self,xn,yn,qwidth,qheight):
        xw = 0.5 * self.width_pixels + self.zoom_scale * qwidth * ( xn - 0.5 - self.zoom_tx )
        yw = 0.5 * self.height_pixels + self.zoom_scale * qheight * ( yn - 0.5 - self.zoom_ty )
        return (xw,yw)

    def window_to_norm_image(self,xw,yw,qwidth,qheight):
        xn = (xw - ( 0.5 * self.width_pixels )) / (self.zoom_scale * qwidth) + 0.5 + self.zoom_tx
        yn = (yw - ( 0.5 * self.height_pixels )) / (self.zoom_scale * qheight) + 0.5 + self.zoom_ty
        return (xn,yn)

    def window_to_image(self,xw,yw,qwidth,qheight,orient):
        ordict={1:[0, 1,1,-1], # 0,1,2,3 Horizontal *normal*
                2:[1,-1,1,-1], # 1,0,3,2 Horizontal, Mirror left-right
                3:[1,-1,0, 1], # 2,3,0,1 Horizontal, Rotate 180
                4:[0, 1,0, 1], # 3,2,1,0 Horizontal, Mirror top-bottom
                5:[1,-1,0, 1], # 2,1,0,3 Mirror left-right, Rotate 270 cw
                6:[1,-1,1,-1], # 1,2,3,0 Rotate 90 cw
                7:[0, 1,1,-1], # 0,3,2,1 Mirror left-right, Rotate 90 cw
                8:[0, 1,0, 1]} # 3,0,1,2 Rotate 270 cw
        order = ordict[orient]
        xn,yn = self.window_to_norm_image(xw,yw,qwidth,qheight)
        xi = order[0] * self.photo_width + order[1] * xn * self.photo_width
        yi = order[2] * self.photo_height + order[3] * yn * self.photo_height
        if orient > 4:
            return (yi,xi)
        else:
            return (xi,yi)

    def bind_texture(self,photo_image,photo_texture,w,h,hiq):
        """
        Bind RGB image photo_image to texture photo_texture.
        """
        # Unfortunately, OpenGL has a maximum texture size, which may not be big enough.
        # If the image is too big, resize it before making it a texture.
        maxsize = glGetInteger(GL_MAX_TEXTURE_SIZE)
        if( w > maxsize or h > maxsize ):
            if w > h:
                h = ( h * maxsize ) // w
                w = maxsize
            else:
                w = ( w * maxsize ) // h
                h = maxsize
            safe_photo_image = photo_image.resize((w,h),Image.BILINEAR)
        else:
            safe_photo_image = photo_image
        # Set the edge pixels to the background colour to avoid zoom artefacts with OpenGL.
        if True:
            draw = ImageDraw.Draw(safe_photo_image)
            draw.line([(0,0),(w-1,0),(w-1,h-1),(0,h-1),(0,0)])
        # Set the image as a texture.
        glBindTexture(GL_TEXTURE_2D,photo_texture)
        photo_data = numpy.asarray(safe_photo_image,dtype=numpy.uint8)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        border_color = (GLfloat * 4)() 
        for i in range(0,4): 
            border_color[i] = 0.0 
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color) 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER )
        if hiq:
            texmaginterp = GL_LINEAR
            if self.fast_graphics:
                texmininterp = GL_LINEAR_MIPMAP_LINEAR
            else:
                texmininterp = GL_LINEAR
        else:
            texmaginterp = GL_NEAREST
            texmininterp = GL_NEAREST
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, texmaginterp )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, texmininterp )
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, \
                         w, h, \
                         0, GL_RGB, GL_UNSIGNED_BYTE, photo_data)
        if hiq and self.fast_graphics:
            glGenerateMipmap(GL_TEXTURE_2D)

    def make_image_texture(self,imagefilename,photo_texture,orient,hiq):
        """
        Bind a texture to an image in file imagefilename with orientation orient.
        The texture must already have been generated.
        Return the width and height of the image.
        """
        # Try to read the image file.
        try:
            photo_image = Image.open(imagefilename)
            if photo_image.mode != 'RGB':
                photo_image = photo_image.convert('RGB') # Ensure it is RGB
            if orient > 4: # Vertical formats
                photo_width = photo_image.size[1]
                photo_height = photo_image.size[0]
            else:          # Horizontal formats
                photo_width = photo_image.size[0]
                photo_height = photo_image.size[1]
            if self.debuglevel > 1:
                print('make_image_texture(): size=',photo_image.size[0],photo_image.size[1])
            self.pil_photo_image = photo_image
            self.bind_texture(photo_image,photo_texture,photo_image.size[0],photo_image.size[1],hiq)
        # If cannot read, say so in an image.
        except Exception as e:
            print("ERROR: Cannot read:", imagefilename, "Reason:", e)
            errormsg = 'Cannot read!'
            photo_width = 300
            photo_height = 266
            photo_image = Image.new('RGB',(photo_width,photo_height))
            draw = ImageDraw.Draw(photo_image)
            (w,h) = draw.textsize(errormsg)
            x = (photo_width-w)//2
            y = (photo_height-h)//2
            draw.text((x,y),errormsg)
            self.bind_texture(photo_image,photo_texture,photo_width,photo_height,False)
        return (photo_width,photo_height)

    def draw_photo(self):
        """
        If there is a selected photo, draw its thumbnail with information.
        """
        if self.sortedinfotable == None or len(self.sortedinfotable) == 0:
            return
        if self.selected_photo >= 0:
            if self.debuglevel > 1:
                print('self.selected_photo:',self.selected_photo,'self.last_selected_photo:',self.last_selected_photo)
                print('self.disp_mode:',self.disp_mode,'self.old_disp_mode`;',self.old_disp_mode)
                print('self.reread_image:',self.reread_image)
            info = self.sortedinfotable[self.selected_photo]
            # If it is not the same as the last selected photo,
            # read the thumbnail image.
            if (self.selected_photo != self.last_selected_photo) or \
                    (self.disp_mode != self.old_disp_mode) or \
                    self.reread_image:
                self.reread_image= False
                thumbsdir = 'thumbnails'
                thumbname = photohack.make_time_file_name(info,'T')
                thumbpath = os.path.join(thumbsdir,thumbname)
                if self.debuglevel > 1:
                    print('draw_photo(): Org name = ',info['filename'])
                if os.access( thumbpath, os.F_OK ):
                    if self.debuglevel > 1:
                        print('draw_photo(): Thumbpath=',thumbpath)
                    (self.photo_width,self.photo_height) = \
                        self.make_image_texture(thumbpath,self.photo_texture,info['orient'],False)
                    self.last_selected_photo = self.selected_photo
                else:
                    print('*** Failed to access thumbpath file:',thumbpath)
            # Draw the thumbnail image.
            margin = 10
            topmargin = 80
            if self.month_to_xpos(self.cur_month) < (self.width_pixels//2):
                xshift = self.width_pixels - (self.photo_width+2*margin)
            else:
                xshift = 0
            # Background rectangle. Save this so we cannot pick in it.
            self.thumb_rect = (xshift+0.0,0.0,xshift+self.photo_width+2*margin,self.photo_height+margin+topmargin)
            glColor4f(0.5,0.5,0.5,1.0)
            glBegin(GL_QUADS)
            glVertex2f(xshift+0.0,0.0)
            glVertex2f(xshift+self.photo_width+2*margin,0.0)
            glVertex2f(xshift+self.photo_width+2*margin,self.photo_height+margin+topmargin)
            glVertex2f(xshift+0.0,self.photo_height+margin+topmargin)
            glEnd()
            # image
            self.draw_image(self.photo_texture,self.photo_width,self.photo_height,
                            margin,margin,info['orient'],xshift)
            # information
            ypos = self.photo_height+topmargin
            self.draw_string((xshift+margin,ypos),info['date'])
            if info['orient'] < 5:
                restring = '{0}x{1}'.format(info['width'],info['height'])
            else:
                npixels = info['width'] * info['height']
                if npixels == 0: # Yes - really! Seems like EXIF w & h are not always there.
                    restring = '?MP'
                else:
                    if npixels < 1000000:
                        restring = '{0}KP'.format(npixels//1000)
                    else:
                        restring = '{0}MP'.format(npixels//1000000)
            xpos = self.photo_width+margin-self.string_length(restring)
            self.draw_string((xshift+xpos,ypos),restring)
            ypos -= self.linespace
            self.draw_string((xshift+margin,ypos),info['maker']+' '+info['model'].rstrip('\0'))
            orientstring = 'Rot:{0}'.format(info['orient'])
            xpos = self.photo_width+margin-self.string_length(orientstring)
            self.draw_string((xshift+xpos,ypos),orientstring)
            ypos -= self.linespace
            self.draw_string((xshift+margin,ypos),'Tags: '+self.make_tag_string(info['tags']), xshift+self.photo_width+margin)
            ypos -= self.linespace
            if info['geotags']:
                self.draw_string((xshift+margin,ypos),'Where: {0:.4f},{1:.4f}'.format(info['lat'],info['long']))
            else:
                self.draw_string((xshift+margin,ypos),'Where: unknown')
            if 'rawfilename' in info:
                rawstring = '+RAW'
                xpos = self.photo_width+margin-self.string_length(rawstring)
                self.draw_string((xshift+xpos,ypos),rawstring)

    def find_full_image_quad(self,info):
        """
        Find the width, height and bottom left corner for a quad to texture map
        to display a full photo image.
        """
        if info['orient'] < 5: # Horizontal
            xpos = 0
            wphoto = self.width_pixels # Use maximum width if possible.
            hphoto = float(self.photo_height)/float(self.photo_width)*wphoto
            if hphoto > self.height_pixels: # Too high. Change to maximum height.
                ypos = 0
                hphoto = self.height_pixels
                wphoto = float(self.photo_width)/float(self.photo_height)*hphoto
                xpos = int((self.width_pixels - wphoto)/2)
            else:
                ypos = int((self.height_pixels - hphoto)/2)
        else:
            ypos = 0
            hphoto = self.height_pixels # Use maximum height if possible.
            wphoto = float(self.photo_width)/float(self.photo_height)*hphoto
            if wphoto > self.width_pixels: # Too wide. Change to maximum width.
                xpos = 0
                wphoto = self.width_pixels
                hphoto = float(self.photo_height)/float(self.photo_width)*wphoto
                ypos = int((self.height_pixels - hphoto)/2)
            else:
                xpos = int((self.width_pixels - wphoto)/2)
        return (wphoto,hphoto,xpos,ypos)

    def draw_full_photo(self):
        """
        Draw the full size picture.
        """
        if self.sortedinfotable == None or len(self.sortedinfotable) == 0:
            return
        if self.selected_photo >= 0:
            info = self.sortedinfotable[self.selected_photo]
            # If it is not the same as the last selected photo,
            # read the new full image.
            if (self.selected_photo != self.last_selected_photo) or \
                    (self.disp_mode != self.old_disp_mode) or \
                    self.reread_image:
                self.reread_image = False
                photosdir = 'photos'
                photoname = photohack.make_time_file_name(info,'P')
                photopath = os.path.join(photosdir,photoname)
                if os.access( photopath, os.F_OK ):
                    if self.debuglevel > 1:
                        print('draw_full_photo(): Photopath=',photopath)
                    (self.photo_width,self.photo_height) = \
                        self.make_image_texture(photopath,self.photo_texture,info['orient'],True)
                    self.last_selected_photo = self.selected_photo
            # Background rectangle
            glColor4f(0.5,0.5,0.5,1.0)
            glBegin(GL_QUADS)
            glVertex2f(0.0,0.0)
            glVertex2f(self.width_pixels,0.0)
            glVertex2f(self.width_pixels,self.height_pixels)
            glVertex2f(0.0,self.height_pixels)
            glEnd()
            # Draw the photo centered in the window.
            # Make sure it is all visible regardless of display/photo aspect ratio mismatches.
            wphoto,hphoto,xpos,ypos = self.find_full_image_quad(info)
            self.draw_image_full(self.photo_texture,wphoto,hphoto,info['orient'])

    def paintGL(self):
        """
        Draw the visualization.
        """
        # Start by clearing the screen.
        if self.havefocus:
            if self.view_image_select == VIEW_PICK:
                glClearColor(0.6,0.8,0.6,1.0)
            elif self.view_image_select == VIEW_UNPICK:
                glClearColor(0.6,0.6,0.8,1.0)
            else:
                glClearColor(0.8,0.8,0.8,1.0)
        else:
            if self.view_image_select == VIEW_PICK:
                glClearColor(0.3,0.4,0.3,1.0)
            elif self.view_image_select == VIEW_UNPICK:
                glClearColor(0.3,0.3,0.4,1.0)
            else:
                glClearColor(0.4,0.4,0.4,1.0)
        # There is an error on clear when changing to and from full screen. Ignore it.
        try:
            glClear(GL_COLOR_BUFFER_BIT)
        except:
            return
        # Deal with informational display first.
        if self.disp_mode == INFO_DISPLAY:
            glColor4f(0.0,0.0,0.0,1.0)
            ypos = self.height_pixels // 2
            xpos = self.width_pixels // 2 
            self.draw_string_cent((xpos,ypos),self.info_message)
            glFlush()
            return
        # Unless viewing full res(ish) photo, draw the time chart.
        if self.disp_mode != PHOTO_ONLY:
            if self.month_scale > 4:
                self.draw_day_verticals()
            elif self.month_scale >= 2:
                self.draw_weekish_verticals()
            self.draw_now_patch()
            self.draw_month_verticals()
            self.draw_year_horizontals()
            glBindTexture(GL_TEXTURE_2D,self.texture)
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            self.draw_months(25)
            self.draw_months(self.height_pixels+5)
            self.draw_years(datetime.datetime.now().year - self.year_offset)
            glDisable(GL_BLEND)
            glDisable(GL_TEXTURE_2D)
            self.plot_photodb()
            if self.draw_sel_box:
                self.draw_box()
            self.draw_whenstring()
            glColor4f(0.1,0.1,0.3,1.0) # Dark blue
            self.draw_string((3,self.height_pixels-5),'Selected')
            self.draw_string((3,self.height_pixels-5-self.linespace),
                             '{0}'.format(self.count_selected(self.sortedinfotable)))
            if self.view_image_select == VIEW_PICK:
                self.draw_string((3,self.height_pixels-5-2*self.linespace),'Pick +')
                self.draw_string((3,self.height_pixels-5-3*self.linespace),
                                 '{0}'.format(len(self.pickedset)))
            elif self.view_image_select == VIEW_UNPICK:
                self.draw_string((3,self.height_pixels-5-2*self.linespace),'Pick -')
                self.draw_string((3,self.height_pixels-5-3*self.linespace),
                                 '{0}'.format(len(self.pickedset)))
            else:
                self.draw_string((3,self.height_pixels-5-2*self.linespace),'Picked')
                self.draw_string((3,self.height_pixels-5-3*self.linespace),
                                 '{0}'.format(len(self.pickedset)))
            self.draw_string((3,self.height_pixels-5-7*self.linespace),'Deleted')
            self.draw_string((3,self.height_pixels-5-8*self.linespace),
                             '{0}'.format(len(self.deletedtable)))
            # Draw a minimal thumb rectangle (which is insensitive to selecting photos) when there
            # is no thumbnail display as such.
            if self.disp_mode != TIME_THUMB:
                self.thumb_rect = (0.0,0.0,20.0,20.0)
                glColor4f(0.5,0.9,0.5,1.0)
                glBegin(GL_QUADS)
                glVertex2f(self.thumb_rect[0],self.thumb_rect[1])
                glVertex2f(self.thumb_rect[2],self.thumb_rect[1])
                glVertex2f(self.thumb_rect[2],self.thumb_rect[3])
                glVertex2f(self.thumb_rect[0],self.thumb_rect[3])
                glEnd()
        # Maybe draw thumbnail with information of the full res photo.
        if self.disp_mode == TIME_THUMB:
            self.draw_photo()
        elif self.disp_mode == PHOTO_ONLY:
            self.draw_full_photo()
            if self.draw_sel_box:
                self.draw_pbox()
        # Record current disp_mode as old disp_mode.
        self.old_disp_mode = self.disp_mode
        glFlush()

    def resizeGL(self, w, h):
        """
        Handle widget resizes.
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, 0, h, -50.0, 50.0)
        glViewport(0, 0, w, h)
        self.viewport = (w,h)
        self.width_pixels = w
        self.height_pixels = h
        self.aspect = float(self.width_pixels) / float(self.height_pixels)
        
    def initializeGL(self):
        """
        Initialize OpenGL for our task.
        """
        # Make an *alpha* texture from the *luminance* image data.
        img_data = numpy.asarray(self.imgl,dtype=numpy.uint8)
        self.texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glBindTexture(GL_TEXTURE_2D,self.texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP )
        # Generate textures. 
        # Nearest neighbour minification sampling with a carefully pre-scaled texture.
        # This seems to give *by far* the best results for text drawing (perhaps not surprisingly).
        glTexImage2D(GL_TEXTURE_2D, 0, GL_ALPHA, self.imgl.size[0], self.imgl.size[1], \
                         0, GL_ALPHA, GL_UNSIGNED_BYTE, img_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
        # You *must* turn on blending to get the desired result with the texture BTW!
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
        # For image display
        self.photo_texture = glGenTextures(1)
        # Flat shading please.
        glShadeModel(GL_FLAT)

    def focusInEvent(self,event):
        """
        Handle gain of focus.
        """
        if self.debuglevel > 2:
            print('@@@ got focus')
        self.havefocus = True
        self.update()

    def focusOutEvent(self,event):
        """
        Handle loss of focus.
        """
        if self.debuglevel > 2:
            print('@@@ lost focus')
        self.havefocus = False
        self.update()

    def in_thumb_region(self,x,y):
        """
        See if raw mouse position (x,y) is in the thumb region.
        """
        y = self.height_pixels - y
        return(x >= self.thumb_rect[0] and x <= self.thumb_rect[2] and y >= self.thumb_rect[1] and y <= self.thumb_rect[3])

    def mousePressEvent(self,mouseEvent):
        """
        Mouse button press handler.
        """
        if self.debuglevel > 0:
            print('Mouse press. Pos=({0},{1})'.format(int(mouseEvent.position().x()),int(mouseEvent.position().y())))
        # If in the thumb region, do nothing. Unless in PHOTO_ONLY!
        if self.disp_mode != PHOTO_ONLY:
            if self.in_thumb_region(int(mouseEvent.position().x()),int(mouseEvent.position().y())):
                return
        # Record position.
        self.oldmouse_x = int(mouseEvent.position().x())
        self.oldmouse_y = int(mouseEvent.position().y())
        # Time chart, maybe with thumb.
        if self.disp_mode != PHOTO_ONLY:
            self.cur_month = self.start_month = self.end_month = self.xpos_to_month(self.oldmouse_x)
            self.cur_year = self.start_year = self.end_year = self.ypos_to_year(self.oldmouse_y)
            ut = self.current_position_to_unix_time()
            self.selected_photo = self.find_nearest_photo(ut)
            if self.debuglevel > 2:
                print('Month =',self.xpos_to_month(self.oldmouse_x))
                print('Back to x =',self.month_to_xpos(self.xpos_to_month(self.oldmouse_x)))
                print('Year =',self.ypos_to_year(self.oldmouse_y))
                print('Back to y =',self.year_to_ypos(self.ypos_to_year(self.oldmouse_y)))
            self.valid_when = True
        # Full photo.
        else:
            self.pbox_cur_x = self.pbox_start_x = self.oldmouse_x
            self.pbox_cur_y = self.pbox_start_y = self.oldmouse_y
            self.panning = (self.ctrl and self.alt) or (mouseEvent.buttons() == Qt.MiddleButton)
            if self.debuglevel > 2:
                print('panning, havefocus:', self.panning, self.havefocus)
            if self.panning:
                if self.havefocus:
                    QApplication.setOverrideCursor(QCursor(Qt.OpenHandCursor))
                self.zoom_tx_start = self.zoom_tx
                self.zoom_ty_start = self.zoom_ty
        self.draw_sel_box = False
        self.update()

    def mouseReleaseEvent(self,mouseEvent):
        """
        Mouse button release handler.
        """
        if self.debuglevel > 0:
            print('Mouse release. Pos=({0},{1})'.format(int(mouseEvent.position().x()),int(mouseEvent.position().y())))
        # If in the thumb region, do nothing. Unless in PHOTO_ONLY!
        if self.disp_mode != PHOTO_ONLY:
            if self.in_thumb_region(int(mouseEvent.position().x()),int(mouseEvent.position().y())):
                return
        self.oldmouse_x = int(mouseEvent.position().x())
        self.oldmouse_y = int(mouseEvent.position().y())
        # Time selection mode.
        if self.disp_mode != PHOTO_ONLY:
            self.cur_month = self.end_month = self.xpos_to_month(self.oldmouse_x)
            self.cur_year = self.end_year = self.ypos_to_year(self.oldmouse_y)
            if self.debuglevel > 0:
                print('Selected: ({0},{1}) -> ({2},{3})'.format(self.start_month,self.start_year,
                                                                self.end_month,self.end_year))
            if self.user is not None:
                self.user.time_box_handler(self.makewhenboxstring())
        # Photo display mode.
        else:
            self.pbox_cur_x = self.pbox_end_x = self.oldmouse_x
            self.pbox_cur_y = self.pbox_end_y = self.oldmouse_y
            self.have_zoom_box = True
            if self.panning:
                if self.havefocus:
                    QApplication.restoreOverrideCursor()
        self.update()

    def mouseDoubleClickEvent(self,mouseEvent):
        """
        Mouse button double-click handler.
        """
        if self.debuglevel > 0:
            print('Mouse double click.')

    def wheelEvent(self,wheelEvent):
        """
        Mouse wheel event handler.
        """
        if wheelEvent.angleDelta().y() < 0:
            self.zoom_zoom(-1)
        else:
            self.zoom_zoom(1)
        self.update()

    def mouseMoveEvent(self,mouseEvent):
        """
        Mouse movement handler.
        """
        # If in the thumb region, do nothing. Unless in PHOTO_ONLY!
        if self.disp_mode != PHOTO_ONLY:
            if self.in_thumb_region(int(mouseEvent.position().x()),int(mouseEvent.position().y())):
                return
        if self.disp_mode != PHOTO_ONLY:
            self.cur_month = self.xpos_to_month(int(mouseEvent.position().x()))
            self.cur_year = self.ypos_to_year(int(mouseEvent.position().y()))
        else:
            self.pbox_cur_x = int(mouseEvent.position().x())
            self.pbox_cur_y = int(mouseEvent.position().y())
        mousebuttons = mouseEvent.buttons()
        if mousebuttons != Qt.NoButton:
            if self.disp_mode != PHOTO_ONLY:
                self.end_month = self.cur_month
                self.end_year = self.cur_year
            else:
                self.pbox_end_x = self.pbox_cur_x
                self.pbox_end_y = self.pbox_cur_y
                if self.panning:
                    info = self.sortedinfotable[self.selected_photo]
                    qwidth,qheight,xpos,ypos = self.find_full_image_quad(info)
                    xn_start,yn_start = self.window_to_norm_image(self.pbox_start_x,self.height_pixels-self.pbox_start_y,qwidth,qheight)
                    xn_cur,yn_cur = self.window_to_norm_image(self.pbox_cur_x,self.height_pixels-self.pbox_cur_y,qwidth,qheight)
                    self.zoom_tx = self.zoom_tx_start + ( xn_start - xn_cur )
                    self.zoom_ty = self.zoom_ty_start + ( yn_start - yn_cur )
            if (mousebuttons == Qt.RightButton) or ((self.ctrl and not self.alt) and (mousebuttons != Qt.MiddleButton)):
                self.draw_sel_box = True
            self.update()
            delta_x = int(mouseEvent.position().x()) - self.oldmouse_x
            delta_y = self.oldmouse_y - int(mouseEvent.position().y())
            if self.debuglevel > 0:
                print('Mouse drag. Delta=({0},{1})'.format(delta_x,delta_y))
        self.oldmouse_x = int(mouseEvent.position().x())
        self.oldmouse_y = int(mouseEvent.position().y())

    def keyPressEvent(self,event):
        """
        Handle the keyboard - key presses.
        """
        keynum = event.key()
        if self.debuglevel > 0:
            print('KeyPress',keynum,event.text())
        # Look for modifier keys first.
        if keynum == Qt.Key_Control:
            self.ctrl = True
        elif keynum == Qt.Key_Shift:
            self.shift = True
        elif keynum == Qt.Key_Alt or keynum == Qt.Key_AltGr:
            self.alt = True

    def keyReleaseEvent(self,event):
        """
        Handle the keyboard - key releases.
        """
        keynum = event.key()
        if self.debuglevel > 1:
            print('KeyRelease',keynum,event.text())
        # Turn off modifiers on modifier key release.
        if keynum == Qt.Key_Control:
            self.ctrl = False
        elif keynum == Qt.Key_Shift:
            self.shift = False
        elif keynum == Qt.Key_Alt or keynum == Qt.Key_AltGr:
            self.alt = False

    def move_zoom(self,mdx,mdy):
        """
        If there is a zoom box and we are zoomed, move the zoom box up/down/left/right.
        By a suitable increment. Called for arrow keys in PHOTO_ONLY mode.
        """
        speed = 0.1 / self.zoom_scale
        self.zoom_tx += speed * mdx
        self.zoom_ty += speed * mdy
        if self.debuglevel > 1:
            print('move_zoom():',self.zoom_tx,self.zoom_ty)

    def zoom_zoom(self,zdir):
        """
        If there is a zoom box and we are zoomed, zoom in or out by a suitable
        increment. Called for + and - keys.
        """
        scale = 0.95
        if zdir > 0:
            scale = 1.0 / scale
        self.zoom_scale *= scale

    def zoom_one(self):
        """
        Display the image so that one display pixel corresponds to one image pixel.
        """
        # Use a zoom based on the ratio of the full image height to the display quad height.
        if self.selected_photo >= 0:
            info = self.sortedinfotable[self.selected_photo]
            wphoto,hphoto,xpos,ypos = self.find_full_image_quad(info)
            self.zoom_scale = float(self.photo_height) / float(hphoto)
            self.do_zoom = True
            # Kill any measurement graphic.
            self.measuring = False

    def default_zoom_box(self):
        """
        If there is no zoom box, make one for the whole image.
        If there is a whole iimage.
        """
        if not self.have_zoom_box:
            if self.selected_photo >= 0:
                info = self.sortedinfotable[self.selected_photo]
                wphoto,hphoto,xpos,ypos = self.find_full_image_quad(info)
                if self.debuglevel > 1:
                    print('default_zoom_box(): xpos =',xpos,'ypos =',ypos,'w =',wphoto,'h =',hphoto)
                self.pbox_start_x = xpos
                self.pbox_end_x = xpos + wphoto
                self.pbox_start_y = ypos + hphoto
                self.pbox_end_y = ypos
                self.have_zoom_box = True

    def points_size(self,pdir):
        """
        Increment or decrement the time plot point size.
        """
        self.point_size += pdir
        if self.point_size < 2:
            self.point_size = 2
        elif self.point_size > 100:
            self.point_size = 100

    def maintain_picked_set(self,selected_photo,add):
        """
        Add or remove selected_photo to/from the picked set.
        """
        if add:
            if not (self.selected_photo in self.pickedset):
                self.pickedset.append(self.selected_photo)
        else:
            if self.selected_photo in self.pickedset:
                self.pickedset.remove(self.selected_photo)

    def pick_to_selected(self,action):
        """
        Add pick to selection (1), remove pick from selection (2), make pick the selection (3).
        """
        if action == 0:
            photohack.unselect_all(self.sortedinfotable)
        if action == 1 or action == 0:
            for ipick in range(0,len(self.pickedset)):
                self.sortedinfotable[self.pickedset[ipick]]['selected'] = True
        elif action == -1:
            for ipick in range(0,len(self.pickedset)):
                self.sortedinfotable[self.pickedset[ipick]]['selected'] = False

    def picked_set_clear(self):
        """
        Clear the picked set.
        """
        self.pickedset = []

    def move_to_next_selected_photo(self,direction):
        """
        Move to the next or previous photo in the selected group.
        Handle picked set maintenance too.
        """
        if self.selected_photo >= 0:
            if self.view_image_select == VIEW_PICK:
                self.selected_photo = \
                    photohack.next_index(self.sortedinfotable,self.selected_photo,direction)
                self.maintain_picked_set(self.selected_photo,True)
            elif self.view_image_select == VIEW_UNPICK:
                self.selected_photo = \
                    photohack.next_index(self.sortedinfotable,self.selected_photo,direction)
                self.maintain_picked_set(self.selected_photo,False)
            else:
                self.selected_photo = \
                    photohack.next_selected_index(self.sortedinfotable,self.selected_photo,direction)

    def has_modifier(self):
        """
        Check for hot key modifier. This is the ALT key on macOS and the CTRL key on Linux.
        """
        if self.is_macos:
            return self.alt
        else:
            return self.ctrl

    def event(self,event):
        """
        Intercept all events here to process hot keys. This may be overkill
        for this application, but it works. Almost all commands are handled by
        hotkey. WELL: not any more, really!
        """
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_D: # Debug level
                if self.has_modifier():
                    self.debuglevel -= 1
                    if self.debuglevel < 0:
                        self.debuglevel = 0
                else:
                    self.debuglevel += 1
                    if self.debuglevel > 10:
                        self.debuglevel = 10
                return True
            if key == Qt.Key_R: # Zoom reset
                self.have_zoom_box = False
                self.default_zoom_box()
                self.reset_zoom()
                self.reset_photo_zoom()
                self.do_zoom = False
                self.update()
                return True
            if key == Qt.Key_F1 or key == Qt.Key_0: # 1:1 pixel zoom.
                self.zoom_one()
                self.do_zoom = True
                self.update()
                return True
            if key == Qt.Key_Z:    # Zoom in
                self.zoom_selected()
                self.do_zoom = True
                self.update()
                return True
            if key == Qt.Key_PageDown: # Move down 5 years
                self.year_offset += 5
                self.valid_when = False
                self.update()
                return True
            if key == Qt.Key_Down: # Move down 1 year OR move zoom down
                if self.disp_mode == PHOTO_ONLY:
                    self.move_zoom(0,-1)
                else:
                    self.year_offset += 1
                    self.valid_when = False
                self.update()
                return True
            if key == Qt.Key_PageUp: # Move up 5 years
                self.year_offset -= 5
                if self.year_offset < 0:
                    self.year_offset = 0
                self.valid_when = False
                self.update()
                return True
            if key == Qt.Key_Up: # Move up 1 year OR move zoom up
                if self.disp_mode == PHOTO_ONLY:
                    self.move_zoom(0,1)
                else:
                    self.year_offset -= 1
                    if self.year_offset < 0:
                        self.year_offset = 0
                    self.valid_when = False
                self.update()
                return True
            if key == Qt.Key_Right:  # Move right one month OR move zoom right
                if self.has_modifier():         # +ALT: Next photo
                    self.move_to_next_selected_photo(1)
                else:
                    if self.disp_mode == PHOTO_ONLY:
                        self.move_zoom(1,0)
                    else:
                        self.month_offset += 1
                        self.valid_when = False
                self.update()
                return True
            if key == Qt.Key_N:  # Next photo.
                self.move_to_next_selected_photo(1)
                self.update()
                return True
            if key == Qt.Key_Left:  # Move left one month OR move zoom left
                if self.has_modifier():        # +ALT: Previous photo
                    self.move_to_next_selected_photo(-1)
                else:
                    if self.disp_mode == PHOTO_ONLY:
                        self.move_zoom(-1,0)
                    else:
                        self.month_offset -= 1
                        if self.month_offset < 0:
                            self.month_offset = 0
                        self.valid_when = False
                self.update()
                return True
            if key == Qt.Key_P:  # Previous photo.
                self.move_to_next_selected_photo(-11)
                self.update()
                return True
            if key == Qt.Key_Space:
                if self.has_modifier():
                    self.move_to_next_selected_photo(-1)
                else:
                    self.move_to_next_selected_photo(1)
                self.update()
                return True
            if key == Qt.Key_Plus: # + Zoom in, +ALT make points bigger
                if self.has_modifier():
                    self.points_size(1)
                else:
                    self.default_zoom_box()
                    self.do_zoom = True
                    self.zoom_zoom(1)
                self.update()
                return True
            if key == Qt.Key_Minus: # - Zoom out, +ALT make points smaller
                if self.has_modifier():
                    self.points_size(-1)
                else:
                    self.default_zoom_box()
                    self.do_zoom = True
                    self.zoom_zoom(-1)
                self.update()
                return True
            if key == Qt.Key_F2:
                self.parent.showFullScreen()
                return True
            if key == Qt.Key_F3:
                self.parent.showNormal()
                return True
            if key == Qt.Key_H:  # Hide photos. Show time only.
                self.disp_mode = TIME_ONLY
                self.update()
                return True
            if key == Qt.Key_T: # Show thumbail with info and time.
                self.disp_mode = TIME_THUMB
                self.update()
                return True
            if key == Qt.Key_V: # Show photo only.
                self.disp_mode = PHOTO_ONLY
                self.update()
                return True
            if key == Qt.Key_B: # Toggle isolated point BIG display
                self.draw_big = not self.draw_big
                self.update()
                return True

            # *** OBSOLETE HOT KEYS ***
            if False:            
                if key == Qt.Key_B: # Start adding viewed pictures to picked.
                    if self.has_modifier():    # +ALT: Add pick to selected.
                        self.pick_to_selected(1)
                    else:
                        self.view_image_select = VIEW_PICK
                        self.maintain_picked_set(self.selected_photo,True)
                    self.update()
                    return True
                if key == Qt.Key_U: # Start removing viewed pictures from picked.
                    if self.has_modifier():    # +ALT: Remove pick from selected.
                        self.pick_to_selected(-1)
                    else:
                        self.view_image_select = VIEW_UNPICK
                        self.maintain_picked_set(self.selected_photo,False)
                    self.update()
                    return True
                if key == Qt.Key_E: # End adding viewed pictures to picked.
                    if self.has_modifier():    # +ALT: Make selected the pick. End picking.
                        self.pick_to_selected(0)
                    else:
                        if self.view_image_select == VIEW_PICK: # Almost certainly do not want this one!
                            self.maintain_picked_set(self.selected_photo,False)
                    self.view_image_select = VIEW_NOPICK
                    self.update()
                    return True
                if key == Qt.Key_C: # Clear pick set.
                    if self.has_modifier():    # +ALT: deleted all files in default "saved" and "saved_raws" folders.
                        for savedphoto in photohack.all_files( 'saved', '*.jpg', True, False ):
                            photohack.delete_file_if_exists( savedphoto )
                        for savedraw in photohack.all_files( 'saved_raws', '*.*', True, False ):
                            photohack.delete_file_if_exists( savedraw )
                    else:
                        self.pickedset = []
                        self.view_image_select = VIEW_NOPICK
                    self.update()
                    return True
                if key == Qt.Key_A: # Select all.
                    self.make_selection(self.sortedinfotable,'Any','All',None)
                    self.view_image_select = VIEW_NOPICK
                    self.update()
                    return True
                if key == Qt.Key_N: # Add tags to the current photo.
                    if self.has_modifier():
                        self.user.tag_set_one()
                    else:
                        self.user.tag_add_one()
                    self.update()
                    return True
                if key == Qt.Key_M: # Add tags to the current photo. Then move to next photo.
                    if self.has_modifier():
                        self.user.tag_set_one()
                    else:
                        self.user.tag_add_one()
                    self.update()
                    self.move_to_next_selected_photo(1)
                    self.update()
                    return True
                if key == Qt.Key_S: # Save image to saved folder.
                    if self.has_modifier():    # +ALT: Save all picked images to saved folder
                        for i in range(0,len(self.pickedset)):
                            self.save_photo(self.pickedset[i])
                    else:
                        if self.selected_photo >= 0:
                            self.save_photo(self.selected_photo)
                    self.update()
                    return True
                if key == Qt.Key_I: # Get EXIF.
                    exifstring = self.get_exif_data(self.has_modifier())
                    print(exifstring)
                # *** END OF OBSOLETE HOT KEYS ***                
                
            # Change the orientation of the picture.
            orientkeydict = {Qt.Key_1:1,Qt.Key_2:2,Qt.Key_3:3,Qt.Key_4:4,
                             Qt.Key_5:5,Qt.Key_6:6,Qt.Key_7:7,Qt.Key_8:8}
            if key in orientkeydict:
                if self.selected_photo >= 0:
                    if self.sortedinfotable != None and len(self.sortedinfotable) != 0:
                        self.sortedinfotable[self.selected_photo]['orient'] = orientkeydict[key]
                    self.reread_image = True
                    self.update()
                return True
            if key == Qt.Key_Q or key == Qt.Key_Escape:
                self.user.close_key_handler(event)
                return True
        return super().event(event) #QOpenGLWidget.event(self,event)

    def reset_zoom(self):
        self.current_year = datetime.datetime.now().year
        self.month_offset = 0
        self.month_scale = 1
        self.year_offset = 0
        self.draw_sel_box = False
        self.update()

    def reset_photo_zoom(self):
        self.zoom_scale = 1.0
        self.zoom_tx = 0.0
        self.zoom_ty = 0.0

    def zoom_selected(self):
        if self.draw_sel_box:
            if self.disp_mode == PHOTO_ONLY:
                info = self.sortedinfotable[self.selected_photo]
                qwidth,qheight,xpos,ypos = self.find_full_image_quad(info)
                xn_start,yn_start = self.window_to_norm_image(self.pbox_start_x,self.height_pixels-self.pbox_start_y,qwidth,qheight)
                xn_end,yn_end = self.window_to_norm_image(self.pbox_end_x,self.height_pixels-self.pbox_end_y,qwidth,qheight)
                cx = 0.5 * ( xn_start + xn_end )
                cy = 0.5 * ( yn_start + yn_end )
                dx = abs( xn_end - xn_start )
                dy = abs( yn_end - yn_start )
                dz = max( dx, dy )
                self.zoom_scale = 1.0 / dz
                self.zoom_tx = cx - 0.5
                self.zoom_ty = cy - 0.5
            else:
                lo_month = min(self.start_month,self.end_month)
                hi_month = max(self.start_month,self.end_month)
                self.month_offset = lo_month - 1
                self.month_scale = 12.0 / (hi_month - lo_month + 1)
                hi_year = int(max(self.start_year,self.end_year))
                self.year_offset = self.current_year - hi_year
            self.draw_sel_box = False
            self.valid_when = False
            self.update()

    def loadCharData(self,jsonfile):
        """
        Load the locations of each character in the character texture from
        a JSON format file containing a single dictionary. I don't much like
        JSON, but it sort of works for this while being human readable.
        The single dictionary also contains character metrics.
        """
        try:
            flun = open(jsonfile,'r')
            input_dir = json.load(flun)
            flun.close()
            self.chardict = {}
            metricdict = {}
            for k in input_dir:
                try:
                    ikey = int(k)
                    self.chardict[ikey] = input_dir[k]
                except ValueError:
                    metricdict[k] = input_dir[k]
            self.scale = 1
            self.charwidth = metricdict['charwidth']
            self.charheight = metricdict['charheight']
            self.charspace = self.charwidth+1
            self.linespace = self.charheight+1
            self.cellduv = metricdict['cellduv']
            self.dsu = self.cellduv[0]
            self.dsv = self.cellduv[1]
        except Exception as e:
            print('ERROR: Failed to open or parse font data file!',jsonfile,'Giving up!')
            print('... Reason:', e)
            sys.exit(1)

    def loadCharImage(self,pngfile):
        """
        Open a PNG image file containing the character glyphs.
        """
        try:
            img = Image.open(pngfile)
            self.imgl = img.convert('L')
        except Exception as e:
            print('ERROR: Failed to open font texture image file! Giving up!')
            print('... Reason:', e)
            sys.exit(1)

    def loadCharDefinitions(self,charsetname):
        """
        Load the contents of the two files that define a character set.
        """
        if self.debuglevel > 1:
            print('Loading char data:', charsetname)
        self.loadCharData(str(charsetname)+'.jsn')
        self.loadCharImage(str(charsetname)+'.png')

    def drawTexChar(self,charcode,xpos,ypos):
        """
        Draw character ucharcode at (xpos,yos).
        """
        # Find the right texture coordinate (top left of character) in pixels.
        try:
            (u,v) = self.chardict[charcode]
        except:
            (u,v) = (0.0,0.0)
        # Draw the rectangle.
        glBegin(GL_QUADS)
        glTexCoord2f(u,v)
        glVertex2f(xpos,ypos)
        glTexCoord2f(u+self.dsu, v)
        glVertex2f(xpos+self.charwidth,ypos)
        glTexCoord2f(u+self.dsu,v+self.dsv)
        glVertex2f(xpos+self.charwidth,ypos-self.charheight)
        glTexCoord2f(u,v+self.dsv)
        glVertex2f(xpos,ypos-self.charheight)
        glEnd()

    def draw_string(self,where,string,xlimit=999999):
        """
        Draw a string at an arbitrary position. Colour is as specified previously.
        """
        xpos = int(where[0])
        ypos = int(where[1])
        glBindTexture(GL_TEXTURE_2D,self.texture)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        for i in range(0,len(string)):
            self.drawTexChar(ord(string[i]),xpos,ypos)
            xpos += self.charspace
            if xpos > xlimit:
                break
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

    def string_length(self,string):
        """
        Return the length of a string in pixels.
        """
        return len(string) * self.charspace

    def draw_string_cent(self,where,string):
        """
        Draw string centered on where.
        """
        xpos = where[0] - 0.5 * self.string_length(string)
        ypos = where[1] - 0.5 * self.charheight
        self.draw_string((xpos,ypos),string)

    def set_photodb(self,photodbname):
        """
        Load a photo database. Set all (sorted) entries as selected.
        """
        (self.dirname, self.infotable, self.hashes, self.deletedtable) = photohack.load_photo_data(photodbname)
        self.dbfolder, self.dbname = os.path.split(photodbname)
        self.dbfolder = os.getcwd()
        return self.refreshdb()

    def refreshdb(self):
        """
        Generate sorted infotable, systimes and hashes. Generate the known camera list.
        Return the number of images in the database.
        """
        num_images = len(self.hashes)
        if self.debuglevel > 1:
            print('set_photodb(): Total of',num_images,'image infos loaded.')
        if num_images == 0:
            return 0
        self.cameras = photohack.camera_list(self.infotable)
        num_cameras = len(self.cameras)
        if self.debuglevel > 1:
            print('set_photodb(): Total of',num_cameras,'camera types used.')
        self.sortedinfotable = sorted(self.infotable,key=lambda v:v['systime'])
        self.sortedsystimes = []
        self.sortedhashes = []
        for info in self.sortedinfotable:
            self.sortedsystimes.append(info['systime'])
            self.sortedhashes.append(info['hashval'])
        photohack.select_all(self.sortedinfotable)
        numsel = 0
        for info in self.sortedinfotable:
            if info['selected']:
                numsel += 1
        if self.debuglevel > 1:
            print('set_photodb(): selected',numsel,'entries after set_photodb.')            
        self.picked_set_clear()
        return num_images

    def delete_selected(self):
        """
        Move all selected photos to the deleted list.
        Refresh the database.
        """
        newinfotable, newdeletedtable = photohack.delete_selected(self.sortedinfotable, self.deletedtable)
        self.infotable = newinfotable
        self.deletedtable = newdeletedtable
        self.refreshdb()
        ut = self.current_position_to_unix_time()
        self.selected_photo = self.find_nearest_photo(ut)
        self.update()

    def undelete(self):
        """
        Move all photos on the deleted list back to the active photo list.
        """
        newinfotable, newdeletedtable = photohack.undelete(self.sortedinfotable, self.deletedtable)
        self.infotable = newinfotable
        self.deletedtable = newdeletedtable
        self.refreshdb()
        self.update()

    def save_photodb(self,photodbname):
        """
        Save a (possibly modified) photo database.
        """
        ok = photohack.save_photo_data( photodbname, self.dirname, self.sortedinfotable, self.sortedhashes, self.deletedtable)
        return ok

    def plot_photodb(self):
        """
        Draw a cluster plot for a photo database.
        """
        if self.sortedinfotable == None:
            return
        # Selected photo cross-hair.
        if (self.selected_photo >= 0) and (len(self.sortedinfotable) > 0):
          info = self.sortedinfotable[self.selected_photo]
          (x,y) = self.unix_time_to_position(info['systime'])
          #print('x:',x,' y:',y, 'year_offset:', self.year_offset)
          glColor4f(0.65,0.65,0.1,1.0)
          glBegin(GL_LINES)
          glVertex2f(x,0.0)
          glVertex2f(x,self.height_pixels)
          glVertex2f(0.0,y)
          glVertex2f(self.width_pixels,y)
          glEnd()
        # Try to find points which are widely spaced in x. Eventually plot these with larger markers.
        if self.draw_big:
            biglist = []
            dx_threshold = 50
            sitlastidx = len(self.sortedinfotable) - 1
            for i in range(0,len(self.sortedinfotable)):
                info = self.sortedinfotable[i]
                (x,y) = self.unix_time_to_position(info['systime'])
                if i > 1:
                    (xp,yp) = self.unix_time_to_position(self.sortedinfotable[i-1]['systime'])
                    dxp = abs(x - xp)
                else:
                    dxp = 0.0
                if i < sitlastidx:
                    (xn,yn) = self.unix_time_to_position(self.sortedinfotable[i+1]['systime'])
                    dxn = abs(x - xn)
                else:
                    dxn = 0.0
                dx = max(dxp,dxn)
                if dx > dx_threshold:
                    biglist.append(i)
        # Point plotting: selected in red.
        glPointSize(float(self.point_size))
        glColor4f(1.0,0.0,0.0,1.0)
        glBegin(GL_POINTS)
        for info in self.sortedinfotable:
            if info['selected']:
                (x,y) = self.unix_time_to_position(info['systime'])
                glVertex2f(x,y)
        glEnd()
        # Big selected points.
        if self.draw_big and (len(biglist) > 0):
            glPointSize(float(5*self.point_size))
            glColor4f(1.0,0.0,0.0,0.5)
            glBegin(GL_POINTS)
            for i in biglist:
                info = self.sortedinfotable[i]
                if info['selected']:
                    (x,y) = self.unix_time_to_position(info['systime'])
                    glVertex2f(x,y)
            glEnd()            
        # Point plotting: unselected in white.
        glPointSize(float(self.point_size))
        glColor4f(1.0,1.0,1.0,1.0)
        glBegin(GL_POINTS)
        for info in self.sortedinfotable:
            if not info['selected']:
                (x,y) = self.unix_time_to_position(info['systime'])
                glVertex2f(x,y)
        glEnd()
        # Big unselected points.
        if self.draw_big and (len(biglist) > 0):
            glPointSize(float(5*self.point_size))
            glColor4f(1.0,1.0,1.0,0.5)
            glBegin(GL_POINTS)
            for i in biglist:
                info = self.sortedinfotable[i]
                if not info['selected']:
                    (x,y) = self.unix_time_to_position(info['systime'])
                    glVertex2f(x,y)
            glEnd()  

    def info_display(self,msg):
        """
        Switch display to an informational message.
        """
        self.info_message = msg
        if self.disp_mode != INFO_DISPLAY:
            self.saved_disp_mode = self.disp_mode
        self.disp_mode = INFO_DISPLAY
        self.update()
        QApplication.processEvents()

    def normal_display(self):
        """
        Switch display back to what it used to be.
        """
        self.disp_mode = self.saved_disp_mode
        self.update()
        QApplication.processEvents()

    def add_disp_callback(self,numproc):
        """
        Show progress on locating photographs.
        """
        if (numproc%20) == 0:
            self.info_display('Found {0} photos so far.'.format(numproc))

    def thumbs_disp_callback(self,numproc,num_images):
        """
        Show progress on creating thumbnails for photographs.
        """
        if (numproc%20) == 0:
            self.info_display('Generated {0} thumbnails so far.'.format(numproc))

    def full_disp_callback(self,numproc,num_images):
        """
        Show progress on copying full resolution photographs.
        """
        if (numproc%20) == 0:
            self.info_display('Copied {0} full images so far.'.format(numproc))

    def raw_disp_callback(self,numproc,num_images):
        """
        Show progress on copying associated RAW files.
        """
        if (numproc%20) == 0:
            self.info_display('Copied {0} associated RAW files so far.'.format(numproc))            

    def add_photos_to_photodb(self,path,doingprocessed=False,
                              taglist=None, maker=None, model=None, unixtime=None):
        """
        Add new photos to the database (in memory) from the photos in the path
        source directory. Generate the 'photos' and 'thumbnails' directory contents
        (or add to them) for this new set of photos.
        """
        self.info_display('Finding photographs and adding to database')
        errors, added, hwm = photohack.add_photos(path,
                                                  self.infotable,
                                                  self.hashes,
                                                  False,
                                                  self.add_disp_callback,
                                                  doingprocessed=doingprocessed,
                                                  taglist=taglist,
                                                  maker=maker,
                                                  model=model,
                                                  unixtime=unixtime)
        self.normal_display()
        num_images = len(self.hashes)
        if self.debuglevel > 1:
            print('add_photos_to_photodb(): Total of',num_images,'image infos loaded.')
        if num_images == 0:
            return 0
        self.info_display('Creating thumbnails for new photographs')
        photohack.create_thumbnails(self.infotable,'thumbnails',callback=self.thumbs_disp_callback,userarg=num_images,hwm=hwm)
        self.info_display('Storing standard named images for new photographs')
        photohack.create_images(self.infotable,'photos',callback=self.full_disp_callback,userarg=num_images,hwm=hwm)
        self.info_display('Storing associated RAW files for new photographs')
        photohack.create_raws(self.infotable,'raws',callback=self.raw_disp_callback,userarg=num_images,hwm=hwm)
        self.normal_display()        
        self.sortedinfotable = sorted(self.infotable,key=lambda v:v['systime'])
        self.sortedsystimes = []
        self.sortedhashes = []
        for info in self.sortedinfotable:
            self.sortedsystimes.append(info['systime'])
            self.sortedhashes.append(info['hashval'])
        return num_images

    def find_nearest_time_index(self,searchsystimes,unixtime,force_dir=0):
        """
        Find the index of an entry in a sorted list of times, searchsystimes,
        closest to unixtime.
        """
        index_next = min(len(searchsystimes)-1,bisect.bisect_left(searchsystimes,unixtime))
        index_prev = max(index_next-1,0)
        if force_dir == -1:
            return index_prev
        if force_dir == 1:
            return index_next
        dist_next = abs(searchsystimes[index_next]-unixtime)
        dist_prev = abs(unixtime-searchsystimes[index_prev])
        if dist_prev < dist_next:
            index = index_prev
        else:
            index = index_next
        return index
            
    def find_nearest_photo(self,unixtime):
        """
        Find the photo nearest to time unixtime.
        """
        # Ensure we have a non-empty sortedsystimes list.
        if self.sortedsystimes == None or len(self.sortedsystimes) == 0:
            return 0
        # If there is a sub selection, search for the nearest time in the sub selection only.
        if self.subselect:
            if len(self.sub_sortedsystimes) == 0:
                return 0
            searchsystimes = self.sub_sortedsystimes
        else:
            searchsystimes = self.sortedsystimes
        # Search for the nearest time.
        index = self.find_nearest_time_index(searchsystimes,unixtime)
        # If located in a sub selection, use the selected time to find the matching index
        # in the full table (by fast search, since it is all sorted). This *assumes* that
        # every photo has a unique systime.
        if self.subselect:
            seltime = searchsystimes[index]
            index = self.find_nearest_time_index(self.sortedsystimes,seltime)
        return index

    def select_all(self):
        """
        Select all photographs.
        """
        photohack.select_all(self.sortedinfotable)
        self.subselect = False

    def make_selection(self,infotable,camera,exif,tags):
        """
        Set the selected flags in infotable's entries according to camera (string),
        exif (string) and tags (array of strings) criteria.
        """
        if self.debuglevel > 1:
            print('make_selection(): Selecting!')
        if camera == None and exif == None and tags == None:
            return
        photohack.select_all(infotable)
        self.subselect = False
        if self.debuglevel > 1:
            print('...',camera,'...',exif,'... all selected?',self.count_selected(infotable))
            print('... tags =',tags)
        # Disqualify if camera name does not match.
        if camera != None:
            if len(camera) > 0 and camera != 'Any':
                if self.debuglevel > 1:
                    print('NOT Any')
                for i in range(0,len(infotable)):
                    camera_name = photohack.camera_full_name(infotable[i])
                    if camera_name != camera:
                        infotable[i]['selected'] = False
                self.subselect = True
        # Disqualify if Exif status does not match.
        if exif != None:
            if len(exif) > 0 and exif != 'All':
                if self.debuglevel > 1:
                    print('NOT All')
                if exif == "EXIF only":
                    exif_crit = True
                else:
                    exif_crit = False
                for i in range(0,len(infotable)):
                    if infotable[i]['exif'] != exif_crit:
                        infotable[i]['selected'] = False
                self.subselect = True
        # Disqualify any which do not contain some member of tags.
        if tags != None:
            if len(tags) > 0:
                onetags = tags.split()
                if self.debuglevel > 1:
                    print(onetags)
                for i in range(0,len(infotable)):
                    foundtag = False
                    if len(infotable[i]['tags']) > 0:
                        if self.debuglevel > 1:
                            print(infotable[i]['tags'])
                        for onetag in onetags:
                            if onetag in infotable[i]['tags']:
                                foundtag = True
                                break
                    if not foundtag:
                        infotable[i]['selected'] = False
                        self.subselect = True
        # If a subset was selected, build an array of selected (sorted) systimes.
        if self.subselect:
            self.sub_sortedsystimes = []
            for i in range(0,len(infotable)):
                if infotable[i]['selected']:
                    self.sub_sortedsystimes.append(self.sortedsystimes[i])

    def unselect_by_time(self,starttime,endtime):
        """
        Unselect anything outside time range: starttime:endtime.
        """
        photohack.unselect_by_time_range(self.sortedinfotable, starttime, endtime)
        self.subselect = True
        self.sub_sortedsystimes = []
        for i in range(0,len(self.sortedinfotable)):
            if self.sortedinfotable[i]['selected']:
                self.sub_sortedsystimes.append(self.sortedsystimes[i])

    def count_selected(self,table):
        """
        Count number of selected photos. Very inefficiently.
        """
        n = 0
        for info in table:
            if info['selected']:
                n += 1
        return n

    def add_a_tag(self,onetag,all_sel):
        """
        Add tag onetag to all selected photos. Or to the current photo (if any).
        """
        if all_sel:
            for info in self.sortedinfotable:
                if info['selected']:
                    photohack.add_tag(info,onetag)
        else:
            if self.selected_photo >= 0:
                photohack.add_tag(self.sortedinfotable[self.selected_photo],onetag)

    def remove_a_tag(self,onetag,all_sel):
        """
        Remove tag onetag from all selected photos. Or to the current photo (if any).
        """
        if all_sel:
            for info in self.sortedinfotable:
                if info['selected']:
                    photohack.remove_tag(info,onetag)
        else:
            if self.selected_photo >= 0:
                photohack.remove_tag(self.sortedinfotable[self.selected_photo],onetag)

    def remove_all_tags(self,all_sel):
        """
        Remove all tags from selected photos. Or the current photo (if any).
        """
        if all_sel:
            for info in self.sortedinfotable:
                if info['selected']:
                    photohack.remove_all_tags(info)
        else:
            if self.selected_photo >= 0:
                photohack.remove_all_tags(self.sortedinfotable[self.selected_photo])

    def trust_orientation(self,info,never_trust):
        """
        If the image is not orientation 1 and it is not on a list of
        trusted cameras that know their orientation, return False. Else True.
        If never_trust, trust nothing!
        """
        if info['orient'] == 1:
            return True
        if never_trust:
            return False
        trusted_cameras = ['SONY DSC-T20','Apple']
        camera_name = photohack.camera_full_name(info)
        trust = False
        for trusted in trusted_cameras:
            if camera_name.find(trusted) >= 0:
                trust = True
                break
        return trust

    def copy_fix_orientation(self,info,inpath,outpath):
        """
        Assuming that the image is horizontal but has been manually set to be
        vertical, read inpath and flip it to the right vertical orientation.
        Then write the result to outpath.
        """
        inimage = Image.open(inpath)
        if info['orient'] == 6:
            fixedimage = inimage.transpose(Image.ROTATE_270)
        elif info['orient'] == 8:
            fixedimage = inimage.transpose(Image.ROTATE_90)
        else: # More possibilities. Not sure what exactly yet.
            fixedimage = inimage.transpose(Image.ROTATE_90)
        fixedimage.save(outpath)

    def save_photo(self,photoindex):
        """
        Save photo to the 'saved' folder.
        Also save the RAW version (if any) to the 'saved_raws' folder.
        """
        if self.debuglevel > 1:
            print('outjpegpath =',self.outjpegpath)
            print('outrawpath =',self.outrawpath)
        filename = photohack.make_time_file_name(self.sortedinfotable[photoindex],'P')
        inpath = os.path.join('photos',filename)
        if self.outjpegpath is not None:
            if not photohack.create_folder_if_not_exists( self.outjpegpath ):
                QMessageBox.warning(self, 'Save JPEG image', 'Cannot create output folder {0}.'.format(self.outjpegpath), 
                                    QMessageBox.Ok, QMessageBox.Ok)
                return
            outpath = os.path.join(self.outjpegpath,filename)
        else:
            photohack.create_folder_if_not_exists( 'saved' )
            outpath = os.path.join('saved',filename)

        #if self.debuglevel > 1:
        print('Exporting JPEG image to:',outpath)
        
        if self.trust_orientation(self.sortedinfotable[photoindex],self.dont_trust_orient):
            try:
                shutil.copy2(inpath,outpath)
            except Exception as e:
                print('ERROR: Failed to copy JPEG image:',e)
                QMessageBox.warning(self, 'Save JPEG image', 'Failed to copy image.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.copy_fix_orientation(self.sortedinfotable[photoindex],inpath,outpath)
            
        if 'rawfilename' in self.sortedinfotable[photoindex]:
            rawfilename, inpath = photohack.construct_raw_file_path(self.sortedinfotable[photoindex])
            if self.outrawpath is not None:
                if not photohack.create_folder_if_not_exists( self.outrawpath ):
                    QMessageBox.warning(self, 'Save RAW image', 'Cannot create output folder {0}.'.format(self.outrawpath), 
                                        QMessageBox.Ok, QMessageBox.Ok)
                    return
                outpath = os.path.join(self.outrawpath,rawfilename)
            else:
                photohack.create_folder_if_not_exists( 'saved_raws' )
                outpath = os.path.join('saved_raws',rawfilename)
                
            #if self.debuglevel > 1:
            print('Exporting RAW image to:',outpath)
                
            try:
                shutil.copy2(inpath,outpath)
            except Exception as e:
                print('ERROR: Failed to  copy RAW image:',e)
                QMessageBox.warning(self, 'Save RAW image', 'Failed to copy image.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
            
    def open_google_maps_at_location(self,info):
        """
        Open Google Maps at the location of info (if it has one).
        If not, just silently return.
        """
        if info['geotags']:
            url = 'https://maps.google.com/maps?q={0},{1}'.format(info['lat'],info['long'])
            webbrowser.open(url)
            return True
        else:
            return False

    def google_maps(self):
        """
        If the currently selected photo has geo location data, try to open Google Maps
        at that location.
        """
        if self.selected_photo >= 0:
            self.open_google_maps_at_location(self.sortedinfotable[self.selected_photo])

    def get_exif_data(self,getraw=False):
        """
        Get all EXIF information for the current JPEG or RAW image.
        """
        if self.selected_photo >= 0:
            info = self.sortedinfotable[self.selected_photo]

            infostring  = 'Date/Time taken: {0} (unspecified time zone)\n'.format( info['date'] )
            infostring += 'Width: {0} pixels.\n'.format(info['width'])
            infostring += 'Height: {0} lines.\n'.format(info['height'])
            infostring += 'Orientation code: {0}\n'.format(info['orient'])
            infostring += 'Camera maker: {0}\n'.format(info['maker'])
            infostring += 'Camera model: {0}\n'.format(info['model'])
            if info['geotags']:
                infostring += 'Latitude: {0} degrees.\n'.format(info['lat'])
                infostring += 'Longitude: {0} degrees.\n'.format(info['long'])
                infostring += 'Altitude: {0} metres.\n'.format(info['alt'])
            else:
                infostring += 'Location: unknown.\n'
            if 'rawfilename' in info:
                infostring += 'Has RAW file.\n'
            else:
                infostring += 'No RAW file.\n'
            if 'processor' in info:
                infostring += 'Processed by: {0}\n'.format(info['processor'])
                infostring += 'Processed file created/modified at: {0} GMT\n'.format(photohack.time_to_exif(info['whenprocessed']))
            else:
                infostring += 'Camera direct (no post-processing).\n'
            if len(info['tags']) > 0:
                infostring += '{0} tags defined.\n'.format(len(info['tags']))
                sorted_tags = sorted( info['tags'],  key=str.casefold)
                for sorted_tag in sorted_tags:
                    infostring += '... tag: {0}\n'.format(sorted_tag)
            else:
                infostring += 'No tags defined.\n'
            infostring += '\n'
                
            if getraw:
                if 'rawfilename' in info:
                    junk_stem,raw_ext = os.path.splitext(info['rawfilename'])
                    photoname = photohack.make_time_file_name(info,'R',inext=raw_ext)
                    photosdir = 'raws'
                else:
                    return 'No RAW file exists for this image.'
            else:
                photosdir = 'photos'
                photoname = photohack.make_time_file_name(info,'P')
                
            photopath = os.path.join(photosdir,photoname)
            cmd = ['exiftool',photopath]
            try:
                retstring = subprocess.check_output(cmd, universal_newlines=True)
                return (infostring + retstring)
            except Exception as e:
                print( 'ERROR: Failed to get EXIF:',e)
                return 'Failed to extract EXIF information.'
        else:
            return 'No photograph selected.'

if __name__ == '__main__':

    class DropLineEdit(QLineEdit):
        """
        Customized LineEdit which allows drag and drop of files and directories on it.
        """
        def __init__(self, parent=None,callback=None):
            super(DropLineEdit, self).__init__(parent)
            self.setAcceptDrops(True)
            self.setPlaceholderText("Drag/drop/type file/dir here.")
            self.callback = callback

        def dragEnterEvent(self, event):
            if event.mimeData().hasUrls or event.mimeData().hasText():
                event.accept()
            else:
                event.ignore()

        def dragMoveEvent(self, event):
            if event.mimeData().hasUrls:
                event.setDropAction(Qt.CopyAction)
                event.accept()
            else:
                event.ignore()

        def dropEvent(self, event):
            if event.mimeData().hasUrls:
                event.setDropAction(Qt.CopyAction)
                event.accept()

                for url in event.mimeData().urls():
                    path = os.path.normpath(str(url.toLocalFile()))
                    if self.callback is not None:
                        self.callback(path)

            elif mime_data.hasText():
                self.setText(mime_data.text())
                event.accept()

            else:
                event.ignore()

    class ExtendedLoadDialog(QDialog):
        """
        Dialog to set items for extended load of new photos.
        """
        def __init__(self, parent = None):
            super(ExtendedLoadDialog, self).__init__(parent)
            layout = QVBoxLayout(self)

            # Nice widget for editing the date
            date_layout = QHBoxLayout()
            self.datetime = QDateTimeEdit(self)
            self.datetime.setCalendarPopup(True)
            self.datetime.setDateTime(QDateTime.currentDateTime())
            self.datetime.setToolTip('Date and time to use for these images. Overrides Exif value if Set on.')
            date_layout.addWidget(self.datetime)
            set_label = QLabel('Set:')
            date_layout.addWidget(set_label)
            self.set_checkbox = QCheckBox()
            self.set_checkbox.setToolTip('Set the date. Otherwise, keep Exif date and time (if any).')
            date_layout.addWidget(self.set_checkbox)
            layout.addLayout(date_layout)
            
            # Text edits for tags and camera.
            camera_layout = QHBoxLayout()
            camera_label = QLabel("Camera maker:")
            self.camera_maker_edit = QLineEdit(self)
            self.camera_maker_edit.setToolTip('Name of camera manufacturer to set. Blank to leave Exif value.')
            model_label = QLabel("Model:")
            self.camera_model_edit = QLineEdit(self)
            self.camera_maker_edit.setToolTip('Model of camera to set. Blank to leave Exif value.')
            camera_layout.addWidget(camera_label)
            camera_layout.addWidget(self.camera_maker_edit)
            camera_layout.addWidget(model_label)
            camera_layout.addWidget(self.camera_model_edit)
            layout.addLayout(camera_layout)

            tags_layout = QHBoxLayout()
            tags_label = QLabel("Tags:")
            self.tags_edit = QLineEdit(self)
            self.tags_edit.setToolTip('Tags to apply to these images.')
            tags_layout.addWidget(tags_label)
            tags_layout.addWidget(self.tags_edit)
            layout.addLayout(tags_layout)

            # OK and Cancel buttons
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            layout.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        # get current date and time from the dialog
        def dateTime(self):
            return self.datetime.dateTime()

        # static method to create the dialog and return (date, time, maker, model, tags, accepted)
        @staticmethod
        def getDateTime(parent = None):
            dialog = ExtendedLoadDialog(parent)
            result = dialog.exec_()
            date = dialog.dateTime()
            setdate = dialog.set_checkbox.isChecked()
            maker = dialog.camera_maker_edit.text()
            model = dialog.camera_model_edit.text()
            tags = dialog.tags_edit.text()
            return (date.date(), date.time(), setdate, maker, model, tags, result == QDialog.Accepted)                

    class PhotoxDialog(QDialog):
        """
        Implement a different sort of photo browser.
        """
        def HLine(self):
            """
            Draw a horizontal line to separate control groups.
            """
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            return line

        def VLine(self):
            """
            Draw a vertical line to separate control groups.
            """
            line = QFrame()
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)
            return line

        def add_spacing(self,layout,minstretch=1):
            """
            Add horizontal space and separating line between control groups.
            """
            layout.addSpacing(minstretch)
            layout.addStretch(1)
            layout.addWidget(self.VLine())
            layout.addStretch(1)
            layout.addSpacing(minstretch)

        def __init__(self,parent=None):
            super(PhotoxDialog,self).__init__(parent)
            # Try to have the dialog show a minimize icon.
            windowflags = Qt.Window | Qt.WindowSystemMenuHint | \
                Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint
            self.setWindowFlags(windowflags)

            # Find OS once.
            self.is_macos = sys.platform.startswith('darwin')

            # Photox widget.
            self.photox = PhotoxWidget(parent=self)
            self.photox.setUser(self)
            self.photox.setFocus()

            # Declare a group of controls for loading and saving the database.
            db_label = QLabel("DB:")
            self.db_drop_text = DropLineEdit(callback=self.db_handle_dropped_path)
            self.db_drop_text.setToolTip('PhotoX .photodb database file name. Can drag and drop file here, or press Load for file browser.')
            self.db_load_button = QPushButton("Load")
            self.db_load_button.setFixedWidth(60)
            self.db_load_button.setToolTip('Load a PhotoX database file.')

            self.db_count_edit = QLineEdit('0 images')
            self.db_count_edit.setFixedWidth(95)
            self.db_count_edit.setReadOnly(True)

            self.db_create_button = QPushButton("Create")
            self.db_create_button.setFixedWidth(70)
            self.db_create_button.setToolTip('Create a new PhotoX database file.')

            self.db_save_button = QPushButton("Save")
            self.db_save_button.setFixedWidth(60)
            self.db_save_button.setToolTip('Save to the current PhotoX database file.')

            ph_label = QLabel("Source:")
            self.ph_drop_text = DropLineEdit(callback=self.ph_handle_dropped_path)
            self.ph_drop_text.setToolTip('Folder name containing photos to import. Can drag and drop folder here, or press Add for folder browser.')

            self.ph_load_button = QPushButton("Add")
            self.ph_load_button.setFixedWidth(50)
            self.ph_load_button.setToolTip('Import all photos in a folder.')

            self.ph_load_extended_button = QPushButton("AddEx")
            self.ph_load_extended_button.setFixedWidth(70)
            self.ph_load_extended_button.setToolTip('Import all photos in a folder with overrides.')

            self.ph_delsel_button = QPushButton("Del Sel")
            self.ph_delsel_button.setFixedWidth(70)
            self.ph_delsel_button.setToolTip('Move all selected photos to the deleted list.')            

            self.ph_undel_button = QPushButton("Undelete")
            self.ph_undel_button.setFixedWidth(80)
            self.ph_undel_button.setToolTip('Reinstate all photos on the deleted list.')

            self.help_button = QPushButton("Help/Status")

            io_layout = QHBoxLayout()
            io_layout.setSpacing(2)
            #io_layout.setMargin(2)
            io_layout.addWidget(db_label)
            io_layout.addWidget(self.db_drop_text)
            io_layout.addWidget(self.db_load_button)
            #self.add_spacing(io_layout,2)
            io_layout.addWidget(self.db_count_edit)
            #self.add_spacing(io_layout,2)
            io_layout.addWidget(self.db_create_button)
            io_layout.addWidget(self.db_save_button)
            #self.add_spacing(io_layout,2)
            io_layout.addWidget(ph_label)
            io_layout.addWidget(self.ph_drop_text)
            io_layout.addWidget(self.ph_load_button)
            io_layout.addWidget(self.ph_load_extended_button)
            #self.add_spacing(io_layout,2)
            io_layout.addWidget(self.ph_delsel_button)
            io_layout.addWidget(self.ph_undel_button)
            io_layout.addWidget(self.help_button)

            # Declare a group of controls for selections.
            fl_label = QLabel("Wanted:")
            self.fl_filter_text = QLineEdit("")
            self.fl_filter_text.setToolTip('Tags (space separated) to select photos by.')
            self.fl_filter_button = QPushButton("Sel Wanted")
            self.fl_filter_button.setFixedWidth(95)
            self.fl_filter_button.setToolTip('Select by tags in Wanted text.')

            self.fl_all_button = QPushButton("Sel *")
            self.fl_all_button.setFixedWidth(60)
            self.fl_all_button.setToolTip('Select all photos')

            flt_label = QLabel("Known:")
            self.known_tags_combo = QComboBox()
            self.known_tags_combo.setDuplicatesEnabled(False)
            self.known_tags_combo.setToolTip('List of tags currently defined.')

            self.known_tags_button = QPushButton("+ Wanted")
            self.known_tags_button.setFixedWidth(85)
            self.known_tags_button.setToolTip('Add a defined tag to the list of wanted tags.')

            self.known_tags_copy_button = QPushButton("+ Tags")
            self.known_tags_copy_button.setFixedWidth(70)
            self.known_tags_copy_button.setToolTip('Add a defined tag to the list of tags to add to image(s).')

            cam_label = QLabel("Camera:")
            self.cam_combo = QComboBox()
            self.cam_combo.addItems(["Any"])
            self.cam_combo.setCurrentIndex(0)
            self.cam_combo.setToolTip('List of cameras used to take the photos.')

            exif_label = QLabel("EXIF:")
            self.exif_combo = QComboBox()
            self.exif_combo.addItems(["All","EXIF only","No EXIF only"])
            self.exif_combo.setCurrentIndex(0)
            self.exif_combo.setToolTip('Select photos that have or do not have EXIF data.')

            self.pick_add_button = QPushButton("Pick +")
            self.pick_add_button.setFixedWidth(70)
            self.pick_add_button.setToolTip('Add current photo to pick.')

            self.pick_sub_button = QPushButton("Pick -")
            self.pick_sub_button.setFixedWidth(70)
            self.pick_sub_button.setToolTip('Remove current photo from pick.')

            self.pick_clear_button = QPushButton("Clear Pick")
            self.pick_clear_button.setFixedWidth(85)
            self.pick_clear_button.setToolTip('Clear pick.')

            self.pick_sel_button = QPushButton("Sel Pick")
            self.pick_sel_button.setFixedWidth(85)
            self.pick_sel_button.setToolTip('Select all picked and clear pick.')

            sel_layout = QHBoxLayout()
            sel_layout.addWidget(fl_label)
            sel_layout.addWidget(self.fl_filter_text)
            sel_layout.addWidget(self.fl_filter_button)

            sel_layout.addWidget(self.fl_all_button)

            sel_layout.addWidget(flt_label)
            sel_layout.addWidget(self.known_tags_combo)

            sel_layout.addWidget(self.known_tags_button)
            sel_layout.addWidget(self.known_tags_copy_button)

            sel_layout.addWidget(cam_label)
            sel_layout.addWidget(self.cam_combo)

            sel_layout.addWidget(exif_label)
            sel_layout.addWidget(self.exif_combo)

            sel_layout.addWidget(self.pick_add_button)
            sel_layout.addWidget(self.pick_sub_button)
            sel_layout.addWidget(self.pick_clear_button)
            sel_layout.addWidget(self.pick_sel_button)

            # Declare a group of controls for adding tags. And doing time based selection.
            tg_label = QLabel("Tags:")
            self.tg_add_edit = QLineEdit("")
            self.tg_add_edit.setToolTip('Tags (space separated) to add or set on photo(s).')
            
            self.tg_add_button = QPushButton("+ Tags")
            self.tg_add_button.setFixedWidth(70)
            self.tg_add_button.setToolTip('Add tags in Tags to current or all selected photos.')

            self.tg_set_button = QPushButton("= Tags")
            self.tg_set_button.setFixedWidth(70)
            self.tg_set_button.setToolTip('Set tags in Tags on current or all selected photos.')

            self.tg_sub_button = QPushButton("- Tags")
            self.tg_sub_button.setFixedWidth(70)
            self.tg_sub_button.setToolTip('Remove tags in Tags from current or all selected photos.')

            self.tg_combo = QComboBox()
            self.tg_combo.addItems(["Tag 1","Tag 1/move","Tag selected"])
            self.tg_combo.setCurrentIndex(0)
            self.tg_combo.setToolTip('Tag current image, tag current and move to next, tag all selected.')

            tm_label = QLabel("Times:")
            self.tm_time_edit = QLineEdit("<None>")
            self.tm_time_edit.setReadOnly(True)
            self.tm_time_edit.setFixedWidth(320)
            self.tm_time_edit.setToolTip('Currently selected time range (by right mouse drag over times), if any.')

            self.tm_select_button = QPushButton("Sel Times")
            self.tm_select_button.setToolTip('Use the current time selection to select photos.')

            self.map_locate_button = QPushButton("Google Maps")
            self.map_locate_button.setToolTip('Show current photo location (if known) with Google Maps in browser.')

            tag_layout = QHBoxLayout()
            tag_layout.addWidget(tg_label)
            tag_layout.addWidget(self.tg_add_edit)
            tag_layout.addWidget(self.tg_add_button)
            tag_layout.addWidget(self.tg_set_button)
            tag_layout.addWidget(self.tg_sub_button)
            tag_layout.addWidget(self.tg_combo)
            self.add_spacing(tag_layout,2)
            tag_layout.addWidget(tm_label)
            tag_layout.addStretch(1)
            tag_layout.addWidget(self.tm_time_edit)
            tag_layout.addWidget(self.tm_select_button)
            tag_layout.addStretch(1)
            self.add_spacing(tag_layout,2)
            tag_layout.addWidget(self.map_locate_button)

            # Declare two controls to set where to save (export) JPEG and RAW images to.
            jpeg_save_label = QLabel("JPEG export:")
            self.jpeg_save_drop_text = DropLineEdit(callback=self.jpeg_save_handle_dropped_path)
            self.jpeg_save_drop_text.setToolTip('Where to save (export) JPEGs to. Drag and drop directory here.')

            self.jpeg_save_button = QPushButton("Dfl")
            self.jpeg_save_button.setFixedWidth(40)
            self.jpeg_save_button.setToolTip('Restore default JPEG save folder (DB/saved).')

            raw_save_label = QLabel("  RAW export:")
            self.raw_save_drop_text = DropLineEdit(callback=self.raw_save_handle_dropped_path)
            self.raw_save_drop_text.setToolTip('Where to save (export) RAWs to. Drag and drop directory here.')

            self.raw_save_button = QPushButton("Dfl")
            self.raw_save_button.setFixedWidth(40)
            self.raw_save_button.setToolTip('Restore default RAW save folder (DB/saved_raws).')

            self.doexport_button = QPushButton("Export")
            self.doexport_button.setFixedWidth(75)
            self.doexport_button.setToolTip('Export current photos JPEG and RAW images.')            

            self.doexport_pick_button = QPushButton("ExpPick")
            self.doexport_pick_button.setFixedWidth(75)
            self.doexport_pick_button.setToolTip('Export all picked photos JPEG and RAW images.')            

            # EXIF info fetch.
            self.exif_jpeg_button = QPushButton("INFO JPEG")
            self.exif_jpeg_button.setFixedWidth(100)
            self.exif_jpeg_button.setToolTip('Show photo data and the EXIF data in the JPEG image.')

            self.exif_raw_button = QPushButton("INFO RAW")
            self.exif_raw_button.setFixedWidth(100)
            self.exif_raw_button.setToolTip('Show photo data and the EXIF data in the RAW image (if there is one).')

            # Import processed version.
            #proc_read_label = QLabel("PROC import:")
            self.proc_read_drop_text = DropLineEdit(callback=self.proc_read_handle_dropped_path)
            self.proc_read_drop_text.setToolTip('Where to import processed versions from. Drag and drop directory here.')

            self.proc_read_button = QPushButton("Import")
            self.proc_read_button.setFixedWidth(75)
            self.proc_read_button.setToolTip('Import all processed images.')

            save_layout = QHBoxLayout()
            save_layout.addWidget(jpeg_save_label)
            save_layout.addWidget(self.jpeg_save_drop_text)
            save_layout.addWidget(self.jpeg_save_button)
            save_layout.addWidget(raw_save_label)
            save_layout.addWidget(self.raw_save_drop_text)
            save_layout.addWidget(self.raw_save_button)
            save_layout.addWidget(self.doexport_button)
            save_layout.addWidget(self.doexport_pick_button)

            save_layout.addWidget(self.exif_jpeg_button)
            save_layout.addWidget(self.exif_raw_button)
            save_layout.addWidget(self.proc_read_drop_text)
            save_layout.addWidget(self.proc_read_button)

            # Assemble the groups vertically.
            layout = QVBoxLayout()
            layout.setSpacing(2)

            layout.addWidget(self.photox)
            layout.addLayout(io_layout)
            layout.addWidget(self.HLine())
            layout.addLayout(sel_layout)
            layout.addWidget(self.HLine())
            layout.addLayout(tag_layout)
            layout.addWidget(self.HLine())
            layout.addLayout(save_layout)
            self.setLayout(layout)

            # Connect event handlers.
            self.db_drop_text.returnPressed.connect(self.db_handle_typed_path)
            self.db_load_button.clicked.connect(self.db_load)
            self.db_create_button.clicked.connect(self.db_create)
            self.db_save_button.clicked.connect(self.db_save)
            
            self.ph_drop_text.returnPressed.connect(self.ph_handle_typed_path)
            self.ph_load_button.clicked.connect(self.ph_load)
            self.ph_load_extended_button.clicked.connect(self.ph_load_extended)

            self.ph_delsel_button.clicked.connect(self.ph_delsel)
            self.ph_undel_button.clicked.connect(self.ph_undel)
            
            self.cam_combo.currentIndexChanged.connect(self.sel_camera)
            
            self.exif_combo.currentIndexChanged.connect(self.sel_exif)
            
            self.tg_add_button.clicked.connect(self.tag_add)
            self.tg_set_button.clicked.connect(self.tag_set)
            self.tg_sub_button.clicked.connect(self.tag_remove)
            
            self.fl_filter_button.clicked.connect(self.tag_filter)
            self.fl_all_button.clicked.connect(self.sel_all)
            self.tg_combo.currentIndexChanged.connect(self.tag_mode_changed)
            
            self.known_tags_button.clicked.connect(self.add_known_tag)
            self.known_tags_copy_button.clicked.connect(self.copy_known_tag)
            
            self.map_locate_button.clicked.connect(self.map_locate)
            
            self.help_button.clicked.connect(self.showstatus)
            
            self.tm_select_button.clicked.connect(self.time_select)
            
            self.jpeg_save_button.clicked.connect(self.jpeg_save_default)
            self.jpeg_save_drop_text.textChanged.connect(self.jpeg_save_handle_changed_path)
            self.jpeg_save_drop_text.returnPressed.connect(self.jpeg_save_handle_typed_path)
            self.raw_save_button.clicked.connect(self.raw_save_default)
            self.raw_save_drop_text.textChanged.connect(self.raw_save_handle_changed_path)
            self.raw_save_drop_text.returnPressed.connect(self.raw_save_handle_typed_path)
            self.doexport_button.clicked.connect(self.export_image_one)
            self.doexport_pick_button.clicked.connect(self.export_image_pick)
            self.exif_jpeg_button.clicked.connect(self.get_exif_jpeg)
            self.exif_raw_button.clicked.connect(self.get_exif_raw)
            self.proc_read_button.clicked.connect(self.proc_read)
            
            self.pick_add_button.clicked.connect(self.add_to_pick)
            self.pick_sub_button.clicked.connect(self.remove_from_pick)
            self.pick_clear_button.clicked.connect(self.clear_pick)
            self.pick_sel_button.clicked.connect(self.pick_to_sel)

            # Turn off default button behaviour on pressing enter.
            for btn in self.findChildren(QPushButton):
                btn.setAutoDefault(False)
                btn.setDefault(False)

            # Data.
            self.database_path = ''
            self.photo_folder = ''
            self.sel_cam_name = 'Any'
            self.sel_exif_name = 'All'
            self.savedtime = 0
            self.tag_mode = K_TAG_1

        def time_box_handler(self,text):
            """
            Update the time edit widget with the current time range string.
            """
            self.tm_time_edit.setText(text)

        def db_handle_typed_path(self):
            """
            Choose database with typed path.
            """
            path = str(self.db_drop_text.text())
            if os.path.exists(path):
                self.database_path = path
            else:
                QMessageBox.warning(self, 'Database selection', 'Database does not exist.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.db_drop_text.setText('')

        def db_handle_dropped_path(self,path):
            """
            Choose database with dropped path.
            """
            self.database_path = path
            self.db_drop_text.setText(path)

        def db_create(self):
            """
            Create a new, empty, database. This is a directory and file name chosen by the user.
            """
            photodbname = str(QFileDialog.getSaveFileName(self,'Enter database file name.',os.getenv('HOME'),"*.photodb")[0])
            if os.path.exists(photodbname):
                QMessageBox.warning(self, 'Database creation', 'Database file already exists.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
            else:
                dbhomedir, dbname = os.path.split( photodbname )
                namepart,extpart = os.path.splitext(dbname)
                photodbname = os.path.join(dbhomedir,namepart+'.photodb')
                if photohack.create_folder_if_not_exists( dbhomedir ):
                    self.db_drop_text.setText(photodbname)
                    try:
                        os.chdir( dbhomedir )
                    except Exception as e:
                        print('ERROR: db_create() failed. Reason:', e)
                        QMessageBox.warning(self, 'Database creation',
                                            'FATAL: Cannot change working directory to database home',
                                            QMessageBox.Ok, QMessageBox.Ok)
                        sys.exit(9)  
                else:
                    QMessageBox.warning(self, 'Database creation', 'Cannot create folder{0}.'.format(dbhomedir), 
                                        QMessageBox.Ok, QMessageBox.Ok)

        def db_load(self):
            """
            Load the chosen database.
            """
            photodbname = str(self.db_drop_text.text())
            secondload = False
            if len(photodbname) != 0:
                reply = QMessageBox.question(self, 'Reload database', 
                                             'Yes = Reload current database (lose changes). No = Load new database.', 
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    photodbname = ''
                    secondload = True
                    self.db_drop_text.setText('')
            if len(photodbname) == 0:
                photodbnametemp = str(QFileDialog.getOpenFileName(self,'Choose database file.',os.getenv('HOME'),'*.photodb')[0])
                if secondload and (len(photodbnametemp) == 0):
                    return
                photodbname = photodbnametemp
                self.db_drop_text.setText(photodbname)
            if len(photodbname) == 0:
                QMessageBox.warning(self, 'Database selection', 'No database specified.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
            else:
                dbhomedir, dbname = os.path.split( str(photodbname) )
                if self.photox.debuglevel > 1:
                    print('db_load(): dbhomedir=',dbhomedir,'dbname=',dbname)
                if dbhomedir != '':
                    try:
                        os.chdir( dbhomedir )
                    except Exception as e:
                        print('ERROR: db_load() failed. Reason:', e)
                        QMessageBox.warning(self, 'Database selection',
                                            'FATAL: Cannot change working directory to database home',
                                            QMessageBox.Ok, QMessageBox.Ok)
                        sys.exit(9)
                # Read the database from file.
                num_images = self.photox.set_photodb(dbname)
                if num_images == 0:
                    QMessageBox.warning(self, 'Database selection', 'Failed to read database.', 
                                        QMessageBox.Ok, QMessageBox.Ok)
                    self.db_count_edit.setText('0 images')
                else:
                    self.db_count_edit.setText('{0} images'.format(num_images))
                # Find the types of camera in the database.
                self.cam_combo.clear()
                self.cam_combo.addItems(["Any"])
                for camera in self.photox.cameras:
                    self.cam_combo.addItem(camera)
                self.cam_combo.setCurrentIndex(0)
                # Select everything.
                self.sel_cam_name = 'Any'
                self.sel_exif_name = 'All'
                self.photox.make_selection(self.photox.sortedinfotable,self.sel_cam_name,self.sel_exif_name,None)
                # Find a list of unique tags in the database.
                self.known_tags = photohack.find_all_tags(self.photox.sortedinfotable)
                if len(self.known_tags) > 0:
                    for known_tag in self.known_tags:
                        self.known_tags_combo.addItem(known_tag)
                    self.known_tags_combo.setCurrentIndex(0)
                # Unselect photo (no thumbnail).
                self.photox.selected_photo = -1
                self.photox.update()

        def db_save(self):
            """
            Save the database, making a backup first.
            """
            photodbname = str(self.db_drop_text.text())
            if len(photodbname) == 0:
                QMessageBox.warning(self, 'Database selection', 'No database specified yet.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
            else:
                # If it exists, back it up.
                if os.access( photodbname, os.F_OK ):
                    dated = time.strftime("_%Y_%m_%d_%H_%M_%S", time.gmtime(time.time()))
                    parts = os.path.splitext(str(photodbname))
                    dated_photodbname = parts[0] + dated + parts[1]
                    if self.photox.debuglevel > 1:
                        print('db_save(): dated_photodbname=',dated_photodbname)
                    shutil.copy2(photodbname,dated_photodbname)
                # Save its current state.
                if not self.photox.save_photodb(photodbname):
                    QMessageBox.warning(self, 'Database save', 'Failed to save database.', 
                                        QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.information(self, 'Database save', 'Database saved!', 
                                            QMessageBox.Ok, QMessageBox.Ok)
                    self.savedtime = time.time()

        def ph_handle_typed_path(self):
            """
            Choose location of new photographs with typed path.
            """
            path = str(self.ph_drop_text.text())
            if os.path.exists(path):
                if self.photox.debuglevel > 1:
                    print('ph_handle_typed_path(): source path=',path)
                pass
            else:
                QMessageBox.warning(self, 'Add photo folder', 'Folder does not exist.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.ph_drop_text.setText('')

        def ph_handle_dropped_path(self,path):
            """
            Choose location of new photographs with dropped path.
            """
            if self.photox.debuglevel > 1:
                print('ph_handle_dropped_path(): source path=',path)
            self.ph_drop_text.setText(path)

        def ph_load(self):
            """
            Add more photos to the database (in memory) from the photos in the chosen photo
            source directory. Generate the 'photos' and 'thumbnails' directory contents
            (or add to them) for this new set of photos.
            """
            self.ph_load_core(False)

        def ph_load_extended(self):
            """
            Present an extended information dialog and use its contents to override the data
            obtained from any Exif data in the input files.
            """
            self.ph_load_core(True)


        def ph_load_core(self, extended=False):
            """
            Do all the work for ph_load() and ph_load_extended().
            """
            # We need a database to exist to do this.
            photodbname = str(self.db_drop_text.text())
            if len(photodbname) == 0:
                QMessageBox.warning(self, 'Database selection', 'No database specified yet.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
                return
            # Find the photos.
            path = str(self.ph_drop_text.text())
            if len(path) == 0:
                path = str(QFileDialog.getExistingDirectory(self,'Photo source folder',os.getenv('HOME')))
                self.ph_drop_text.setText(path)
            if len(path) == 0:
                QMessageBox.warning(self, 'Add photos', 'No source directory specified.', 
                                    QMessageBox.Ok, QMessageBox.Ok)
            else:
                num_images = 0
                if self.photox.debuglevel > 1:
                    print('ph_load(): source path=',path)
                if extended:
                    date, time, setdate, maker, model, tags, ok = ExtendedLoadDialog.getDateTime()
                    taglist = tags.split()
                    if len(taglist) == 0:
                        taglist = None
                    day = date.day()
                    month = date.month()
                    year = date.year()
                    hour = time.hour()
                    minute = time.minute()
                    second = time.second()
                    tpl = (year, month, day, hour, minute, second)
                    unixtime = photohack.time_tuple_to_time(tpl)
                    maker = maker.strip()
                    if len(maker) == 0:
                        maker = None
                    model = model.strip()
                    if len(model) == 0:
                        model = None
                    if setdate:
                        unixtime = unixtime
                    else:
                        unixtime = None
                    if ok:
                        num_images = self.photox.add_photos_to_photodb(path,
                                                                       taglist=taglist,
                                                                       maker=maker,
                                                                       model=model,
                                                                       unixtime=unixtime)
                else:
                    num_images = self.photox.add_photos_to_photodb(path)
                if num_images == 0:
                    QMessageBox.warning(self, 'Add photos', 'Failed to add photos to database.', 
                                        QMessageBox.Ok, QMessageBox.Ok)
                    self.db_count_edit.setText('0 images')
                else:
                    self.db_count_edit.setText('{0} images'.format(num_images))
                    self.photox.cameras = photohack.camera_list(self.photox.infotable)
                    self.cam_combo.clear()
                    self.cam_combo.addItems(["Any"])
                    for camera in self.photox.cameras:
                        self.cam_combo.addItem(camera)
                    self.cam_combo.setCurrentIndex(0)
            self.photox.update()
            self.ph_drop_text.clear()            

        def ph_delsel(self):
            reply = QMessageBox.question(self, 'Delete photos', 'Move selected photos to deleted list?', 
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.photox.delete_selected()
            self.photox.update()

        def ph_undel(self):
            self.photox.undelete()
            self.photox.update()
            # Find a list of unique tags in the database.
            self.known_tags_combo.clear()
            self.known_tags = photohack.find_all_tags(self.photox.sortedinfotable)
            if len(self.known_tags) > 0:
                for known_tag in self.known_tags:
                    self.known_tags_combo.addItem(known_tag)
                self.known_tags_combo.setCurrentIndex(0)

        def sel_camera(self,ihost):
            """
            Handle camera name selection.
            """
            self.sel_cam_name = str(self.cam_combo.itemText(ihost))
            if self.photox.debuglevel > 1:
                print('sel_camera(): sel_cam_name=',self.sel_cam_name)
            tags = str(self.fl_filter_text.text())
            self.photox.make_selection(self.photox.sortedinfotable,self.sel_cam_name,self.sel_exif_name,tags)
            if self.photox.debuglevel > 1:
                print('... Num selected = ', self.photox.count_selected(self.photox.sortedinfotable))
            self.photox.update()

        def sel_exif(self,ihost):
            """
            Handle Exif type selection.
            """
            self.sel_exif_name = str(self.exif_combo.itemText(ihost))
            if self.photox.debuglevel > 1:
                print('sel_exif(): sel_exif_name=',self.sel_exif_name)
            tags = str(self.fl_filter_text.text())
            self.photox.make_selection(self.photox.sortedinfotable,self.sel_cam_name,self.sel_exif_name,tags)
            if self.photox.debuglevel > 1:
                print('... Num selected = ', self.photox.count_selected(self.photox.sortedinfotable))
            self.photox.update()

        def tag_mode_changed(self,imode):
            """
            Handle tag mode selection.
            """
            self.tag_mode = imode
            
        def tag_add(self):
            """
            Add the tags in the add tag edit box to the tags for all selected photos.
            """
            tags = str(self.tg_add_edit.text())
            if len(tags) > 0:
                onetags = tags.split()
                for onetag in onetags:
                    self.photox.add_a_tag(onetag, (self.tag_mode == K_TAG_SELECTED))
                    if not (onetag in self.known_tags):
                        self.known_tags_combo.addItem(onetag)
                        self.known_tags.append(onetag)
            if self.tag_mode == K_TAG_1_MOVE:
                self.photox.move_to_next_selected_photo(1)
            self.photox.update()

        def tag_remove(self):
            """
            Remove the tags in the tag edit box from the tags for all selected photos.
            """
            tags = str(self.tg_add_edit.text())
            if len(tags) > 0:
                onetags = tags.split()
                for onetag in onetags:
                    self.photox.remove_a_tag(onetag, (self.tag_mode == K_TAG_SELECTED))
            if self.tag_mode == K_TAG_1_MOVE:
                self.photox.move_to_next_selected_photo(1)
            self.photox.update()

        def tag_set(self):
            """
            Set the tags in the add tag edit box as the tags for all selected photos.
            """
            doit = True
            if self.tag_mode == K_TAG_SELECTED:
                reply = QMessageBox.question(self, 'Set tags', 'Set tags on all selected photos?.', 
                                             QMessageBox.Yes, QMessageBox.No)
                doit = (reply == QMessageBox.Yes)
            if doit:
                self.photox.remove_all_tags( (self.tag_mode == K_TAG_SELECTED) )
                tags = str(self.tg_add_edit.text())
                if len(tags) > 0:
                    onetags = tags.split()
                    for onetag in onetags:
                        self.photox.add_a_tag(onetag, (self.tag_mode == K_TAG_SELECTED) )
                        if not (onetag in self.known_tags):
                            self.known_tags_combo.addItem(onetag)
                            self.known_tags.append(onetag)
            if self.tag_mode == K_TAG_1_MOVE:
                self.photox.move_to_next_selected_photo(1)
            self.photox.update()

        def tag_filter(self):
            """
            Apply the tags as a filter.
            """
            tags = str(self.fl_filter_text.text())
            if self.photox.debuglevel > 1:
                print('tag_filter(): tags = ',tags)
            if len(tags) > 0:
                self.photox.make_selection(self.photox.sortedinfotable,self.sel_cam_name,self.sel_exif_name,tags)
            if self.photox.debuglevel > 1:
                print('... Num selected = ', self.photox.count_selected(self.photox.sortedinfotable))
            self.photox.update()

        def sel_all(self):
            """
            Select everything.
            """
            self.photox.select_all()
            self.photox.update()

        def add_known_tag(self):
            """
            Add the selected known tag to the list of tags to filter on.
            """
            try:
                cursel = self.known_tags_combo.currentIndex()
                tag = str(self.known_tags_combo.itemText(cursel))
                filtags = str(self.fl_filter_text.text()) + ' ' + tag
                self.fl_filter_text.setText(filtags)
            except:
                pass

        def copy_known_tag(self):
            """
            Copy the selected known tag to the list of tags to potentially add or set.
            """
            try:
                cursel = self.known_tags_combo.currentIndex()
                tag = str(self.known_tags_combo.itemText(cursel))
                filtags = str(self.tg_add_edit.text()) + ' ' + tag
                self.tg_add_edit.setText(filtags)
            except:
                pass

        def add_to_pick(self):
            """
            Add current photo to pick.
            """
            self.photox.maintain_picked_set(self.photox.selected_photo,True)
            self.photox.update()
        
        def remove_from_pick(self):
            """
            Add current photo to pick.
            """
            self.photox.maintain_picked_set(self.photox.selected_photo,False)
            self.photox.update()
        
        def clear_pick(self):
            """
            Clear the pick.
            """
            self.photox.picked_set_clear()
            self.photox.update()
        
        def pick_to_sel(self):
            """
            Add the pick to the selection.
            """
            self.photox.pick_to_selected(0)
            self.photox.update()
    
        def map_locate(self):
            """
            If the photo has geo tagging data, open Google Maps at its location.
            """
            self.photox.google_maps()

        def time_select(self):
            """
            Use the current time selection to select photos.
            """
            rangestring = str(self.tm_time_edit.text())
            if len(rangestring) >= 38:
                splitstring = rangestring.split('>')
                if len(splitstring) == 2:
                    starttime = photohack.exif_to_time(splitstring[0].strip())
                    endtime = photohack.exif_to_time(splitstring[1].strip())
                    if self.photox.debuglevel > 1:
                        print('time_select(): starttime=',starttime,'endtime=',endtime)
                    self.photox.unselect_by_time(starttime,endtime)
                    self.photox.update()

        def jpeg_save_handle_dropped_path(self,path):
            """
            Choose where to save JPEGs with dropped path.
            """
            self.photox.outjpegpath = path
            self.jpeg_save_drop_text.setText(path)
            if self.photox.debuglevel > 1:
                print('set outjpegpath =',self.photox.outjpegpath,'type(path):',type(path))

        def jpeg_save_handle_typed_path(self):
            """
            Choose where to save JPEGs with typed path.
            """
            self.photox.outjpegpath = str(self.jpeg_save_drop_text.text())
            self.jpeg_save_drop_text.setStyleSheet("color: green;")

        def jpeg_save_handle_changed_path(self):
            """
            Choose where to save JPEGs with typed path.
            """
            self.photox.outjpegpath = str(self.jpeg_save_drop_text.text())
            self.jpeg_save_drop_text.setStyleSheet("color: red;")

        def jpeg_save_default(self):
            """
            Restore the default JPEG save location.
            """
            self.photox.outjpegpath = None
            self.jpeg_save_drop_text.clear()
            if self.photox.debuglevel > 1:
                print('reset outjpegpath to None')

        def raw_save_handle_dropped_path(self,path):
            """
            Choose where to save RAWs with dropped path.
            """
            self.photox.outrawpath = path
            self.raw_save_drop_text.setText(path)

        def raw_save_handle_typed_path(self):
            """
            Choose where to save RAWs with typed path.
            """
            self.photox.outrawpath = str(self.raw_save_drop_text.text())
            self.raw_save_drop_text.setStyleSheet("color: green;")

        def raw_save_handle_changed_path(self):
            """
            Choose where to save RAWs with typed path.
            """
            self.photox.outrawpath = str(self.raw_save_drop_text.text())
            self.raw_save_drop_text.setStyleSheet("color: red;")

        def raw_save_default(self):
            """
            Restore the default JPEG save location.
            """
            self.photox.outrawpath = None
            self.raw_save_drop_text.clear()

        def export_image_one(self):
            """
            Export the current image.
            """
            self.export_image(False)
            
        def export_image_pick(self):
            """
            Export all picked images.
            """
            self.export_image(True)
            
        def export_image(self,allpicked):
            """
            Save/Export the current image or all picked images.
            """
            if allpicked:
                for i in range(0,len(self.photox.pickedset)):
                    self.photox.save_photo(self.photox.pickedset[i])
            else:
                if self.photox.selected_photo >= 0:
                    self.photox.save_photo(self.photox.selected_photo)
            self.photox.update()

        def get_exif_jpeg(self):
            """
            Get the JPEG EXIF and display it in a popup dialog.
            """
            exifstring = self.photox.get_exif_data(False)
            # Display it.
            statRect = QRect(10,10,610,500)
            font = QFont('Courier')
            font.setFixedPitch(True)
            font.setPointSize(11)
            self.statLabel = QLabel()
            self.statLabel.setTextFormat(Qt.PlainText)
            self.statLabel.setFont(font)
            self.statLabel.setText(exifstring)
            self.scrollArea = QScrollArea()
            self.scrollArea.setGeometry(statRect)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWindowTitle("JPEG EXIF information")
            self.scrollAreaWidgetContents = QWidget()
            self.scrollAreaWidgetContents.setGeometry(statRect)
            self.scrollArea.setWidget(self.statLabel)
            self.scrollArea.show()

        def get_exif_raw(self):
            """
            Get the RAW EXIF and display it in a popup dialog.
            """
            exifstring = self.photox.get_exif_data(True)
            # Display it.
            statRect = QRect(10,10,610,500)
            font = QFont('Courier')
            font.setFixedPitch(True)
            font.setPointSize(11)
            self.statLabel = QLabel()
            self.statLabel.setTextFormat(Qt.PlainText)
            self.statLabel.setFont(font)
            self.statLabel.setText(exifstring)
            self.scrollArea = QScrollArea()
            self.scrollArea.setGeometry(statRect)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWindowTitle("RAW EXIF information")
            self.scrollAreaWidgetContents = QWidget()
            self.scrollAreaWidgetContents.setGeometry(statRect)
            self.scrollArea.setWidget(self.statLabel)
            self.scrollArea.show()

        def proc_read_handle_dropped_path(self,path):
            """
            Choose where to read processed versions with dropped path.
            """
            self.photox.inprocpath = path
            self.proc_read_drop_text.setText(path)

        def proc_read(self):
            """
            Read all processed versions.
            """
            if self.photox.inprocpath is not None:

                # Add the processed photos to the database.
                # Generate the 'photos' and 'thumbnails' directory contents
                # (or add to them) for this new set of photos.
                # We need a database to exist to do this.
                photodbname = str(self.db_drop_text.text())
                if len(photodbname) == 0:
                    QMessageBox.warning(self, 'Database selection', 'No database specified yet.', 
                                        QMessageBox.Ok, QMessageBox.Ok)
                    return
                # Find the photos.
                path = self.photox.inprocpath
                if not os.path.isdir(path):
                    QMessageBox.warning(self, 'Read processed', 'Processed image directory does not exist.', 
                                        QMessageBox.Ok, QMessageBox.Ok)
                else:
                    if self.photox.debuglevel > 1:
                        print('proc_read(): source path=',path)
                    num_images = self.photox.add_photos_to_photodb(path,doingprocessed=True)
                    if num_images == 0:
                        QMessageBox.warning(self, 'Read processed', 'Failed to add photos to database.', 
                                            QMessageBox.Ok, QMessageBox.Ok)
                    else:
                        self.db_count_edit.setText('{0} images'.format(num_images))
                        self.photox.cameras = photohack.camera_list(self.photox.infotable)
                        self.cam_combo.clear()
                        self.cam_combo.addItems(["Any"])
                        for camera in self.photox.cameras:
                            self.cam_combo.addItem(camera)
                        self.cam_combo.setCurrentIndex(0)
                self.photox.update()

        def showstatus(self):
            """
            Show help/status dialog.
            """
            # Get status data.
            totalsize, \
                num_exif, \
                num_geotagged, \
                num_commented, \
                num_cameraed, \
                num_vert, \
                earliest_time, \
                latest_time, \
                num_raw, \
                num_processed = \
                photohack.stats(self.photox.sortedinfotable)
            num_selected = self.photox.count_selected(self.photox.sortedinfotable)
            num_known_tags = len(photohack.find_all_tags(self.photox.sortedinfotable))
            num_picked = len(self.photox.pickedset)
            # Format it.
            sp3 = '&nbsp;&nbsp;&nbsp;'
            sp6 = sp3 + sp3
            sp9 = sp6 + sp3
            smsg = "<font color=red size=7><b>PhotoX Help and Status:</b></font><br>"
            smsg += "{0}Version: {1}<br>".format(sp6,current_version_string)
            smsg += "{0}PySide/Qt version: {1}<br>".format(sp6,pyside_version)
            smsg += "{0}Python version: {1}<br>".format(sp6,sys.version)
            if getattr(sys, 'frozen', False):
                smsg += "{0}Running as a frozen binary.<br>".format(sp6)
            try:
                buildtime = time.ctime(os.path.getmtime(__file__))
                smsg += "{0}<b>Photox script (perhaps) last modified: {1}</b><br>".format(sp3,buildtime)
            except:
                pass
            smsg += "{0}Author: Nick Glazzard (nick.nos28@gmail.com)<br>".format(sp6)
            smsg += "{0}Script location: {1}<br>".format(sp6,self.photox.starting_dir)
            smsg += "{0}Debug level: {1}<br>".format(sp6,self.photox.debuglevel)
            smsg += "{0}<b>Window Geometry:</b><br>".format(sp3)
            smsg += "{0}Width = {1} pixels, Height = {2} lines, Aspect ratio = {3}<br>".\
                format(sp6,self.photox.width_pixels,self.photox.height_pixels,self.photox.aspect)
            smsg += "{0}<b>Image Database:</b><br>".format(sp3)
            smsg += "{0}Database folder: {1}<br>".format(sp6,self.photox.dbfolder)
            smsg += "{0}Database file: {1}<br>".format(sp6,self.photox.dbname)
            smsg += "{0}Earliest photograph in database: {1}<br>".format(sp6,photohack.time_to_exif(earliest_time))
            smsg += "{0}Latest photograph in database: {1}<br>".format(sp6,photohack.time_to_exif(latest_time))
            smsg += "{0}Image count: {1}<br>".format(sp6,len(self.photox.sortedinfotable))
            smsg += "{0}Image full res disk usage: {1:.1f} MBytes<br>".format(sp6,totalsize/1000000.0)
            smsg += "{0}Images with Exif: {1}<br>".format(sp6,num_exif)
            smsg += "{0}Images with geotags: {1}<br>".format(sp6,num_geotagged)
            smsg += "{0}Images with RAW version: {1}<br>".format(sp6,num_raw)
            smsg += "{0}Images from processing: {1}<br>".format(sp6,num_processed)
            smsg += "{0}Images deleted: {1}<br>".format(sp6,len(self.photox.deletedtable))
            smsg += "{0}Images with JFIF comments: {1}<br>".format(sp6,num_commented)
            smsg += "{0}Images with camera names: {1}<br>".format(sp6,num_cameraed)
            smsg += "{0}Images with vertical orientation: {1}<br>".format(sp6,num_vert)
            smsg += "{0}Images last added from folder: {1}<br>".format(sp6,self.photox.dirname)
            smsg += "{0}Number of camera types: {1}<br>".format(sp6,len(self.photox.cameras))
            smsg += "{0}Number of distinct tags: {1}<br>".format(sp6,num_known_tags)
            if self.savedtime == 0:
                smsg += "{0}Last saved: Not yet.<br>".format(sp6)
            else:
                smsg += "{0}Last saved: {1:.1f} minutes ago<br>".format(sp6,(time.time()-self.savedtime)/60.0)
            smsg += "{0}<b>Selection states:</b><br>".format(sp3)
            smsg += "{0}Images selected: {1}. {2} Images picked: {3}<br>".format(sp6,num_selected,sp9,num_picked)
            if self.photox.view_image_select == VIEW_PICK:
                selmode = 'Adding to pick.'
            elif self.photox.view_image_select == VIEW_UNPICK:
                selmode = 'Removing from pick.'
            else:
                selmode = 'Not picking.'
            smsg += "{0}Current picking action: {1}<br>".format(sp6,selmode)
            smsg += "{0}Current image index: {1}<br>".format(sp6,self.photox.selected_photo)
            if (self.photox.selected_photo >= 0) and (len(self.photox.sortedinfotable) > 0):
                if self.photox.debuglevel > 1:
                    print('showstatus(): self.photox.selected_photo =',self.photox.selected_photo)
                    print('... length of sortedinfotable =', len(self.photox.sortedinfotable))
                info = self.photox.sortedinfotable[self.photox.selected_photo]
                smsg += "{0}Current image date: {1}<br>".format(sp6,info['date'])
                if info['orient'] < 5:
                    restring = '{0}x{1}'.format(info['width'],info['height'])
                else:
                    restring = '{0}x{1}'.format(info['height'],info['width'])
                smsg += "{0}Current image resolution: {1}<br>".format(sp6,restring)
                camname = info['maker']+' '+info['model'].rstrip('\0')
                smsg += "{0}Current image camera: {1}<br>".format(sp6,camname)
                smsg += "{0}Current image orientation: {1}<br>".format(sp6,info['orient'])
                smsg += "{0}Current image tags: {1}<br>".format(sp6,self.photox.make_tag_string(info['tags']))
                if info['geotags']:
                    smsg += "{0}Current image location: {1:.4f},{2:.4f}<br>".format(sp6,info['lat'],info['long'])
                else:
                    smsg += "{0}Current image location: Unknown.<br>".format(sp6)
            smsg += "<br><br>"
            smsg += "{0}<b>Hot Key Help:</b><br>".format(sp3)
            if not self.is_macos: # Changing fonts in macOS Catalina in rich text does not currently work.
                smsg += "<font size=2><pre>"
                alt = "CTL"
            else:
                alt = "ALT"
            smsg += "  Image selection:<br>"
            smsg += "    Up Arrow: Up 1 year / Move zoom up.             Down Arrow: Down 1 year / Move zoom down.<br>"
            smsg += "    Left Arrow: Left 1 month/ Move zoom left.       "+alt+" + Left Arrow: Previous image.<br>"
            smsg += "    Right Arrow: Right 1 month / Move zoom right.   "+alt+" + Right Arrow: Next image.<br>"
            smsg += "    Space: Next image.                              "+alt+" + Space: Previous image.<br>"
            smsg += "    N: Next image.                                  P: Previous image.<br>"
            smsg += "  Zooming and panning:<br>"
            smsg += "    Set zoom box (region to zoom to):\n"
            if self.is_macos:
                smsg += "      [right mouse] + (drag)  OR  [cmd] + [left mouse] + (drag)\n"
            else:
                smsg += "      [right mouse] + (drag)  OR  [ctrl] + [left mouse] + (drag)\n"
            smsg += "    Drag image (set zoom center):\n"
            if self.is_macos:
                smsg += "      [middle mouse] + (drag) OR [alt] + [cmd] + [left mouse] + (drag)\n"
            else:
                smsg += "      [middle mouse] + (drag)\n"
            smsg += "    R: Reset Zoom.        Z: Zoom to box.           +: Zoom in.       -: Zoom out.<br>"
            smsg += "    [mouse wheel down]: Zoom in.                    [mouse wheel up]: Zoom out.\n"
            smsg += "  Viewing modes:<br>"
            smsg += "    H: Hide thumb and full photo. Show time chart only.<br>"
            smsg += "    T: Show thumb over time chart.<br>"
            smsg += "    V: View current photo high res.<br>"
            if False:
                # *** OBSOLETE HOT KEYS ***
                smsg += "  Picking and selecting images:<br>"
                smsg += "    B: Begin picking.                               "+alt+" + B: Add pick to selected.<br>"
                smsg += "    E: End picking.                                 "+alt+" + E: Current pick = selected. End picking.<br>"
                smsg += "    U: Begin unpicking.                             "+alt+" + U: Remove pick from selected.<br>"
                smsg += "    C: Clear pick.                                  "+alt+" + C: Delete images in 'saved' folder.<br>"
                smsg += "    A: Select all (reset selection).<br>"
                smsg += "    S: Copy current photo to 'saved' folder.        "+alt+" + S: Save all picked photos<br>"
                smsg += "  Tagging images:<br>"
                smsg += "    N: Add tags to current photo.                   "+alt+" + N: Set tags on current photo.<br>"
                smsg += "    M: Add tags to current photo and move to next.  "+alt+" + M: Set tags version.<br>"
                smsg += "  Image orientation:<br>"
                smsg += "    1-8: Set current photo orientation.<br>"
                smsg += "  Settings:<br>"
                smsg += "    "+alt+" + +: Increment time chart point size.       "+alt+" + -: Decrement time chart point size.<br>"
                smsg += "    D: Increment debug level.                       "+alt+" + D: Decrement debug level.<br>"
                smsg += "    Q or [escape]: Exit PhotoX.<br>"
            if not self.is_macos: # Changing fonts in macOS Catalina in rich text does not currently work.
                smsg += "</pre></font>"
            # Display it.
            statRect = QRect(10,10,610,500)
            self.statLabel = QLabel(smsg)
            self.scrollArea = QScrollArea()
            self.scrollArea.setGeometry(statRect)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWindowTitle("PhotoX Help and Status")
            self.scrollAreaWidgetContents = QWidget()
            self.scrollAreaWidgetContents.setGeometry(statRect)
            self.scrollArea.setWidget(self.statLabel)
            self.scrollArea.show()

        def closeEvent(self, event):
            """
            Intercept close program event to warn to save DB.
            """
            quit_msg = "Exit PhotoX? Database changes since last Save will be lost."
            reply = QMessageBox.question(self, 'PhotoX Exit Warning', quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._is_closing = True
                event.accept()
            else:
                event.ignore()

        def close_key_handler(self,event):
            """
            Exit if requested by hot key.
            """
            self.close()

    # Main line
    maintitle = "PhotoX: Synoptic Photo Collection Viewer and Tagger"
    app = QApplication([maintitle])
    dialog = PhotoxDialog()
    dialog.show()
    dialog.raise_() # Move it to the top.
    dialog.setWindowTitle(maintitle)
    if sys.platform.startswith('darwin'):
        ouricon = '/Applications/PhotoX.app/Contents/Resources/photox.png'
    else:
        ouricon = '/usr/local/applications/photox/photox.png'
    if not os.path.isfile( ouricon ):
        ouricon = 'photox.png'
    dialog.setWindowIcon(QIcon(ouricon))
    app.exec()
