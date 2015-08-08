#!/bin/bash

TTY=`tty`
if [ "$TTY" = "/dev/tty1" ]
then
	cd /home/devel/github/venus_in_fur
	/usr/bin/python venus_in_fur.py
fi
