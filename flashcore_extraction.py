from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium import webdriver
from datetime import datetime
# import pandas as pd
import random
import time
import json
import re
import os
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta
import os
import requests
import string
# import psycopg2
from check_points import *

def launch_navigator(url):
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-blink-features=AutomationControlled") 
	options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
	options.add_experimental_option("useAutomationExtension", False)
	options.add_argument(r"user-data-dir=/home/jorge/.config/google-chrome/")
	options.add_argument(r"profile-directory=Profile 6")

	drive_path = Service('/usr/local/bin/chromedriver')
	# drive_path = Service('/home/jorge/Work_may_2023/Mitsoku_project/Tool_TO_GET_PERSON_CONTACT/chrome_driver/chromedriver-linux64/chromedriver')
	driver = webdriver.Chrome(service=drive_path,  options=options)
	# driver = webdriver.Chrome(service=drive_path)
	driver.get(url)
	return driver

def int_folders():
	if not os.path.exists('check_points'):
		os.mkdir('check_points')
	if not os.path.exists('news_images'):
		os.mkdir('news_images')

def get_sports_links(driver):
	wait = WebDriverWait(driver, 10)
	buttonmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))
	buttonmore.click()
	
	dict_links = {}  

	list_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'menuMinority__item')))

	list_links = driver.find_elements(By.CLASS_NAME, 'menuMinority__item')

	for link in list_links:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		if sport_name == '':
			sport_name = sport_url.split('/')[-2].upper()
		dict_links[sport_name] = {'url':sport_url, 'enable':"True"}
		
	buttonminus = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))
	buttonminus.click()
	
	return dict_links

def wait_update_page(driver, url, class_name):
	current_tab = driver.find_element(By.CLASS_NAME, class_name)    
	driver.get(url)
	current_tab = wait.until(EC.staleness_of(current_tab))    
	
def find_ligues_torneos(driver):
	wait = WebDriverWait(driver, 10)
	ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))    
	ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
	dict_liguies = {}
	for ligue in ligues:
		dict_liguies['_'.join(ligue.text.split())] = ligue.get_attribute('href')
	return dict_liguies

def find_teams_players(driver):
	wait = WebDriverWait(driver, 10)
	xpath_expression = '//div[@class="menu selected-country-list leftMenu leftMenu--selected"]/div/a'
	teams_players = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))    
	teams_players = driver.find_elements(By.XPATH,xpath_expression)

	dict_teams_players = {}
	for team_player in teams_players:
		dict_teams_players['_'.join(team_player.text.split())] = team_player.get_attribute('href')
	return dict_teams_players

def getdb():
	return psycopg2.connect(
		#host="172.17.0.2",
		user="wohhu",
		password="panaJose",
	)

# con = getdb()

def get_sports_links(driver):
    wait = WebDriverWait(driver, 10)
    buttonmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))
    buttonmore.click()
    
    dict_links = {}  

    list_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'menuMinority__item')))

    list_links = driver.find_elements(By.CLASS_NAME, 'menuMinority__item')

    for link in list_links:
        sport_name = '_'.join(link.text.split())
        sport_url = link.get_attribute('href')
        if sport_name == '':
            sport_name = sport.get_attribute('href').split('/')[-2].upper()
        dict_links[sport_name] = sport_url
        
    buttonminus = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))
    buttonminus.click()
    
    return dict_links

def wait_update_page(driver, url, class_name):
    current_tab = driver.find_element(By.CLASS_NAME, class_name)    
    driver.get(url)
    current_tab = wait.until(EC.staleness_of(current_tab))    
    
def find_ligues_torneos(driver):
    wait = WebDriverWait(driver, 10)
    ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))    
    ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
    dict_liguies = {}
    for ligue in ligues:
        dict_liguies['_'.join(ligue.text.split())] = ligue.get_attribute('href')
    return dict_liguies

