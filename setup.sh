#!/bin/bash

cleanup() {
	# remove tty script from /root/.bashrc
	sed -i '/tty.sh$/d' /root/.bashrc
}

# check if the files exists
if [ ! -f venus_in_fur.py ]
then
	echo "the scripts are missing!"
	exit -1
fi

if [ "$1" == "--clean" ]
then
	cleanup
	exit 0
fi

cleanup

# update the /root/.bashrc file, cos iin order to get the sound
# right, we need to use a tty
echo "$PWD/tty.sh" >> /root/.bashrc
