#!/bin/bash
#
# Install some media68 components.
#
BIN_PATH="/usr/local/bin"
sudo cp scripts/video68.sh ${BIN_PATH}
sudo cp scripts/audio68.sh ${BIN_PATH}
sudo cp scripts/books68.sh ${BIN_PATH}
sudo cp scripts/radio68.sh ${BIN_PATH}
sudo cp mpv-run.sh ${BIN_PATH}
#
MPV_CONF_DIR="${HOME}/.config/mpv"
if [ ! -d "$MPV_CONF_DIR" ]; then
    mkdir -p "$MPV_CONF_DIR"
fi
cp input.conf "$MPV_CONF_DIR"
