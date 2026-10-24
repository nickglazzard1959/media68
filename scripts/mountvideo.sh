#!/bin/bash
echo "Mount NUC1 video library link farm on /mnt/videolib."
sudo mount -t cifs -o username=nick,password=12345678 //nuc1/videolib /mnt/videolib
echo "Done."
