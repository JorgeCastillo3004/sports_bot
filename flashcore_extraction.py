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
import random
import time
import json
import re
import os
from selenium.webdriver.support.ui import Select

local_time_naive = datetime.now()
utc_time_naive = datetime.utcnow()
time_difference_naive = utc_time_naive - local_time_naive

from datetime import date, timedelta
import os
import requests
import string
import psycopg2
from check_points import *

def launch_navigator(url):
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-blink-features=AutomationControlled") 
	options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
	options.add_experimental_option("useAutomationExtension", False)	
	options.add_argument('--headless') #test-
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')

	options.add_argument(r"user-data-dir=/home/jorge/.config/google-chrome/")
	options.add_argument(r"profile-directory=Profile 6")


	drive_path = Service('/usr/local/bin/chromedriver')

	driver = webdriver.Chrome(service=drive_path,  options=options)
	driver.get(url)
	return driver

def int_folders():
	if not os.path.exists('check_points'):
		os.mkdir('check_points')
	# if not os.path.exists('news_images'):
	# 	os.mkdir('news_images')
	if not os.path.exists('logo_images'):
		os.mkdir('logo_images')
	if not os.path.exists('images'):
		os.mkdir("images")
	if not os.path.exists('images/news'):
		os.mkdir("images/news")
	if not os.path.exists('images/news/small_images'):
		os.mkdir("images/news/small_images/")
	if not os.path.exists('images/news/full_images'):
		os.mkdir("images/news/full_images/")

def get_sports_links_news(driver):
	wait = WebDriverWait(driver, 1)
	buttonmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'arrow.topMenuSpecific__moreIcon')))

	mainsports = driver.find_elements(By.XPATH, '//div[@class="topMenuSpecific__items"]/a')

	dict_links = {}

	for link in mainsports[1:]:		
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		if sport_name != '':			
			dict_links[sport_name] = sport_url	
	buttonmore.click()

	list_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'topMenuSpecific__dropdownItem')))
	list_links = driver.find_elements(By.CLASS_NAME, 'topMenuSpecific__dropdownItem')

	for link in list_links:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')		
		if sport_name == '':
			sport_name = sport_url.split('/')[-2].upper()
		dict_links[sport_name] = sport_url

	buttonminus = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'arrow.topMenuSpecific__moreIcon')))
	buttonminus.click()
	return dict_links

def get_list_recent_news(driver):
	# container_news = driver.find_elements(By.XPATH, '//div[@data-testid="wcl-elementBodyNews" and contains(.,"More Football News")]/div/a')
	wait = WebDriverWait(driver, 10)
	webdriver.ActionChains(driver).send_keys(Keys.END).perform()
	xpath_expression = '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'
	container_news = driver.find_elements(By.XPATH, xpath_expression)
	list_upate_news = []
	for block in container_news:
		news_link = block.get_attribute('href')
		news_date = block.find_element(By.CLASS_NAME, '_newsMeta_gh8ui_5').text
		data_utc = process_date(news_date)
		title = block.find_element(By.XPATH, './/div[@role="heading"]').text
		image = wait.until(EC.element_to_be_clickable((By.XPATH, './/figure/picture/img')))
		image = image.get_attribute('src')
		# image_url = block.find_element(By.XPATH, './/figure/picture/source').get_attribute('srcset').split(', ')[0]
		# image_url = re.sub(r'\s+\d+\w','', image_url)
	#     if title not in database:
		if True:
			image_path_small = random_name(folder = 'images/news/small_images', termination = '.avif')
			# save_image(driver, image_url, image_path_small)
			dict_current_news = {'title':title, 'published':data_utc, 'image_path_small':image_path_small, 'news_link':news_link} 
			list_upate_news.append(dict_current_news)
	return list_upate_news

