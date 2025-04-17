#!/bin/bash

user=$(awk -F: '$3 >= 1000 && $1 != "nobody" { print $1; exit }' /etc/passwd)

export HOME="/home/$user"
export XAUTHORITY="$HOME/.Xauthority"
export DISPLAY=:0

rm -rf /tmp/.X11-unix /tmp/.X0-lock 2>/dev/null
pkill -x X  

# 3. Start the X server and run that user's .xinitrc
xinit "/home/$user/.xinitrc" -- /usr/bin/X -nolisten tcp vt1
