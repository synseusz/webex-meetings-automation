#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import sys
import getpass
import time

user_home_dir = os.getenv('HOME')
chrome_profile_path = "user-data-dir=%s/.config/google-chrome/Webex"%(user_home_dir)
options = Options()
options.add_argument(chrome_profile_path)

driver = webdriver.Chrome(options = options)
driver.get('https://ibm.webex.com/webappng/sites/ibm/dashboard?siteurl=ibm')

logged_in = False
meeting_host = sys.argv[1]

def w3_login():
	global logged_in
	sign_in_btn = driver.find_element_by_xpath('//*[@id="guest_signin_button"]')
	sign_in_btn.click()

	try:
		IBM_email_field = driver.find_element_by_xpath('//*[@id="desktop"]')
		IBM_passwd_field = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/form/input[4]")

		if os.getenv('W3_USER') and os.getenv('W3_PASSWD'):
			print("Found saved credentials\nLogging in...\n")
			IBM_email_field.click()
			IBM_email_field.send_keys(os.getenv('W3_USER'))
			time.sleep(1)
			IBM_passwd_field.click()
			IBM_passwd_field.send_keys(os.getenv('W3_PASSWD'))

			logged_in = True

		else:
			print("No saved credentials")
			while True:
				IBM_email_field.click()
				email_input = input("Please enter your W3 email: ")
				if len(email_input) > 0 and '@' in email_input:
					os.environ['W3_USER'] = email_input
					IBM_email_field.send_keys(email_input)
					break
				else:
					print("Invalid email address\nTry again!\n")
			while True:
				IBM_passwd_field.click()
				passwd_input = getpass.getpass("Please enter your W3 password: ")
				if len(passwd_input) > 0:
					os.environ['W3_PASSWD'] = passwd_input
					IBM_passwd_field.send_keys(passwd_input)
					break
				else:
					print("Invalid password\nTry again!\n")

			#escape special characters colliding with shell
			filtered_passwd = escape_special_chars(passwd_input)
			
			#export into venv
			export1 = "export W3_USER='%s'"%(email_input)
			export2 = "export W3_PASSWD='%s'"%(filtered_passwd)
			os.system('echo %s >> ./webex-env/bin/activate'%(export1))
			os.system('echo %s >> ./webex-env/bin/activate'%(export2))

		time.sleep(1)
		sign_in_btn = driver.find_element_by_xpath('//*[@id="btn_signin"]')
		sign_in_btn.click()

		logged_in = True

	except:
		print("Already logged in to W3 intranet")
		logged_in = True

def escape_special_chars(passwd_input):
	special_chars = ['>', '<', '$', '%', '&', '(', ')']

	for special_char in special_chars:
		if special_char in passwd_input:
			passwd_input = passwd_input.replace(special_char, '\\%s'%(special_char))
	return passwd_input

def join_meeting(host):
    search_input_field = driver.find_element_by_xpath('//*[@id="autoSearchInput"]')
    search_input_field.click()

    search_input_field.send_keys(host)
    try:
        time.sleep(3)
        join_btn = driver.find_element_by_xpath('/html/body/div[4]/span/div/div[1]/div/div[2]/section/a/div/div[4]/button')
        join_btn.click()
    except:
        time.sleep(2)
        join_btn = driver.find_element_by_xpath('/html/body/div[4]/span/div/div[1]/div/div[2]/section/a/div/div[4]/button')
        join_btn.click()

    time.sleep(5)
    driver.switch_to_frame("pbui_iframe")

    try:
        dialog_mask = driver.find_element_by_class_name('dialog-mask')
        got_it_btn = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div[1]/button')
        got_it_btn.click()
    except:
        pass

    mute_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div/button')
    stop_video_btn = driver.find_element_by_xpath('//*[@id="meetingSimpleContainer"]/div[3]/div[2]/div[2]/div/button/span[2]')

    # Mic and Camera state check
    if mute_btn.text == "Mute":
        mute_btn.click()
    elif mute_btn.text == "Unmute":
        pass
    else:
        print("Current mic state - ",mute_btn.text)

    if stop_video_btn.text == "Stop video":
        stop_video_btn.click()
    elif stop_video_btn.text == "Start video":
        pass
    else:
        print("Current camera state - ",stop_video_btn.text)

    time.sleep(1)
    join_meeting_btn = driver.find_element_by_xpath('//*[@id="interstitial_join_btn"]')
    join_meeting_btn.click()

###############################################################################

def main():
    if logged_in:
        print("Logged in to Webex")
        print("Searching for a meeting with - ",meeting_host)

        join_meeting(meeting_host)

    elif not logged_in:
        print("\nYou are not logged in to Webex\nAttempting to login...\n")
        w3_login()
        time.sleep(10)
        main()

main()