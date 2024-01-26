from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys,ActionChains
from xpaths import Xpaths
import re
import time

class TinderScraper:
	def __init__(self,driver : webdriver):
		self.driver = driver

	def elem_check(self,XPATH,arr = False):
		elems = self.driver.find_elements(By.XPATH,XPATH)
		if len(elems) == 0:
			return False
		elif arr == False:
			return elems[0]
		else:
			return elems

	def get_image_url(self):
		elem = self.elem_check(Xpaths.image)
		if elem is False:
			return "none"
		else:
			text = elem.get_attribute('style')
			url = self.url_extractor(text)
			return url

	
	def get_name(self) -> str:
		elem = self.elem_check(Xpaths.name)
		if elem is False:
			return "none"
		else:
			return elem.text
	
	def get_age(self) -> str:
		elem = self.elem_check(Xpaths.age)
		if elem is False:
			return "none"
		else:
			return elem.text
	
	def is_verified(self) -> bool:
		verified = self.elem_check(Xpaths.verified)
		if verified is False:
			return False
		else:
			return True
  
	def get_looking_for(self) -> str:
		looking_for = self.elem_check(Xpaths.looking_for)
		if looking_for is False:
			return "none"
		else: 
			return looking_for.text

	def get_about(self) -> list:
		about = []
		elems = self.elem_check(XPATH=Xpaths.about,arr=True)
		if elems is False:
			return about
		else:
			for elem in elems:
				about.append(elem.text)
			return about

	def get_lifestyle(self) -> dict:
		data = {}
		elems = self.driver.find_elements(By.XPATH,Xpaths.lifestyle_categories)
		for elem in elems:
			self.click_expandables(elem)
			heading = elem.find_element(By.XPATH,'.//h2').text
			data[heading] = []
			attributes = data[heading]
			attribute_elems = elem.find_elements(By.XPATH,Xpaths.lifestyle_attributes)
			for attribute_elem in attribute_elems:
				attributes.append(attribute_elem.text)
		return data.copy()


	
	def url_extractor(self,text):
		url_pattern = r'url\(&quot;([^&]+)&quot;\)'
		match = re.search(url_pattern, text)
		if match:
			url = match.group(1)
			return url
		else:
			return "none"
		
	def click_expandables(self,elem):
		clickables = elem.find_elements(By.XPATH,Xpaths.more_expand_elem)
		if len(clickables) == 0:
			return
		else:
			for clickable in clickables:
				clickable.click()
				time.sleep(0.2)