def click_show_more_news(driver):
	wait = WebDriverWait(driver, 5)
	click_more = True
	count = 0 
	showmore = driver.find_elements(By.CLASS_NAME, 'showMore.showMore--fsNews')
	if len(showmore)!= 0:
		click_more = True
	else:
		click_more = False
	container_news = driver.find_elements(By.XPATH, '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a')
	print(len(container_news))
	current_len = len(container_news)
	while click_more:
		print("Count: ", count)
		showmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'showMore.showMore--fsNews')))
		showmore.click()
		new_len = current_len
		while current_len == new_len:
			time.sleep(0.8)
			new_len = len(driver.find_elements(By.XPATH, '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a'))
		time.sleep(1)
		webdriver.ActionChains(driver).send_keys(Keys.END).perform()
		webdriver.ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

		showmore = driver.find_elements(By.CLASS_NAME, 'showMore.showMore--fsNews')
		if len(showmore)== 0:
			click_more = False
		container_news = driver.find_elements(By.XPATH, '//div[@class="fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped"]/a')
		print("Total news found: ", len(container_news))

def find_ligues_torneos(driver):
	wait = WebDriverWait(driver, 10)
	ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))    
	ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
	dict_liguies = {}
	for ligue in ligues:
		dict_liguies['_'.join(ligue.text.split())] = ligue.get_attribute('href')
	return dict_liguies

def getdb():
	return psycopg2.connect(
                host="localhost",
                user="wohhu",
                password="caracas123",
        dbname='sports_db',
        )

def get_sports_links(driver):
	wait = WebDriverWait(driver, 10)
	buttonmore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))

	mainsports = driver.find_elements(By.XPATH, '//div[@class="menuTop__items"]/a')

	dict_links = {}

	for link in mainsports:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		dict_links[sport_name] = sport_url

	buttonmore.click()

	list_links = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'menuMinority__item')))

	list_links = driver.find_elements(By.CLASS_NAME, 'menuMinority__item')

	for link in list_links:
		sport_name = '_'.join(link.text.split())
		sport_url = link.get_attribute('href')
		if sport_name == '':
			sport_name = sport_url.split('/')[-2].upper()
		dict_links[sport_name] = sport_url
		
	buttonminus = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'menuMinority__arrow')))
	buttonminus.click()
	
	return dict_links

def wait_update_page(driver, url, class_name):
	wait = WebDriverWait(driver, 10)
	current_tab = driver.find_elements(By.CLASS_NAME, class_name)
	driver.get(url)

	if len(current_tab) == 0:		
		current_tab = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
	else:
		element_updated = wait.until(EC.staleness_of(current_tab[0]))		
	
def find_ligues_torneos(driver):
	wait = WebDriverWait(driver, 5)
	ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))    
	ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
	dict_liguies = {}
	for ligue in ligues:
		dict_liguies['_'.join(ligue.text.split())] = ligue.get_attribute('href')
	return dict_liguies

def find_teams_players(driver):
	wait = WebDriverWait(driver, 4)
	try:
		xpath_expression = '//div[@class="menu selected-country-list leftMenu leftMenu--selected"]/div/a'
		teams_players = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))    
		teams_players = driver.find_elements(By.XPATH,xpath_expression)
		dict_teams_players = {}
		for team_player in teams_players:
			dict_teams_players['_'.join(team_player.text.split())] = team_player.get_attribute('href')
	except:
		dict_teams_players = {}
	return dict_teams_players

def click_news(driver):
	wait = WebDriverWait(driver, 10)
	newsbutton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tabs__tab.news')))  # "tabs__tab news selected"
	newsbutton.click()

def extract_news(driver):
	print("Extacting news: ")

def get_ligues_data(driver):
	block_ligue_team = driver.find_element(By.CLASS_NAME, 'container__heading')
	sport = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[1]').text
	country = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[2]').text
	name_ligue_tournament = block_ligue_team.find_element(By.CLASS_NAME,'heading__title').text
	temporada = block_ligue_team.find_element(By.CLASS_NAME, 'heading__info').text
	image_url = block_ligue_team.find_element(By.XPATH, './/div[@class= "heading"]/img').get_attribute('src')
	image_path = random_name(folder = 'logo_images')
	save_image(driver, image_url, image_path)
	league_id = random_id()
	ligue_tornamen = {"league_id":league_id, 'sport':sport, 'league_country': country,
					 'league_name': name_ligue_tournament,
					'temporada':temporada, 'league_logo':image_path}
	ligue_tornamen['league_name_i18n'] = 'ADITIONAL'
	return ligue_tornamen

