#!/bin/bash
# Run MPV using a hack to determine if it was manually exited or not.
# You must also put this in: ~/.config/mpv/input.conf
# q quit 4
# 
rm -f /tmp/mpv-abort-flag
#mpv --no-audio-display -v --log-file=/dev/null "$1"
mpv --no-audio-display "$1"
status=$?

echo "Status = $status"
if [ $status -eq 4 ]; then
#    echo "YES"
    touch /tmp/mpv-abort-flag
#else
#    echo "NO"
fi
