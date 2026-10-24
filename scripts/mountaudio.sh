#!/bin/bash
echo "Mount Moode player audio library on /mnt/audiolib."
sudo mount -t cifs -o username=nick,password=12345678,iocharset=utf8 //music/f9ede56b-640e-4130-aef9-39dda052a257/newaudio /mnt/audiolib
echo "Done."