def get_news_info(driver, date):
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
	dict_news = {'news_id':random_id(), 'title':title, 'news_summary':summary.text,
				 'news_content':body_html, 'image':image_path,
				'published':date,'news_tags': mentions}	
	dict_max_len = {'news_id':40, 'title':400, 'news_summary':8196, 'news_content':16392, 'news_tags':255}
	for field_name, max_len in dict_max_len.items():
		if len(str(dict_news[field_name])) > max_len:
			print(field_name, "Exceed max len: ", max_len,'/',len(str(dict_news[field_name])))
	for key, field in dict_news.items():
		print(key, len(str(field)), end='--')
	dict_news = {'news_id':random_id(), 'title':title, 'news_summary':summary.text,
				 'news_content':body_html[0:16392], 'image':image_path,
				'published':date,'news_tags': mentions}
	input_user = input("Type s to continue: ")
	return dict_news

def build_dict_urls(driver, dict_sports, file_main_dict = 'check_points/flashscore_links.json',dict_issues = 'check_points/flashscore_issues.json', flag_news = False):

	dict_urls = load_json('check_points/flashscore_links.json')

	# sports_ready = check_previous_execution(file_path = 'check_points/scraper_control.json')

	dict_check_point = check_previous_execution(file_path = 'check_points/check_point_URL_extraction.json')

	sports_ready = check_previous_execution(file_path = 'check_points/scraper_control_get_URL.json')

	if len(dict_check_point) == 0:
		print("Initialization")
		dict_check_point = {'country':'', 'ligue_tournament':''}
		continue_country = True
		continue_ligue_tournament = True
	else:    
		continue_country = False
		continue_ligue_tournament = False

	dict_with_issues = {}
	for sport, url_sport in dict_sports.items():
		try:
			print("Current sport: ", sport)
			if sport in sports_ready.keys():
				pass
				print(sport, "Ready")
			else:
				step = 'sport_loop'
				print("Start process: ", sport, url_sport)
				wait_update_page(driver, url_sport, "container__heading")
				
				dict_countries = find_ligues_torneos(driver)
				print('List liguies-torneos: ', len(dict_countries) )

				try:
					dict_url_ligues_tournaments = dict_urls[sport]
				except:
					dict_url_ligues_tournaments = {}

				for country, country_url in dict_countries.items():
					if country == dict_check_point['country']:
						continue_country = True

					if continue_country:
						try:
							dict_teams_url = dict_urls[sport][country]
						except:
							dict_teams_url = {}

						step = 'Country'
						dict_check_point['country'] = country
						print(" "*15, "############ Ligue: ", country_url)
						wait_update_page(driver, country_url, "container__heading")

						dict_ligues_tournaments = find_teams_players(driver)						
						
						if len(dict_ligues_tournaments)!= 0:
							for ligue_tournament, ligue_tornament_url in dict_ligues_tournaments.items():
								if dict_check_point['ligue_tournament'] == ligue_tournament:
									continue_ligue_tournament = True
							
								if continue_ligue_tournament:

									step = 'loop teams player'								
									wait_update_page(driver, ligue_tornament_url, "heading__title")
									ligue_tornamen_info = get_ligues_data(driver)
									# save_ligue_tornament_info(ligue_tornamen_info) #test-
									print("#"*30, "LIGUE-TOURNAMENTS: ", ligue_tornament_url)

									print("Click on news: ")
									click_news(driver)
									if flag_news:
										process_current_news_link(driver, driver.current_url)								
										wait_update_page(current_url)

									url_news = driver.current_url
									dict_teams_url[ligue_tournament] = {'url':ligue_tornament_url, 'url_news':url_news}
									dict_check_point['ligue_tournament'] = ligue_tournament
									save_check_point('check_points/check_point_URL_extraction.json', dict_check_point)									
							
									dict_url_ligues_tournaments[ligue_tournament] = dict_teams_url
									dict_urls[sport] = dict_url_ligues_tournaments
									save_check_point(file_main_dict, dict_urls)
						else:
							ligue_tornamen_info = get_ligues_data(driver)
							save_ligue_tornament_info(ligue_tornamen_info)
							click_news(driver)
							url_news = driver.current_url
							process_current_news_link(driver, url_news)
							dict_url_ligues_tournaments[ligue_tournament] = {'url':ligue_url, 'url_news':url_news}
					
							dbdict_urls[sport] = dict_url_ligues_tournaments
							save_check_point(file_main_dict, dict_urls)
				sports_ready[sport] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
				save_check_point('check_points/scraper_control_get_URL.json', sports_ready)
					
		except:
			print("-*-*", end='')
			dict_with_issues[sport] = {'step':step, 'url':url_sport}
			save_check_point('check_points/flashscore_issues.json', dict_with_issues)

