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

  "Basics__zodiac",
  "Basics__education",
  "Basics__children",
  "Basics__vaccinated",
  "Basics__personality",
  "Basics__communication",
  "Basics__love_gesture",

  "Lifestyle__pets",
  "Lifestyle__drinking",
  "Lifestyle__smoking",
  "Lifestyle__cannabis",
  "Lifestyle__workout",
  "Lifestyle__diet",
  "Lifestyle__social",
  "Lifestyle__sleep",

  "Passion_1",
  "Passion_2",
  "Passion_3",
  "Passion_4",
  "Passion_5",

  "url",


]



# pets = pd.Series(np.arange(0,len(Ldata.LifeStyle.pets) + 1),index = ["none"] + Ldata.LifeStyle.pets)
# drinking = pd.Series(np.arange(0,len(Ldata.LifeStyle.drinking) + 1),index = ["none"] + Ldata.LifeStyle.drinking)
# smoking = pd.Series(np.arange(0,len(Ldata.LifeStyle.smoking) + 1),index = ["none"] + Ldata.LifeStyle.smoking)
# cannabis = pd.Series(np.arange(0,len(Ldata.LifeStyle.cannabis) + 1),index = ["none"] + Ldata.LifeStyle.cannabis)
# workout = pd.Series(np.arange(0,len(Ldata.LifeStyle.workout) + 1),index = ["none"] + Ldata.LifeStyle.workout)
# diet = pd.Series(np.arange(0,len(Ldata.LifeStyle.diet) + 1),index = ["none"] + Ldata.LifeStyle.diet)
# social = pd.Series(np.arange(0,len(Ldata.LifeStyle.social) + 1),index = ["none"] + Ldata.LifeStyle.social)
# sleep = pd.Series(np.arange(0,len(Ldata.LifeStyle.sleep) + 1),index = ["none"] + Ldata.LifeStyle.sleep)


def create_data_row(data):
  row = []
  row.append(data["name"])
  row.append(data["age"])
  row.append(data["verified"])
  row.append(data["looking_for"])

  if "Pronouns" in data:
    row.append(data["Pronouns"][0])
  else:
    row.append("none")

  check = "Relationship Type" in data
  for i in Ldata.RelationshipType.relationship_type:
    if check:
      if i in data["Relationship Type"]:
        row.append(True)
      else:
        row.append(False)
    else:
      row.append(False)
      

  check = "Languages I Know" in data
  for i in range(5):
    if check and i < len(data["Languages I Know"]):
      row.append(data["Languages I Know"][i])
    else:
      row.append("none")

  check = "Basics" in data
  j = 0
  for i in range(7):
    if check and (j < len(data["Basics"])) and (data["Basics"][j] in Ldata.Basics.all_data[i]):
      row.append(data["Basics"][j])
      j+=1
    else:
      row.append("none")

  check = "Lifestyle" in data
  j = 0
  for i in range(8):
    if check and (j < len(data["Basics"])) and (data["Lifestyle"][j] in Ldata.LifeStyle.all_data[i]):
      row.append(data["Lifestyle"][j])
      j+=1
    else:
      row.append("none")

  
  check = "Passions" in data
  for i in range(5):
    if check and i < len(data["Passions"]):
      row.append(data["Passions"][i])
    else:
      row.append("none")
  
  row.append(data["url"])

  return row
  
  
