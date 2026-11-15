#!/bin/bash
echo "Rebuild video media static website."
echo "Assumes /mnt/videolib is aliased to external-files."
echo "Index file is vindex.html."
a68g files_to_html.a68 -- -o video_site -v -p video -r /mnt/videolib -f external-files -i vindex.html -t "Film and TV Collection"