def process_date(date):
	date_format = "%d.%m.%Y %H:%M:%S"
	if 'min ago' in date:		
		min_ = int(re.findall(r'(\d+)\ min ago', date)[0])        
		news_time_post = local_time_naive - timedelta(minutes=min_)
	elif ' h ago' in date:
		hours_ = int(re.findall(r'(\d+)\ h ago', date)[0])        
		news_time_post = local_time_naive - timedelta(hours=hours_)
	elif 'Yesterday' in date:
		previous_day = local_time_naive - timedelta(days=1)
		time_post = re.findall(r'\d+:\d+', date)[0]+':00'
		time_post = datetime.strptime(time_post, "%H:%M:%S")
		news_time_post = datetime(
			previous_day.year,
			previous_day.month,
			previous_day.day,
			time_post.hour,
			time_post.minute,
			time_post.second,
		)
	elif 'Just now' in date:
		news_time_post = local_time_naive
	else:		
		date = date +':00'
		news_time_post = datetime.strptime(date, date_format)	

	news_utc_time = news_time_post + time_difference_naive
	return news_utc_time

def save_image(driver, image_url, image_path):
	img_data = requests.get(image_url).content

	with open(image_path, 'wb') as handler:
		handler.write(img_data)

######################## NEWS EXTRACTION BLOCK 
def get_news_url_date(driver, current_news_link, source_new = 'Flashscore News'):
	wait = WebDriverWait(driver, 15)
	newsresult = driver.find_elements(By.ID, 'tournamentNewsTab')
	driver.get(current_news_link)
	if len(newsresult) == 0:
		newsresult = wait.until(EC.presence_of_all_elements_located((By.ID, 'tournamentNewsTab')))
	else:
		newsupdate = wait.until(EC.staleness_of(newsresult[0]))
		newsresult = driver.find_elements(By.ID, 'tournamentNewsTab')	
	if not 'No news found.' in newsresult[0].text:
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

def wait_load_detailed_news(driver, url_news):
	print("Start wait load detailed news")
	wait = WebDriverWait(driver, 10)
	class_name = 'fsNewsArticle__title'
	title = driver.find_elements(By.CLASS_NAME, class_name)
	driver.get(url_news)
	if len(title) == 0:
		title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
	else:
		wait.until(EC.staleness_of(title[0]))

def random_name(folder = 'news_images', termination = '.jpg'):
	file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	return os.path.join(folder,file_name + termination)

def random_id():
	rand_id = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
	rand_id = rand_id + str(random.choice([0, 9]))
	digits = ''.join([str(random.randint(0, 9)) for i in range(4)])
	return rand_id+digits

def get_mentions(driver):
	mention_list = ''
	mentions = driver.find_elements(By.XPATH, '//div[@class="fsNewsArticle__mentions"]/a')
	for mention in mentions:
		if mention_list == '':
			mention_list = mention.text
		else:
			mention_list = mention_list +', '+mention.text
	return mention_list

def save_news_database(dict_news):	
	query = "INSERT INTO news VALUES(%(news_id)s, %(news_content)s, %(image)s,\
			 %(published)s, %(news_summary)s, %(news_tags)s, %(title)s)"
	cur = con.cursor()
	cur.execute(query, dict_news)
	con.commit()

