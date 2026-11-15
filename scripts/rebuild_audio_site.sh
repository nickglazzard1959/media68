#!/bin/bash
echo "Rebuild audio media static website."
echo "Assumes /mnt/audiolib is aliased to external-files2."
echo "Index file is aindex.html."
a68g files_to_html.a68 -- -r /mnt/audiolib/ -o audio_site -p audio -v -e '.flac,.mp3' --multi -f external-files2 -i aindex.html -a -t "Music Collection"
