#!/bin/bash
echo "Mount NUC1 photo library link farm on /mnt/photolib."
sudo mount -t cifs -o username=nick,password=12345678,uid=nick,gid=nick,noforceuid,noforcegid //nuc1/photolib /mnt/photolib
echo "Done."
