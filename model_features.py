import pandas as pd 
import numpy as np 




all_features = [
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
    
non_encodables = ['age']
  
class encodables:
  passions = [
    'Passions__0',
    'Passions__1',
    'Passions__2',
    'Passions__3',
    'Passions__4',
  ]
  language = [
    'Language_1',
    'Language_2',
    'Language_3',
    'Language_4',
    'Language_5',
  ]
  remaining = [
    'verified',
    'looking_for',
    'Pronouns',
    'Relationship_Monogamy',
    'Relationship_Ethical non-monogamy',
    'Relationship_Open relationship',
    'Relationship_Polyamory',
    'Relationship_Open to exploring',
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
  ]
  
  
def make_cat_ser_from_feat(*features):
  length = 0;
  for feat in features:
    length+=len(feat)
    
  joined_features = []
  [joined_features.extend(feat) for feat in features]
  
  return pd.Series(
    data = [np.array([]) for i in range(length)],
    index = joined_features
  )

