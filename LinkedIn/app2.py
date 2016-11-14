from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random, getpass, os
from bs4 import BeautifulSoup


class Main:

	def __init__(self):
		print('\nHUNTING HEAD HUNTERS by Tomas Silva Ebensperger.')
		chromedriver = os.getcwd()+'/chromedriver'
		chrome_options = webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		chrome_options.add_experimental_option("prefs",prefs)
		self.credentials = self.credentials()
		self.driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
		self.main(self.driver, self.credentials['email'], self.credentials['password'], self.credentials['job'], self.credentials['location'], self.credentials['n'])

	def credentials(self):
		print('\n[+] Credentials.\n')
		email = input('Enter email    | ')
		password = getpass.getpass('Enter password | ')
		job = input('Job keywords   | ')
		location = input('Job location   | ')
		n_pages = int(input('Page limit     | '))
		return {'email': email, 'password':password, 'job':job, 'location':location, 'n':n_pages}

	def jobLinks(self, driver, pages):
		print('\n[+] Getting jobs.')
		page_count = 0
		jobs_links = []
		count = 0
		while True:
			if page_count > pages:
				print('\n[+] Limit reached, total jobs: {}'.format(count))
				break
			time.sleep(random.uniform(0.1,0.3))
			soup = BeautifulSoup(driver.page_source, 'lxml')
			matches = soup.find_all('a', {'class':'job-title-link'})
			for job in matches:
				href = job.get('href')
				if href not in jobs_links:
					jobs_links.append(href)
					# print('----')
					# print(job.text)
					# print(href)
					count +=1
			try:
				driver.execute_script("window.scrollTo(0, 1000)")
				time.sleep(random.uniform(1,2))
				element = driver.find_element_by_class_name('next-btn-icon')
				element.click()
				page_count += 1

			except:
				print('\n[+] No more jobs to parse, total jobs: {}'.format(count))
				break
		
		return jobs_links

	def profileLinks(self, driver, job_links):
		print('\n[+] Profiles to visit:\n')
		count = 0
		profile_links=[]
		for job in job_links:
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

		return profile_links

	def profileVisit(self, driver, profile_links):
		total = len(profile_links)
		print('\n[+] Visiting profiles.\n')
		for number, profile in enumerate(profile_links):
			driver.get(profile)
			print('{}/{}'.format((number+1), total))
			time.sleep(random.uniform(0.1,0.3))

	def main(self, driver, email, password, job, location, n):
		driver.get('https://www.linkedin.com/uas/login')

		element = driver.find_element_by_id('session_key-login')
		element.send_keys(email)

		element = driver.find_element_by_id('session_password-login')
		element.send_keys(password)
		element.submit()

		element = WebDriverWait(driver, 2).until(EC.title_is('Welcome! | LinkedIn'))
		driver.get('https://www.linkedin.com/jobs/')

		jobs_input = driver.find_element_by_id('keyword-search-box')
		jobs_input.clear()
		jobs_input.send_keys(job)
		location_input = driver.find_element_by_id('location-search-box')
		location_input.clear()
		location_input.send_keys(location)
		location_input.submit()

		jobs_links = self.jobLinks(driver, n)
		profile_links = self.profileLinks(driver, jobs_links)
		self.profileVisit(driver, profile_links)

		print('\n[+] Done.')
		driver.quit()


if __name__ == '__main__':
	main = Main()

