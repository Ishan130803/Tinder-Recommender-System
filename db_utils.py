import pandas as pd
import numpy as np
import lifestyledata as Ldata

columns = [
  "name",
  "age",
  "verified",
  "looking_for",

  "Pronouns",

  "Relationship Type_Monogamy",
  "Relationship Type_Ethical non-monogamy",
  "Relationship Type_Open relationship",
  "Relationship Type_Polyamory",
  "Relationship Type_Open to exploring",

  "Language_1",
  "Language_2",
  "Language_3",
  "Language_4",
  "Language_5",

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
  
  "url",
]

column_ser = pd.Series({
  "name" : 'none',
  "age" : 'none',
  "verified" : 'none',
  "looking_for" : 'none',
  "Pronouns" : 'none',
  "Relationship_Monogamy" : 'none',
  "Relationship_Ethical non-monogamy" : 'none',
  "Relationship_Open relationship" : 'none',
  "Relationship_Polyamory" : 'none',
  "Relationship_Open to exploring" : 'none',
  "Language_1" : 'none',
  "Language_2" : 'none',
  "Language_3" : 'none',
  "Language_4" : 'none',
  "Language_5" : 'none',
  'Basics__astrological_sign' : 'none',
  'Basics__education' : 'none',
  'Basics__kids' : 'none',
  'Basics__covid_comfort' : 'none',
  'Basics__mbti' : 'none',
  'Basics__communication_style' : 'none',
  'Basics__love_language' : 'none',
  'Lifestyle__pets' : 'none',
  'Lifestyle__drink_of_choice' : 'none',
  'Lifestyle__smoking' : 'none',
  'Lifestyle__420' : 'none',
  'Lifestyle__workout' : 'none',
  'Lifestyle__appetite' : 'none',
  'Lifestyle__social_media' : 'none',
  'Lifestyle__sleeping_habits' : 'none',
  'Passions__0' : 'none',
  'Passions__1' : 'none',
  'Passions__2' : 'none',
  'Passions__3' : 'none',
  'Passions__4' : 'none',
  'About_0' : 'none',
  'About_1' : 'none',
  'About_2' : 'none',
  'About_3' : 'none',
  'About_4' : 'none',
  "url" : 'none',
  "prediction" : 'none'
})



# pets = pd.Series(np.arange(0,len(Ldata.LifeStyle.pets) + 1),index = ["none"] + Ldata.LifeStyle.pets)
# drinking = pd.Series(np.arange(0,len(Ldata.LifeStyle.drinking) + 1),index = ["none"] + Ldata.LifeStyle.drinking)
# smoking = pd.Series(np.arange(0,len(Ldata.LifeStyle.smoking) + 1),index = ["none"] + Ldata.LifeStyle.smoking)
# cannabis = pd.Series(np.arange(0,len(Ldata.LifeStyle.cannabis) + 1),index = ["none"] + Ldata.LifeStyle.cannabis)
# workout = pd.Series(np.arange(0,len(Ldata.LifeStyle.workout) + 1),index = ["none"] + Ldata.LifeStyle.workout)
# diet = pd.Series(np.arange(0,len(Ldata.LifeStyle.diet) + 1),index = ["none"] + Ldata.LifeStyle.diet)
# social = pd.Series(np.arange(0,len(Ldata.LifeStyle.social) + 1),index = ["none"] + Ldata.LifeStyle.social)
# sleep = pd.Series(np.arange(0,len(Ldata.LifeStyle.sleep) + 1),index = ["none"] + Ldata.LifeStyle.sleep)

def create_row_series(data):
  row = column_ser.copy()
  row["name"] = data["name"]
  row["age"] = data["age"] 
  row["verified"] = str(data["verified"]) 
  row["looking_for"] = data["looking_for"] 
  row["url"] = data["url"] 
  
  if "Pronouns" in data:
    row["Pronouns"] = data["Pronouns"][0][1]
    
  check = "Relationship Type" in data
  if check:
    rels = {i[1] for i in data["Relationship Type"]}
    for i in Ldata.RelationshipType.relationship_type:
      if i in rels:
        row[f'Relationship_{i}'] = 'True'
      else:
        row[f'Relationship_{i}'] = 'False'
        
  if "Languages I Know" in data:
    languages = [i[1] for i in data["Languages I Know"]]
    for i,language in enumerate(languages):
      row[f'Language_{i+1}'] = language
  
  if "Basics" in data:
    for i in data["Basics"]:
      row[i[0]] = i[1]
  if "Lifestyle" in data:
    for i in data["Lifestyle"]:
      row[i[0]] = i[1]
  if "Passions" in data:
    for i in data["Passions"]:
      row[i[0]] = i[1]
  
  if 'about' in data:
    j = 0
    for i in data['about']:
      if (j < 5):
        row[f'About_{j}'] = i
        j+=1
      else:
        break
  return row
  

    
  
    
    
def create_data_row(data):
  row = column_ser.copy()
  index = 0
  row[index] = data["name"] ; index += 1
  row[index] = data["age"] ; index += 1
  row[index] = str(data["verified"]) ; index += 1
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
      row[columns.index(i[0])] = i[1]
  index+=7
  
  check = "Lifestyle" in data
  if check:
    for i in data["Lifestyle"]:
      row[columns.index(i[0])] = i[1]
  index+=8
  
  check = "Passions" in data
  if check:
    for i in data["Passions"]:
      row[columns.index(i[0])] = i[1]
  index+=5

  return row