def find_teams_players(driver):
    wait = WebDriverWait(driver, 10)
    xpath_expression = '//div[@class="menu selected-country-list leftMenu leftMenu--selected"]/div/a'
    teams_players = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))    
    teams_players = driver.find_elements(By.XPATH,xpath_expression)

    dict_teams_players = {}
    for team_player in teams_players:
        dict_teams_players['_'.join(team_player.text.split())] = team_player.get_attribute('href')
    return dict_teams_players

def click_news(driver):
    wait = WebDriverWait(driver, 10)
    newsbutton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tabs__tab.news')))  # "tabs__tab news selected"
    newsbutton.click()


def click_news(driver):
	wait = WebDriverWait(driver, 10)
	newsbutton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tabs__tab.news')))  # "tabs__tab news selected"
	newsbutton.click()

def extract_news(driver):
	print("Extacting news: ")

def build_dict_urls(driver, dict_sports, 
			file_main_dict = 'check_points/flashscore_links.json',
			 dict_issues = 'check_points/flashscore_issues.json'):
	dict_urls = {}
	dict_with_issues = {}
	for sport, url_sport in dict_sports.items():
		try:
			step = 'sport_loop'
			print("Sport: ", url_sport)
			wait_update_page(driver, url_sport['url'], "container__heading")
			
			dict_ligues = find_ligues_torneos(driver)
			print('List liguies-torneos: ', print(len(dict_ligues)))
			dict_url_ligues_tournaments = {}
			
			for ligue_name, ligue_url in dict_ligues.items():
				step = 'ligue tornaments loop'
				print("############ Ligue: ", ligue_url)
				wait_update_page(driver, ligue_url, "container__heading")
				# wait_update_page(driver, ligue_url, "tabs__tab.summary selected")

				dict_teams_players = find_teams_players(driver)
				
				dict_teams_url = {}

				for team_player, url_team in dict_teams_players.items():            
					step = 'loop teams player'
					wait_update_page(driver, url_team, "heading__title")
					print("#"*30, "Team Player: ", url_team)

					print("Click on news: ")
					click_news(driver)
					extract_news(driver)
					url_news = driver.current_url
					dict_teams_url[team_player] = {'url_team':url_team, 'url_news':url_news}
				
				dict_url_ligues_tournaments[ligue_name] = dict_teams_url
				
			dict_urls[sport] = dict_url_ligues_tournaments
			save_check_point(file_main_dict, dict_urls)
			
		except:
			print("Don't found team player")
			dict_with_issues[sport] = {}
			dict_with_issues[sport] = {'step':step, 'url':url_sport['url']}
			save_check_point(dict_issues, dict_with_issues)

def process_date(date):
	try:
		date = datetime.strptime(date, date_format)
		return date
	except:
		return date

def save_image(driver, image_url, image_path):
	img_data = requests.get(image_url).content

	with open(image_path, 'wb') as handler:
		handler.write(img_data)

######################## NEWS EXTRACTION BLOCK 
def get_news_url_date(driver, source_new = 'Flashscore News'):
	date_format = "%d.%m.%Y %H:%M"
	# block to load more news links.
	# try:
	#     driver.find_element()# click on load more news.
	# except:
	#     pass
	wait = WebDriverWait(driver, 4)
	# resultnews = driver.find_element(By.ID, 'tournamentNewsTab')
	resultnews = wait.until(EC.visibility_of_element_located((By.ID, 'tournamentNewsTab')))
	if not resultnews.text == 'No news found.':

		block_news = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="fsNewsSection"]/a')))
		# block_news = driver.find_elements(By.XPATH, '//div[@class="fsNewsSection"]/a')
		flashscore_url = []
		for news in block_news:        
			if source_new in news.text:            
				date = news.find_element(By.XPATH, './/span[@data-testid="wcl-newsMetaInfo-date"]').text
				date = process_date(date)
				flashscore_url.append({'url':news.get_attribute('href'), 'date':date})
	else:
		print("Case no results")
		flashscore_url = []
	return flashscore_url

