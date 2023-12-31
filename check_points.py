import json
import os
from selenium import webdriver
from datetime import date, timedelta
#####################################################################
#					CHECK POINTS BLOCK 								#
#####################################################################

def load_json(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:        
        json_object = json.load(openfile)
    return json_object

def save_check_point(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def load_check_point(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
    else:
        json_object = {}
    return json_object

def check_previous_execution(file_path = 'check_points/scraper_control.json'):
    if os.path.isfile(file_path):
        dict_scraper_control = load_json(file_path)
    else:
        dict_scraper_control = {}
    return dict_scraper_control