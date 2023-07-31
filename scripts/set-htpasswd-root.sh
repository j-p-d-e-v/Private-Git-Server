#!/bin/bash

htpasswd_file="/var/git/htpasswd"

if [ ! -f "$htpasswd_file" ]; then
    touch $htpasswd_file
fi

htpasswd -bB $htpasswd_file root ${ROOT_PASSWORD}
