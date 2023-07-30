#!/bin/bash

SCRIPTS_PATH="/var/scripts"

bash $SCRIPTS_PATH/gitserver-configure.sh
bash $SCRIPTS_PATH/ssh-configure.sh
bash $SCRIPTS_PATH/set-ssh-root-password.sh
bash $SCRIPTS_PATH/set-htpasswd-root.sh
bash $SCRIPTS_PATH/add-ssh-keys.sh

/etc/init.d/fcgiwrap start
/usr/bin/supervisord