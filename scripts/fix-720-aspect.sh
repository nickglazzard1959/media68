#!/bin/bash
rm -f /tmp/modasp.mp4
ffmpeg -i ${1}.mp4 -c copy -bsf:v h264_metadata=sample_aspect_ratio=64/45 /tmp/modasp.mp4
mv ${1}.mp4 ${1}-old.mp4
mv /tmp/modasp.mp4 ${1}.mp4