def load_detailed_news(driver, url_news):
	wait = WebDriverWait(driver, 10)
	class_name = 'fsNewsArticle__title'
	title = driver.find_elements(By.CLASS_NAME, class_name)
	driver.get(url_news)
	if len(title) == 0:
		title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
	else:
		wait.until(EC.staleness_of(title[0]))

def get_news_info(driver, date):
	# news_id      varchar(40),
 #    news_content varchar(4196),
 #    image        varchar(255),
 #    published    timestamp(6),
 #    news_summary varchar(512),
 #    news_tags    varchar(128),
 #    title        varchar(255)
	title = driver.find_element(By.CLASS_NAME, 'fsNewsArticle__title').text
	image = driver.find_element(By.XPATH, '//div[@class="imageContainer__element"]/figure/picture/img')
	image_url = image.get_attribute('src')
	articlebody = driver.find_element(By.CLASS_NAME, 'fsNewsArticle__content')
	summary = articlebody.find_element(By.XPATH, './/div[@class="fsNewsArticle__perex"]')
	body_html = articlebody.get_attribute('outerHTML')
	body_html = body_html.replace(str(summary.get_attribute('ourterHTML')), '')
	image_path = random_name(folder = 'news_images')
	save_image(driver, image_url, image_path)
	mentions = get_mentions(driver)

	dict_new = {'news_id':random_id(), 'title':title, 'news_summary':summary.text, 'news_content':body_html, 'image':image_path,
				'published':date,'news_tags': mentions}
	return dict_new

def random_name(folder = 'news_images'):
	file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	return os.path.join(folder,file_name + '.jpg')

def random_id():
	rand_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	return rand_id

def get_mentions(driver):
	mention_list = ''
	mentions = driver.find_elements(By.XPATH, '//div[@class="fsNewsArticle__mentions"]/a')
	for mention in mentions:
		if mention_list == '':
			mention_list = mention.text
		else:
			mention_list = mention_list +', '+mention.text
	return mention_list

def insertdb(q,d):
	cur = con.cursor()
	cur.execute(q, d)
	con.commit()
	# con.close()

def save_news_database(dict_news):	
	query = "INSERT INTO news VALUES(%(news_id)s, %(news_content)s, %(image)s, %(published)s, %(news_summary)s, %(news_tags)s, %(title)s)"
	# insertdb(q,dict_news)

def process_current_news_link(driver, current_news_link):
	driver.get(current_news_link)
	flashscore_url_news = get_news_url_date(driver)

	for url_date_news in flashscore_url_news:

		load_detailed_news(driver, url_date_news['url'])
		dict_new = get_news_info(driver, url_date_news['date'])
		save_news_database(dict_new)
		# dict to save in database dict_new
		save_news_database(dict_new)

def get_all_news(driver):
	dict_sports = load_json('check_points/dict_sports.json')
	for sport, dict_sport in dict_sports.items():
	    print("--------------------------- SPORT---------------------------")
	    for country, country_info in dict_sport.items():
	        print("--------------------------- COUNTRY-------------------")
	        for team, team_info in country_info.items():        
	            print("--------------------------- TEAM ------------")
	            print(team, team_info)
	            current_news_link = team_info['url_news']
	            print(current_news_link,'\n')
	            driver.get(current_news_link)	            
	            process_current_news_link(driver, current_news_link)

# int_folders()
# con.close()

def main():
	config_dict = load_json('check_points/config.json')

	driver = launch_navigator('https://www.flashscore.com')

	if config_dict['sports_link']:
		get_sports_links(driver)

	if config_dict['update_links']:
		build_dict_urls(driver, dict_sports, 
				file_main_dict = 'check_points/flashscore_links.json',
				 dict_issues = 'check_points/flashscore_issues.json')

	if config_dict['get_news']:
		get_all_news(driver)



if __name__ == "__main__":
	main()            

