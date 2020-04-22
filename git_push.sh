#!/bin/sh
function help () {
echo "git_push - Script that pushes code to git with user provided description."
	echo "Usage: $0 description"
	echo "* description: user provides general description on updates to code, surrounded by quotes"
}

#show help if not
if [ ${#@} == 1 ]; 
then
#User inputs
description=${1}

sudo git add --all
sudo git commit -m "$description"
sudo git push

else
	help

fi
