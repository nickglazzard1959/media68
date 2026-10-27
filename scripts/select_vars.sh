#!/bin/bash
#
# Source this to set up environment variables for the media68 programs.
# Before that, edit it as necessary.
#
# Where is the media68 software?
export MEDIA68_HOME="/home/nick/gitprojects/media68"
#
# Where are the internet radio stream definition (.m3u) files?
export RADIO68_LISTS="${MEDIA68_HOME}/radio_lists"
#
# Where are the top level directories for the various media libraries?
export VIDEO68_MOUNT="/mnt/videolib"
export AUDIO68_MOUNT="/mnt/audiolib"
export BOOKS68_MOUNT="/mnt/booklib"
#
# Which program is to be used to view PDF files?
export BOOKS68_VIEWER="atril"
#
# --- DO NOT CHANGE BELOW THIS POINT ---
#
export RADIO68_PGM=${MEDIA68_HOME}
export VIDEO68_PGM=${MEDIA68_HOME}
export AUDIO68_PGM=${MEDIA68_HOME}
export BOOKS68_PGM=${MEDIA68_HOME}
