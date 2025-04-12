#!/bin/bash

TARGET_USER="$1"

if [ -z "$TARGET_USER" ]; then
    echo "Username not provided."
    exit 1
fi

USER_HOME="/home/$TARGET_USER"

export HOME="$USER_HOME"
export USER="$TARGET_USER"
export LOGNAME="$TARGET_USER"
export XDG_RUNTIME_DIR="/run/user/$(id -u $TARGET_USER)"
export SHELL="/bin/bash"


rm -rf /tmp/.X11-unix /tmp/.X0-lock 2>/dev/null

pkill -x  X

exec openvt -f -c 1 -- su - "$TARGET_USER"