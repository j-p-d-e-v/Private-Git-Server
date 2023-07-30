#!/bin/bash
cd ~
mkdir /var/run/sshd
mkdir .ssh && chmod 700 .ssh
touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys