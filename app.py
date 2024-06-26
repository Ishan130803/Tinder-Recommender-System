from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
import pandas as pd
import numpy as np
from TinderDataClass import TinderScraper as Tsc
import db_utils
from xpaths import Xpaths
import time
from recommender_engine import ModelEvaluator


class TinderBot:
  def __init__(self, service_path, data_path):
    self.service = Service(executable_path=service_path)
    self.driver = webdriver.Chrome(service=self.service)
    self.Tsc = Tsc(driver=self.driver)
    self.df : pd.DataFrame = pd.read_csv(data_path)
    self.evaluator = ModelEvaluator(
      user_clf_path='D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/models/user_clf1.h5',
      cbf_model_path='D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/models/cbf2.h5',
      obj_path='D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/obj',
      lang_enc_name='lang_enc.bin',
      passions_enc_name='passions_enc.bin',
      rem_enc_name='rem_enc.bin',
    )

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

  def auto_routine(self):
    time.sleep(0.5+0.5*np.random.random())
    self.press_key(Keys.ARROW_UP)
    time.sleep(0.5+0.5*np.random.random())
    data = self.get_all()
    row = db_utils.create_row_series(data)
    swipe = np.random.randint(0,2)
    if swipe == 0:
      self.press_key(Keys.ARROW_LEFT)
    else:
      self.press_key(Keys.ARROW_RIGHT)
    return row

  def get_expected_prediction(self,item_data):
    cbf = self.evaluator.get_cbf_pred(item_data)
    clf = self.evaluator.get_user_clf_pred(item_data)
    print(f' Prediction by Content Based Filtering net    = {cbf}')
    print(f' Prediction by User Preference Classifier net = {clf}')
    
  def user_routine(self):
    self.press_key(Keys.ARROW_UP)
    time.sleep(0.5)
    data = self.get_all()
    row = db_utils.create_row_series(data)
    while True:
      q = input('Swipe l/r or q :')
      if q == 'l':
        self.press_key(Keys.ARROW_LEFT)
        row['prediction'] = 'NO'
      elif q == 'r':
        self.press_key(Keys.ARROW_RIGHT)
        row['prediction'] = 'YES'
      elif q == 'q':
        return row,False
      return row,True

  def user_loop(self):
    running = True
    while running:
      time.sleep(0.5)
      row,running = self.user_routine()
      if running == False:
        break
      else:
        self.df.loc[len(self.df)] = row
        print(row.to_frame().T)
        self.get_expected_prediction(row)
    self.append()
    
  def auto_loop(self, max_data = 10):
    running = True
    while running:
      for i in range(max_data):
        row,running = self.auto_routine()
        if running == False:
          break
        else:
          print(row)
          self.df.loc[len(self.df)] = row
      q = input('want to quit(q)   :')
      if q == 'q':
        running = False
    
  def append(self):
    self.df = self.df[self.df['name'] != 'none']
    self.df.to_csv('backup.csv',index = False)
  
  def login(self):
    login_btn = self.driver.find_element(By.XPATH,Xpaths.login_btn)
    login_btn.click()
    time.sleep(0.5)
    more_options = self.driver.find_element(By.XPATH,Xpaths.more_options)
    more_options.click()
    time.sleep(0.5)
    more_options = self.driver.find_element(By.XPATH,Xpaths.more_options)
    more_options.click()
    time.sleep(0.5)
    email_field = self.driver.find_element(By.XPATH,Xpaths.email)
    email_field.click()
    time.sleep(0.5)
    email_field.clear()
    email_field.send_keys('abca19510@gmail.com')
    send_email = self.driver.find_element(By.XPATH,Xpaths.send_email)
    send_email.click()
    time.sleep(0.5)

api = TinderBot(
  "D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/drivers/chromedriver.exe",
  "D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/data/backup.csv"
)

api.get_website('https://www.tinder.com')

