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
        chrome_options.add_argument('--lang=ko_KR_UTF-8')
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

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


def set_browser_ready_for_crawling(test_flag, browser_str='CHROME'):
    # -----------------------
    # Create a Chrome Browser (in Virtual X-Window Mode / Not Visual)
    # -----------------------
    if (not test_flag):
        v_display = Xvfb(width=1280, height=740)
        v_display.start()
        
        if browser_str == 'FIREFOX':
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.headless = True
            
            driver = webdriver.Firefox(options=firefox_options, executable_path='/usr/bin/geckodriver')
            # driver = webdriver.Firefox()
        else:

            # if browser_str == 'CHROME':
            chrome_options = webdriver.ChromeOptions()
            """
            prefs = {
                "download.default_directory" : "/home/ec2-user/download",
                "profile.default_content_settings.popups" : False,
                "credentials_enable_service" : False,
                "useAutomationExtension" : False,
                "chrome.page.customHeaders.referrer" : "http://www.ysl.com",
                "excludeSwitches" : ["enable-automation"]
            }
            chrome_options.add_experimental_option("prefs", prefs)
            """
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-proxy-server')
            chrome_options.add_argument('--no-referrers')
            chrome_options.add_argument('--lang=ko_KR.UTF-8')
            chrome_options.add_argument('--disable-blink-features')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            # chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36');
            # chrome_prefs = {}
            # chrome_prefs["chrome.page.customHeaders.referrer"] = 'http://www.ysl.com'  
            # chrome_options.experimental_options["prefs"] = chrome_prefs
            # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # chrome_options.add_experimental_option('useAutomationExtension', False)

            driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)

            print (" SET CHROME OPTIONS for YSL ")
 
    else:

         if browser_str == 'FIREFOX':
             driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
         else:
             driver = webdriver.Chrome('/usr/bin/chromedriver')
         v_display = False
 
    return driver, v_display


def close_browser_for_crawling (test_flag, driver, v_display):

        driver.quit() 
        if not (test_flag):
            v_display.stop()