def save_ligue_tornament_info(dict_ligue_tornament):
	print("Info ligue tournament info save")
	for field, value in dict_ligue_tornament.items():
		print(field, value, end ='-')

	query = "INSERT INTO league VALUES(%(league_id)s, %(league_country)s, %(league_logo)s, %(league_name)s, %(league_name_i18n)s)"     	 #test-
	cur = con.cursor()																			 #test-	
	cur.execute(query, dict_ligue_tornament)														 #test-
	con.commit()																					 #test-

def process_current_news_link(driver, current_news_link):
	flashscore_url_news = get_news_url_date(driver, current_news_link)

	for url_date_news in flashscore_url_news:		
		wait_load_detailed_news(driver, url_date_news['url'])
		dict_new = get_news_info(driver, url_date_news['date'])
		save_news_database(dict_new) #test-
		# dict to save in database dict_new	

def extract_news_info(driver, list_upate_news, dict_check_point):
	continue_process = False
	for index, current_dict in enumerate(list_upate_news):

		if dict_check_point['index'] == index:
			continue_process = True

		if continue_process:
			pending_extract = True
			count = 0
			while pending_extract and count < 5:
				try:
					print("Start process: ", index, dict_check_point['index'], len(list_upate_news))
					current_url = current_dict['news_link']
					wait_load_detailed_news(driver, current_url)
					dict_new = get_news_info_v2(driver, current_dict)
					save_news_database(dict_news)
					dict_check_point['index'] = index
					save_check_point('check_points/check_point_m1_news.json', dict_check_point)
					pending_extract = False
				except:
					count += 1
					print("Loading again")

def get_news_info_v2(driver, dict_news):
	print("start get_news_info_v2 ")
	wait = WebDriverWait(driver, 10)
	image = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="imageContainer__element"]/figure/picture/img')))
	image_url = image.get_attribute('src')
	articlebody = driver.find_element(By.CLASS_NAME, 'fsNewsArticle__content')
	summary = articlebody.find_element(By.XPATH, './/div[@class="fsNewsArticle__perex"]')
	body_html = articlebody.get_attribute('outerHTML')
	body_html = body_html.replace(str(summary.get_attribute('ourterHTML')), '')
	# image_path = random_name(folder = 'images/news/full_images')
	image_path = dict_news['image_path_small'].replace('small_images','full_images').replace('.avif','.png')
	save_image(driver, image_url, image_path)
	mentions = get_mentions(driver)
	dict_news['news_id']= random_id()
	dict_news['news_summary'] = summary.text
	dict_news['news_content'] = body_html
	dict_news['image'] = image_path
	dict_news['news_tags'] = mentions
	
	# dict_max_len = {'news_id':40, 'title':400, 'news_summary':8196, 'news_content':16392, 'news_tags':255}
	# for field_name, max_len in dict_max_len.items():
	# 	if len(str(dict_news[field_name])) > max_len:
	# 		print(field_name, "Exced max len: ", max_len,'/',len(str(dict_news[field_name])))
	# for key, field in dict_news.items():
	# 	print(key, len(str(field)), end='--')
	# dict_news = {'news_id':random_id(), 'news_summary':summary.text,
	# 			 'news_content':body_html[0:16392], 'image':image_path,
	# 			'published':date,'news_tags': mentions}
	return dict_news

