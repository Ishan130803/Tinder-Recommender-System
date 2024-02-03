import pandas as pd 
import numpy as np 
from keras.models import load_model
from sklearn.preprocessing import OrdinalEncoder

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

  def preprocess_data(self, data_ser : pd.Series):
    pass

  
  
