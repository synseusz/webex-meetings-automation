#!/bin/bash

#Initialize virtual environment
python3 -m venv webex-env

#Activate venv
source ./webex-env/bin/activate

#Upgrade pip
pip install --upgrade pip

#Install selenium
pip3 install selenium

exit
