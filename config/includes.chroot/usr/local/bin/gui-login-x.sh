#!/bin/bash

user=$(awk -F: '$3 >= 1000 && $1 != "nobody" { print $1; exit }' /etc/passwd)

export HOME="/home/$user"
export XAUTHORITY="$HOME/.Xauthority"
export DISPLAY=:0

# 3. Start the X server and run that user's .xinitrc
xinit "/home/$user/.xinitrc" -- /usr/bin/X -nolisten tcp vt1
