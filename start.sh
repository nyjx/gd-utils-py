#!/bin/sh
mkdir -p /gd-utils-py/files/validate

while true; do
    if [ -e /gd-utils-py/exit ]; then
        break
    fi
    wait
done
echo "exiting docker container"