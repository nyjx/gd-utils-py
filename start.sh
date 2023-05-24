#!/bin/sh
mkdir -p /gd-utils-py/files/validate

while true; do
    if [ -e /gd-utils-py/exit ]; then
        rm -rf /gd-utils-py/exit
        break
    fi
    sleep 10
done
echo "exiting docker container"