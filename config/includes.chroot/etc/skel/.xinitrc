#!/bin/sh

export DISPLAY=:0

openbox-session &
/opt/bootScreen/boot_screen.py &
sleep 5
/opt/login/login_screen.py 
