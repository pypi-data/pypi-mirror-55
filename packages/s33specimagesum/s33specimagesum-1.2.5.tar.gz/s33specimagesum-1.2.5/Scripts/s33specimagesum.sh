#! /bin/bash
if [ -f "$HOME/Anaconda3/bin/python" ]; then
	ANACONDA_LOCATION="$HOME/Anaconda3"
elif [ -f "$HOME/anaconda3/python" ]; then
	ANACONDA_LOCATION="$HOME/anaconda3"
elif [ -f "/APSshare/anaconda3/x86_64/bin/python" ]; then
	ANACONDA_LOCATION=/APSshare/anaconda3/x86_64
else 
	echo "Cannot find Anaconda Python"
	exit 1

conda activate s33specimagesum

python -m 33specimagesum