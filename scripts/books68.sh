#!/bin/bash

if [ -z "$BOOKS68_PGM" ]; then
    echo "Env var BOOKS68_PGM is not set. Set it to the location of the program."
    exit 1
fi

if [ -z "$BOOKS68_MOUNT" ]; then
    echo "Env var BOOKS68_MOUNT is not set. Set it to the mount point of the book assets."
    exit 1
fi

if [ -z "$BOOKS68_VIEWER" ]; then
    echo "Env var BOOKS68_VIEWER is not set. Set it to the name of the program used to display books."
    exit 1
fi

cd ${BOOKS68_PGM}

# The program/command you want to run
PROGRAM="a68g select68.a68 -- --root ${BOOKS68_MOUNT} --title books68 -e '.pdf' -n -p ${BOOKS68_VIEWER}" 

# 1. Probe for the best terminal launcher utility
if command -v xdg-terminal-exec &> /dev/null; then
    TERM_CMD="xdg-terminal-exec"
elif command -v x-terminal-emulator &> /dev/null; then
    TERM_CMD="x-terminal-emulator"
# 2. Fall back to common native Wayland/Modern desktop terminals
elif command -v gnome-terminal &> /dev/null; then
    TERM_CMD="gnome-terminal"
elif command -v konsole &> /dev/null; then
    TERM_CMD="konsole"
elif command -v xfce4-terminal &> /dev/null; then
    TERM_CMD="xfce4-terminal"
# 3. Last resort legacy fallback
elif command -v xterm &> /dev/null; then
    TERM_CMD="xterm"
else
    echo "Error: No suitable terminal emulator found." >&2
    exit 1
fi

# Determine execution syntax (Modern '--' vs older '-e')
if [[ "$TERM_CMD" == "gnome-terminal" || "$TERM_CMD" == "xdg-terminal-exec" ]]; then
    # Modern syntax
    $TERM_CMD -- $PROGRAM &
else
    # Legacy fallback syntax (used by xmin/xterm/older apps)
    $TERM_CMD -e "$PROGRAM" &
fi

# Detach the terminal process cleanly from the script
disown
echo "Launched $PROGRAM in $TERM_CMD (detached)."
