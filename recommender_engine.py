import pandas as pd 
import numpy as np 
from keras.models import load_model
from sklearn.preprocessing import OrdinalEncoder
import pickle
import model_features
import importlib
import os

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


class IndependentFeatureEncoding:
  def __init__(self,path):
    self.path = path
    with open(self.path, 'rb') as f:
      self.encoder = pickle.load(f)
  def get_frame(self,data):
    if isinstance(data,pd.Series):
      return data.to_frame().T
    else:
      return data
  def write_encoder(self):
    with open(self.path, 'wb') as f:
      pickle.dump(self.encoder,f)
  def fit(self,data):
    data = self.get_frame(data)
    for row in range(len(data)):
      for j,column in enumerate(self.encoder.feature_names_in_):
        if data.loc[row,column] not in self.encoder.categories_[j]:
           self.encoder.categories_[j] = np.append(self.encoder.categories_[j],data.loc[row,column])
    self.write_encoder()
    return self.encoder
  def transform(self,data):
    data = self.get_frame(data)
    with open(self.path, 'rb') as f:
      self.encoder = pickle.load(f)
    return self.encoder.transform(data)
  def fit_transform(self,data):
    self.fit(data)
    return self.transform(data)
    
    
class CommonFeatureEncoding(IndependentFeatureEncoding):
  def __init__(self, path):
    super().__init__(path)
    self.categories = self.encoder.categories_[0].copy()
  def fit(self,data):
    data = self.get_frame(data)
    for row in range(len(data)):
      for column in self.encoder.feature_names_in_:
        if data.loc[row,column] not in self.categories:
           self.categories = np.append(self.categories,data.loc[row,column])
    for i in range(len(self.encoder.categories_)):
      self.encoder.categories_[i] = self.categories
    self.write_encoder()
  def fit_transform(self,data):
    self.fit(data)
    return self.transform(data)
  
  
class DataPreprocessor:
  def __init__(self):
    self.passion_encoder = CommonFeatureEncoding('D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/obj/passion_enc.bin')
    self.language_encoder = CommonFeatureEncoding('D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/obj/passion_enc.bin')
    self.rem_encoder = IndependentFeatureEncoding('D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/obj/rem_enc.bin')
  def get_frame_from_cols(self,dataset,cols):
    if isinstance(dataset, pd.Series):
      return dataset.to_frame().T[cols]
    else:
      return dataset[cols]
  def preprocess_user_clf(self,data):
    rem = self.get_frame_from_cols(data,model_features.encodables.remaining)
    passions = self.get_frame_from_cols(data,model_features.encodables.passions)
    lang = self.get_frame_from_cols(data,model_features.encodables.language)
    data[model_features.encodables.remaining] = self.rem_encoder.fit_transform(rem)
    data[model_features.encodables.passions] = self.passion_encoder.fit_transform(passions)
    data[model_features.encodables.language] = self.language_encoder.fit_transform(lang)
    return data
    
  
class ModelEvaluator:
  def __init__(self,user_clf_path,cbf_model_path) -> None:
    self.user_clf = load_model(user_clf_path)
    self.cbf_model = load_model(cbf_model_path)
  def _user_clf_pred(self,item_data):
    return self.user_clf.predict(item_data)
  def _cbf_pred(self,item_data,user_data):
    user_data = np.ones_like(item_data) * user_data
    item_data = np.ones_like(user_data) * item_data
    return self.cbf_model.predict([user_data,item_data])