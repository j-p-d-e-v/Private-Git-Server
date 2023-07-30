#!/bin/bash

ssh_keys_directory="/tmp/ssh-keys"

for ssh_key in `ls ${ssh_keys_directory}`; do
    cat $ssh_keys_directory/$ssh_key >> ~/.ssh/authorized_keys 
    echo "$ssh_keys_directory/$ssh_key has been added to authorized_keys"
done