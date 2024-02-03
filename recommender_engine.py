import pandas as pd 
import numpy as np 
from keras.models import load_model
from sklearn.preprocessing import OrdinalEncoder
import pickle

cols = [
    'age',
    'verified',
    'looking_for',
    'Pronouns',
    'Relationship_Monogamy',
    'Relationship_Ethical non-monogamy',
    'Relationship_Open relationship',
    'Relationship_Polyamory',
    'Relationship_Open to exploring',
    'Language_1',
    'Language_2',
    'Language_3',
    'Language_4',
    'Language_5',
    'Basics__astrological_sign',
    'Basics__education',
    'Basics__kids',
    'Basics__covid_comfort',
    'Basics__mbti',
    'Basics__communication_style',
    'Basics__love_language',
    'Lifestyle__pets',
    'Lifestyle__drink_of_choice',
    'Lifestyle__smoking',
    'Lifestyle__420',
    'Lifestyle__workout',
    'Lifestyle__appetite',
    'Lifestyle__social_media',
    'Lifestyle__sleeping_habits',
    'Passions__0',
    'Passions__1',
    'Passions__2',
    'Passions__3',
    'Passions__4',
]

cols_without_age = [
    'verified',
    'looking_for',
    'Pronouns',
    'Relationship_Monogamy',
    'Relationship_Ethical non-monogamy',
    'Relationship_Open relationship',
    'Relationship_Polyamory',
    'Relationship_Open to exploring',
    'Language_1',
    'Language_2',
    'Language_3',
    'Language_4',
    'Language_5',
    'Basics__astrological_sign',
    'Basics__education',
    'Basics__kids',
    'Basics__covid_comfort',
    'Basics__mbti',
    'Basics__communication_style',
    'Basics__love_language',
    'Lifestyle__pets',
    'Lifestyle__drink_of_choice',
    'Lifestyle__smoking',
    'Lifestyle__420',
    'Lifestyle__workout',
    'Lifestyle__appetite',
    'Lifestyle__social_media',
    'Lifestyle__sleeping_habits',
    'Passions__0',
    'Passions__1',
    'Passions__2',
    'Passions__3',
    'Passions__4',
]




class metrics:
    
  # tells about how complete user's profile is 
  def completeness_rating(data_ser, completeness_weights):
    data_np = (data_ser.to_numpy() != 'none') * 1
    completeness_rating = np.dot(data_np, completeness_weights)/np.sum(completeness_weights)
    return completeness_rating
  
  
  def similarity_rating(
    data_user : pd.Series,
    data_target : pd.Series,
  ):
    return (np.sum(data_user == data_target))


class model_evaluation:
  def __init__(self,user_clf_path,cbf_model_path) -> None:
    self.encoder = OrdinalEncoder()
    with open('D:\Programming Languages\Python\.Python Projects\TInder Recommendation system\obj\encoder.bin', 'rb') as f:
      self.encoder = pickle.load(f)
      
    self.user_clf = load_model('D:\Programming Languages\Python\.Python Projects\TInder Recommendation system\models\user_clf.h5')
    self.cbf_model = load_model('D:\Programming Languages\Python\.Python Projects\TInder Recommendation system\models\cbf1.h5')
    
    with open('D:\Programming Languages\Python\.Python Projects\TInder Recommendation system\data','rb') as f:
      self.user_data_ser : pd.Series = pickle.load(f)
    self.user_data_np = self.user_data_ser.to_frame().T[cols].to_numpy()
    
    self.cols_without_age = [
    'verified',
    'looking_for',
    'Pronouns',
    'Relationship_Monogamy',
    'Relationship_Ethical non-monogamy',
    'Relationship_Open relationship',
    'Relationship_Polyamory',
    'Relationship_Open to exploring',
    'Language_1',
    'Language_2',
    'Language_3',
    'Language_4',
    'Language_5',
    'Basics__astrological_sign',
    'Basics__education',
    'Basics__kids',
    'Basics__covid_comfort',
    'Basics__mbti',
    'Basics__communication_style',
    'Basics__love_language',
    'Lifestyle__pets',
    'Lifestyle__drink_of_choice',
    'Lifestyle__smoking',
    'Lifestyle__420',
    'Lifestyle__workout',
    'Lifestyle__appetite',
    'Lifestyle__social_media',
    'Lifestyle__sleeping_habits',
    'Passions__0',
    'Passions__1',
    'Passions__2',
    'Passions__3',
    'Passions__4',
]

    self.cols = [
    'age',
    'verified',
    'looking_for',
    'Pronouns',
    'Relationship_Monogamy',
    'Relationship_Ethical non-monogamy',
    'Relationship_Open relationship',
    'Relationship_Polyamory',
    'Relationship_Open to exploring',
    'Language_1',
    'Language_2',
    'Language_3',
    'Language_4',
    'Language_5',
    'Basics__astrological_sign',
    'Basics__education',
    'Basics__kids',
    'Basics__covid_comfort',
    'Basics__mbti',
    'Basics__communication_style',
    'Basics__love_language',
    'Lifestyle__pets',
    'Lifestyle__drink_of_choice',
    'Lifestyle__smoking',
    'Lifestyle__420',
    'Lifestyle__workout',
    'Lifestyle__appetite',
    'Lifestyle__social_media',
    'Lifestyle__sleeping_habits',
    'Passions__0',
    'Passions__1',
    'Passions__2',
    'Passions__3',
    'Passions__4',
]

  
  def _user_clf_pred(self,item_data):
    return self.user_clf.predict(item_data)
  
  def _cbf_pred(self,item_data ):
    user_data = np.ones_like(item_data) * self.user_data_np
    return self.cbf_model.predict([user_data,item_data])
  
  def preprocess_data(self, data) -> pd.DataFrame:
    encodable_data = data.to_numpy()
    if isinstance(data, pd.Series):
      encodable_data = data.to_frame().T[self.cols_without_age].to_numpy()
    for index in range(len(encodable_data)):
      for i,data in enumerate(encodable_data[index]):
        if data not in self.encoder.categories_[i]:
          self.encoder.categories_[i] = np.append(self.encoder.categories_[i],np.array([data]))
    data[cols_without_age] = encodable_data
    return data
  
  def make_prediction(self, item):
    if isinstance(item,pd.Series):
      item_frame = self.preprocess_data(item)
      item_data = item_frame[cols].to_numpy()
      return (self._user_clf_pred(item_data),self._cbf_pred(item_data))
    elif isinstance(item,pd.DataFrame):
      item_frame = self.preprocess_data(item)
      item_data = item_frame[cols].to_numpy()
      return (self._user_clf_pred(item_data),self._cbf_pred(item_data))
    
        

  
  
