#!/bin/bash

TARGET_USER="$1"

if [ -z "$TARGET_USER" ]; then
    echo "Username not provided."
    exit 1
fi

USER_HOME="/home/$TARGET_USER"
USER_ID=$(id -u "$TARGET_USER")

export HOME="$USER_HOME"
export USER="$TARGET_USER"
export LOGNAME="$TARGET_USER"
export XDG_RUNTIME_DIR="/run/user/$USER_ID"
export SHELL="/bin/bash"

feh --bg-scale /opt/wallpapers/desktop_wallpaper1.jpg &
picom --config ~/.config/picom/picom.conf --experimental-backends &
sleep 1
openbox-session & /opt/desktop/desktop_screen.py &
idesk 

