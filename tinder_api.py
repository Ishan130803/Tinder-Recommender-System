from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
import pandas as pd
import numpy as np
from TinderDataClass import TinderScraper as Tsc
import db_utils

import time


class TinderBot:
	def __init__(self, service_path):
		self.service = Service(executable_path=service_path)
		self.driver = webdriver.Chrome(service=self.service)
		self.Tsc = Tsc(driver=self.driver)

	def get_website(self, website):
		self.driver.get(website)

	def exit(self):
		self.driver.quit()

	def press_key(self, KEY: webdriver.Keys):
		ActionChains(self.driver).send_keys(KEY).perform()
		time.sleep(0.3)

	def get_text(self, XPATH):
		return self.driver.find_element(By.XPATH, XPATH).text

	def get_all(self):
		data = {}
		data["name"] = self.Tsc.get_name()
		data["age"] = self.Tsc.get_age()
		data["verified"] = self.Tsc.is_verified()
		data["url"] = self.Tsc.get_image_url()
		data["looking_for"] = self.Tsc.get_looking_for()
		data["about"] = self.Tsc.get_about()
		data.update(self.Tsc.get_lifestyle())
		return data
	
	def routine(self):
		self.press_key(Keys.ARROW_UP)
		time.sleep(0.3)
		data = self.get_all()
		row = db_utils.create_data_row(data)
		swipe = np.random.randint(0,2)
		if swipe == 0:
			self.press_key(Keys.ARROW_LEFT)
		else:
			self.press_key(Keys.ARROW_RIGHT)
		return row


api = TinderBot("chromedriver.exe")


