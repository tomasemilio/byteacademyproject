from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random, getpass, os
from bs4 import BeautifulSoup


print('''

LinkedIn - Hunting Head Hunters
---------------------------------------
	''')

email = input('Email: ')
password = getpass.getpass('Password: ')
job = input('Job keywords (comma separated): ')
job_edit = job.replace(' ', '').replace(',', '+')
location = input('Job location: ')
location_edit = location.replace(' ', '+')

jobs_links = []
profile_links = []


chromedriver = os.getcwd()+'/chromedriver'


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
driver.get('https://www.linkedin.com/uas/login')

element = driver.find_element_by_id('session_key-login')
element.send_keys(email)

element = driver.find_element_by_id('session_password-login')
element.send_keys(password)
element.submit()

try:
	element = WebDriverWait(driver, 10).until(EC.title_is('Welcome! | LinkedIn'))
	driver.get('https://www.linkedin.com/jobs/')
except:
	driver.quit()
	print('wrong!')

jobs_input = driver.find_element_by_id('keyword-search-box')
jobs_input.send_keys(job)
location_input = driver.find_element_by_id('location-search-box')
location_input.send_keys(location)
location_input.submit()



count = 0
page_count = 0
page = 1
while True:
	try:
		if page_count>=500:
			print('Limit reached!')
			break
		time.sleep(random.uniform(0.1,0.3))
		soup = BeautifulSoup(driver.page_source, 'lxml')
		matches = soup.find_all('a', {'class':'job-title-link'})
		if len(matches)==0:
			print('\nNo jobs to parse.\n')
			break
		for job in matches:
			if job not in jobs_links:
				jobs_links.append(job.get('href'))
				count += 1	
		driver.execute_script("window.scrollTo(0, 1000)")
		time.sleep(random.uniform(1,2))
		element = driver.find_element_by_class_name('next-btn-icon')
		element.click()
		page_count += 25
		page += 1
	except:
		print('No more jobs to parse!')
		break

print('\nNumber of jobs:'+str(count))


count = 0
for job in jobs_links:
	driver.get(job)
	time.sleep(random.uniform(0.1,0.3))
	sauce = BeautifulSoup(driver.page_source, 'lxml')
	links = sauce.find_all('a')
	for link in links:
		try:
			href = link.get('href')
			if 'contact_job_poster_picture' in href:
				if href not in profile_links:
					name = sauce.find('div', {'class':'info-container-upsell'}).h4
					count +=1
					profile_links.append(href)
					print(str(count)+'|'+name.text)

		except:
			continue

print('Number of head hunters to visit: '+str(count))


for profile in profile_links:
	driver.get(profile)
	time.sleep(random.uniform(0.1,0.3))

print('DONE!!!!!')
driver.quit()












