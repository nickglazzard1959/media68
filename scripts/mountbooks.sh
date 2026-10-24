#!/bin/bash
echo "Mount NUC1 book library on /mnt/booklib."
sudo mount -t cifs -o username=nick,password=12345678 //nuc1/booklib /mnt/booklib
echo "Done."
