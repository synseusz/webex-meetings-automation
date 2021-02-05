#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import sys
import getpass
import time

chrome_profile_path = "user-data-dir=/home/piotr/.config/google-chrome/Webex"
options = Options()
options.add_argument(chrome_profile_path)

driver = webdriver.Chrome(options = options)
driver.get('https://ibm.webex.com/webappng/sites/ibm/dashboard?siteurl=ibm')

logged_in = False

print("Meeting with - %s"%(sys.argv[1]))