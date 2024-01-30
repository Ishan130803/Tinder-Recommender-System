from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys,ActionChains
from xpaths import Xpaths
import re
import time
import copy


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
			url = text
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
			for index,attribute_elem in enumerate(attribute_elems):
				attribute_data = self.get_descriptor_attribute(attribute_elem,heading,index)
				attributes.append(attribute_data)
		return data.copy()
	def url_extractor(self,text):
		url_pattern = re.compile(r'background-image:\s*url\((\"|\')(.*?)\1\)')
		match = re.search(url_pattern, text)
		if match:
			url = match.group(2)
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
	def get_descriptor_attribute(self,elem,heading,index):
		text = elem.text
		img_elems = elem.find_elements(By.XPATH,Xpaths.icon_name)
		column = '{}__'.format(heading)
		if len(img_elems) != 0:
			label = self.name_from_url(img_elems[0].get_attribute('src'))
			column = '{}{}'.format(column,label)
		else:
			column = '{}{}'.format(column,index)
		return (column,text)
	def name_from_url(self,url):
		start_index = url.find('descriptors/') + len('descriptors/')
		end_index = url.find('@1x.png')
		extracted_text = url[start_index:end_index]
		return extracted_text
	


def get_all(Tsc):
  data = {}
  data["name"] = Tsc.get_name()
  data["age"] = Tsc.get_age()
  data["verified"] = Tsc.is_verified()
  data["url"] = Tsc.get_image_url()
  data["looking_for"] = Tsc.get_looking_for()
  data["about"] = Tsc.get_about()
  data.update(Tsc.get_lifestyle())
  return data


# data = {
#   'name': 'Ishan', 
#   'age': '20', 
#   'verified': True, 
#   'url': 'background-image: url("https://images-ssl.gotinder.com/65afe5dae74ac8010002d991/640x800_75_f4bc49de-1d73-4aef-9061-d7efe50f48d3.webp"); background-position: 50% 50%; background-size: auto 100%;', 
#   'looking_for': 'Short-term fun', 
#   'about': ['Job Title at Maruti Suzuki', '154 cm', 'cam', 'Lives in Seattle', 'Straight Man'], 
#   'Pronouns': [('Pronouns__pronoun', 'Him'), ('Pronouns__pronoun', 'He')], 
#   'Relationship Type': [('Relationship Type__looking_for', 'Open relationship'), ('Relationship Type__looking_for', 'Polyamory'), ('Relationship Type__looking_for', 'Open to exploring')], 
#   'Languages I Know': [('Languages I Know__0', 'Azerbaijani'), ('Languages I Know__1', 'Belarusian'), ('Languages I Know__2', 'Bosnian'), ('Languages I Know__3', 'Cantonese'), ('Languages I Know__4', 'Burmese')], 
#   'Basics': [('Basics__astrological_sign', 'Gemini'), ('Basics__education', 'In Grad School'), ('Basics__kids', 'I have children and want more'), ('Basics__covid_comfort', 'Prefer not to say'), ('Basics__mbti', 'INFP'), ('Basics__communication_style', 'Video chatter'), ('Basics__love_language', 'Thoughtful gestures')], 
#   'Lifestyle': [('Lifestyle__pets', 'Dog'), ('Lifestyle__drink_of_choice', 'On special occasions'), ('Lifestyle__smoking', 'Social smoker'), ('Lifestyle__420', 'Occasionally'), ('Lifestyle__workout', 'Everyday'), ('Lifestyle__appetite', 'Omnivore'), ('Lifestyle__social_media', 'Influencer status'), ('Lifestyle__sleeping_habits', 'Early bird')], 
#   'Passions': [('Passions__0', 'Heavy Metal'), ('Passions__1', 'Spotify'), ('Passions__2', 'Social Development'), ('Passions__3', 'Harry Potter'), ('Passions__4', 'Self Care')], 
#   'My Anthem': [('My Anthem__0', 'Anthem Part Two\nblink-182')]
# }


def create_data_row(data):
  row = np.full((36,), "none", dtype=str)
  index = 0
  row[index] = data["name"] ; index += 1
  row[index] = data["age"] ; index += 1
  row[index] = data["verified"] ; index += 1
  row[index] = data["looking_for"] ; index += 1
  row[index] = data["url"] ; index += 1
  if "Pronouns" in data:
    row[4] = data["Pronouns"][0][1]
  index+=1
  check = "Relationship Type" in data
  for i in Ldata.RelationshipType.relationship_type:
    if check and any(i == tup[1] for tup in data["Relationship Type"]):
      row[index] = 'True'; index+=1
    else:
      row[index] = 'False'; index+=1
  check = "Languages I Know" in data
  for i in range(5):
    if check and i < len(data["Languages I Know"]):
      row[index] = data["Languages I Know"][i][1] ; index += 1
    else:
      row[index] = "none" ; index += 1
  check = "Basics" in data
  if check:
    for i in data["Basics"]:
      row[columns.index(data["Basics"][i][0])] = data["Basics"][i][1]
  index+=7
  check = "Lifestyle" in data
  if check:
    for i in data["Lifestyle"]:
      row[columns.index(data["Lifestyle"][i][0])] = data["Lifestyle"][i][1]
  index+=8
  check = "Passions" in data
  if check:
    for i in data["Passions"]:
      row[columns.index(data["Passions"][i][0])] = data["Passions"][i][1]
  index+=5
  return row  