#!/bin/bash
echo "root:${ROOT_PASSWORD}" | chpasswd
echo "[INFO]: Please restart the sshd supervisor process if you manually executed this script."