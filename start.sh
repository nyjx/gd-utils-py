#!/bin/sh
mkdir -p /gd-utils-py/files/validate

while true; do
    if [ -e /gd-utils-py/exit ]; then
        rm -rf /gd-utils-py/exit
        break
    fi
    wait
done
echo "exiting docker container"