def get_all_news(driver, dict_news_links ='check_points/flashscore_links.json'):	
	dict_sports = load_json(dict_news_links)
	dict_scraper_control_news = check_previous_execution(file_path = 'check_points/scraper_control_news.json')

	dict_check_point = check_previous_execution(file_path = 'check_points/check_point.json')

	if len(dict_check_point) == 0:
		print("Initialization")
		dict_check_point = {'country':'', 'ligue_tournament':''}
		continue_country = True
		continue_team = True
	else:    
		continue_country = False
		continue_team = False
		
	print("dict_check_point: ", dict_check_point)

	for sport, dict_sport in dict_sports.items():
		if sport in dict_scraper_control_news.keys():
			pass
			print(sport, "Ready")
		else:
			print("--------------------------- SPORT---------------------------")
			for country, country_info in dict_sport.items():
				if country == dict_check_point['country']:
					continue_country = True
					
				if continue_country:
					print("--------------------------- COUNTRY-------------------")
					dict_check_point['country'] = country # Update current country.
					try:						
						current_news_link = country_info['url_news']
						process_current_news_link(driver, current_news_link)
					except:
						for ligue_tournament, ligue_tournament_info in country_info.items():
							if dict_check_point['ligue_tournament'] == ligue_tournament:
								continue_team = True
							
							if continue_team:
								print("--------------------------- TEAM ------------")
								print(ligue_tournament, ligue_tournament_info)
								current_news_link = team_info['url_news']
								print(current_news_link,'\n')
								driver.get(current_news_link)
								process_current_news_link(driver, current_news_link)
								dict_check_point['ligue_tournament'] = ligue_tournament
								save_check_point('check_points/check_point.json', dict_check_point)				
				save_check_point('check_points/scraper_control_news.json', dict_scraper_control_news)
		dict_scraper_control_news[sport] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_teams_info(driver, dict_news_links ='check_points/flashscore_links.json'):
	dict_sports = load_json(dict_news_links)
	for sport, dict_sport in dict_sports.items():
		print("--------------------------- SPORT---------------------------")
		for country, country_info in dict_sport.items():
			print("--------------------------- COUNTRY-------------------")
			for team, team_info in country_info.items():        
				print("--------------------------- LIGUE-TOURNAMENTS ------------")
				print(team, team_info)
				current_news_link = team_info['url_team']

				driver.get(current_news_link)

				# input_user = input("Type s to stop process: ")
				# if input_user == 's':
				# 	print(stop)

########################################################## MILESTONE 2 ###################################################

def main_extract_news(driver, dict_url_news):
	dict_check_point = check_previous_execution(file_path = 'check_points/check_point_m1_news.json')
	enable_news = check_previous_execution(file_path = 'check_points/dict_enable_news.json')
	
	print("dict_check_point: ", dict_check_point)

	if len(dict_check_point) == 0:
		print("Create an empty check point ")
		dict_check_point = {'sport':'', 'index':0}
		continue_sport = True
	else:
		dict_check_point['index'] = dict_check_point['index'] + 1
		continue_sport = False

	for sport, news_url in dict_url_news.items():
		if enable_news[sport]:
			print("Current sport: ", sport, "#", dict_check_point['sport'], '#')
			if dict_check_point['sport'] == sport:
				print("Process sport activated: ")
				continue_sport = True

			if continue_sport:
				dict_check_point['sport'] = sport
				print(sport, news_url)
				wait_update_page(driver, news_url, "section__mainTitle")
			#     click_show_more_news(driver)
				list_upate_news = get_list_recent_news(driver)

				extract_news_info(driver, list_upate_news, dict_check_point)
				dict_check_point['index'] = 0

def main():
	config_dict = load_json('check_points/config.json')

	driver = launch_navigator('https://www.flashscore.com')

	if config_dict['get_news_m1']:
		dict_url_news_m1 = load_json('check_points/sports_url_m1.json')
		main_extract_news(driver, dict_url_news_m1)

	if config_dict['sports_link']:	

		dict_sports = get_sports_links(driver)
		save_check_point('check_points/sports_url.json', dict_sports)

	if config_dict['update_links']:
		if not os.path.isfile('check_points/sports_url.json'):
			dict_sports = get_sports_links(driver)
			save_check_point('check_points/sports_url.json', dict_sports)
		else:
			dict_sports = load_json('check_points/sports_url.json')

		build_dict_urls(driver, dict_sports, 
				file_main_dict = 'check_points/flashscore_links.json',
				 dict_issues = 'check_points/flashscore_issues.json')

	if config_dict['get_news']:
		get_all_news(driver, dict_news_links ='check_points/flashscore_links.json')

con = getdb() #test-
int_folders()			

if __name__ == "__main__":  	#test-	
	main()            			#test-
	con.close()					#test-
# 