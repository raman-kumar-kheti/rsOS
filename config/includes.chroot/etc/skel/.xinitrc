#!/bin/sh

export DISPLAY=:0

/opt/bootScreen/boot_screen.py &
sleep 3
/opt/login/login_screen.py 
