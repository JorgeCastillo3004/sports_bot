from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import date, timedelta, datetime
from selenium import webdriver
import chromedriver_autoinstaller
import random
import string
import requests
import json
import os
import re

from common_functions import *

import time
driver = launch_navigator('https://www.flashscore.com', False)
wait = WebDriverWait(driver, 10)
# user_menu = driver.find_element(By.ID,'user-menu')
user_menu = wait.until(EC.element_to_be_clickable((By.ID, 'user-menu')))
print(user_menu.text)

time.sleep(4)
driver.quit()