#!/bin/bash

#Initialize virtual environment
python3 -m venv webex-env

#Activate venv
source ./webex-env/bin/activate

#Upgrade pip
pip install --upgrade pip

#Install selenium
pip3 install selenium

#Move chromedriver (chrome version 88.0) to /usr/bin directory
echo
echo "SUDO permissions required in order to move chromedriver to /usr/bin dir"
sudo mv ./chromedriver /usr/bin

exit
