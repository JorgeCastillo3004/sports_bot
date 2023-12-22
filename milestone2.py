from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import psycopg2

from common_functions import *
# from main import database_enable
# from common_functions import utc_time_naive
from data_base import *

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--db', type=bool, default=False)
# args = parser.parse_args()
# database_enable = args.db

# print("Type: ", type(database_enable))

# print("database_enable: ", database_enable)
# if database_enable:
# 	print("Write on db activate")
# else:
# 	print("Don't write in database")



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

def click_news(driver):
	wait = WebDriverWait(driver, 10)
	newsbutton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'tabs__tab.news')))  # "tabs__tab news selected"
	newsbutton.click()

def check_pin(driver):
	pin = driver.find_element(By.ID, "toMyLeagues")
	if 'pinMyLeague active 'in pin.get_attribute('outerHTML'):
		return True
	else:
		return False

def get_ligues_data(driver):
	block_ligue_team = driver.find_element(By.CLASS_NAME, 'container__heading')
	sport = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[1]').text
	league_country = block_ligue_team.find_element(By.XPATH, './/h2[@class= "breadcrumb"]/a[2]').text
	league_name = block_ligue_team.find_element(By.CLASS_NAME,'heading__title').text
	season_name = block_ligue_team.find_element(By.CLASS_NAME, 'heading__info').text
	image_url = block_ligue_team.find_element(By.XPATH, './/div[@class= "heading"]/img').get_attribute('src')
	image_path = random_name(folder = 'images/logos/')
	save_image(driver, image_url, image_path)
	image_path = image_path.replace('images/logos/','')
	league_id = random_id()
	season_id = random_id()
	ligue_tornamen = {"league_id":league_id,"season_id":season_id, 'sport':sport, 'league_country': league_country,
					 'league_name': league_name,'season_name':season_name, 'league_logo':image_path,
					  'league_name_i18n':'', 'season_end':'', 'season_end':'', 'season_start':''}
	return ligue_tornamen

def find_ligues_torneos(driver):
	wait = WebDriverWait(driver, 5)
	xpath_expression = '//div[@id="my-leagues-list"]'
	ligues_info = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_expression)))
	dict_liguies = {}
	if not "To select your leagues " in ligues_info.text:
		# ligues = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))        
		ligues = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')))
		print(len(ligues))        
		# ligues = driver.find_elements(By.XPATH, '//div[@id="my-leagues-list"]/div/div/a')
		# print(len(ligues))
		gender = ''
		for ligue in ligues:
			if '#man' in ligue.get_attribute('outerHTML'):
				gender = "_man"
			if '#woman' in ligue.get_attribute('outerHTML'):
				gender = "_woman"
			dict_liguies['_'.join(ligue.text.split())+gender] = ligue.get_attribute('href')			
	return dict_liguies

def main_m2(driver, flag_news = False):
	dict_sports = load_json('check_points/sports_url_m2.json')
	conf_enable_news = check_previous_execution(file_path = 'check_points/CONFIG_M2.json')
	
	dict_with_issues = {}
	for sport, flag_load in conf_enable_news.items():
		# user_confirmation = False
		if flag_load:			
			print("Init: ", sport, dict_sports[sport])
			wait_update_page(driver, dict_sports[sport], "container__heading")
			
			dict_ligues_tornaments = find_ligues_torneos(driver)
			# if not user_confirmation:
				# for ligue_tournament, ligue_tournament_url in dict_ligues_tornaments.items():
				# 	print(ligue_tournament)
				# user_input = input("Type y to continue")
				# if user_input == 'y':
				# 	user_confirmation = True
				# if user_input == 's':
				# 	print(stop)

			for ligue_tournament, ligue_tournament_url in dict_ligues_tornaments.items():

					step = 'ligue_tournament'						
					print(" "*15, "############ Ligue: ", ligue_tournament_url)
					wait_update_page(driver, ligue_tournament_url, "container__heading")
					step = 'Ligues extraction'								
					# wait_update_page(driver, ligue_tornament_url, "heading__title")
					pin_activate = check_pin(driver)
					if pin_activate:
						print("Extract ligue info: ")
						ligue_tornamen_info = get_ligues_data(driver)
						print(ligue_tornamen_info)
						print("#"*30, '\n'*2)
						print("database_enable: ", database_enable)
						if database_enable:
							save_ligue_tornament_info(ligue_tornamen_info)
							save_season_database(ligue_tornamen_info)
						if flag_news:
							process_current_news_link(driver, driver.current_url)								
							wait_update_page(current_url)

						url_news = driver.current_url

def initial_settings_m2(driver):

	# GET SPORTS AND SPORTS LINKS
	if not os.path.isfile('check_points/sports_url_m1.json'):
		driver.get('https://www.flashscore.com')
		dict_sports = get_sports_links(driver)
		save_check_point('check_points/sports_url_m2.json', dict_sports)

	# BUILD CONFIG_M2
	if not os.path.isfile('check_points/CONFIG_M2.json'):
		dict_sports = load_json('check_points/sports_url_m2.json')
		dict_sports
		dict_config_m2 = {}
		for sport in dict_sports.keys():
			dict_config_m2[sport] = False
		save_check_point('check_points/CONFIG_M2.json', dict_config_m2)

CONFIG = load_json('check_points/CONFIG.json')
database_enable = CONFIG['DATA_BASE']
if database_enable:
	con = getdb()

if __name__ == "__main__":  	
	driver = launch_navigator('https://www.flashscore.com', database_enable)
	login(driver, email_= "jignacio@jweglobal.com", password_ = "Caracas5050@\n")
	initial_settings_m2(driver)
	create_sports_selected_in_db()
	main_m2(driver, flag_news = False)
	if database_enable:
		con.close()