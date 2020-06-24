#-*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------
# Define a library for Controlling Xvfb & Chrome / ChromDrive
# ----------------------------------------------------------------------------------------------------
# By ykh  2020. 01. 03.  Make a common module for controlling Xvfb & Chrome / ChromeDrive for Selenium
# ----------------------------------------------------------------------------------------------------

import os
import sys
import csv
import glob

import time
from datetime import date
from random import randint

import requests as rq
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
# For Simulate "Headless Mode" of Chrome
from xvfbwrapper import Xvfb
from bs4 import BeautifulSoup
from lxml import html, etree

import openpyxl

# sys.path.append("../../include")
# sys.path.append('~/sshutl_env/my_env')

# from ss_sys_data import *

# ----------------------------------------------
# Set Up X-Window / Headless Chrome for Crawling
# ----------------------------------------------

def set_chrome_ready_for_crawling(test_flag):

    # -----------------------
    # Create a Chrome Browser (in Virtual X-Window Mode / Not Visual)
    # -----------------------
    if (not test_flag):
        v_display = Xvfb(width=1280, height=740)
        v_display.start()
        chrome_options = webdriver.ChromeOptions()
        #    "download.default_directory" : "/home/ec2-user/download",
        prefs = {
            "download.default_directory" : "/home/kieshoon/다운로드",
            "profile.default_content_settings.popups" : False,
            "credentials_enable_service" : False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)

        # driver = webdriver.PhantomJS('/usr/bin/phantomjs')
    else:
        driver = webdriver.Chrome('/usr/bin/chromedriver')
        v_display = False

    return driver, v_display


def close_chrome_for_crawling (test_flag, driver, v_display):

        driver.quit() 
        if not (test_flag):
            v_display.stop()


