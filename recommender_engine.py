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
    return self.fit(data).transform(data)
    
    
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
    return self.encoder
  
  def fit_transform(self,data):
    return self.fit(data).transform(data)
  
  

class DataPreprocessor:
  def __init__(
    self,
    passion_enc_path,
    language_enc_path,
    rem_enc_path,
  ):
    self.passion_encoder = CommonFeatureEncoding(passion_enc_path)
    self.language_encoder = CommonFeatureEncoding(language_enc_path)
    self.rem_encoder = IndependentFeatureEncoding(rem_enc_path)
  
  def get_frame_from_cols(self,dataset,cols):
    if isinstance(dataset, pd.Series):
      return dataset.to_frame().T[cols].astype('object')
    else:
      return dataset[cols].astype('object')
    
  def preprocess_data(self,data):
    passions = self.passion_encoder.fit_transform(self.get_frame_from_cols(data,model_features.encodables.passions))
    lang = self.language_encoder.fit_transform(self.get_frame_from_cols(data,model_features.encodables.language))
    rem = self.rem_encoder.fit_transform(self.get_frame_from_cols(data,model_features.encodables.remaining))
    
    passions = np.sort(passions,axis = 1)
    lang = np.sort(lang,axis=1)
    
    data[model_features.encodables.remaining] = rem
    data[model_features.encodables.passions] = passions
    data[model_features.encodables.language] = lang
    
    return data
  
  
  def preprocessing_cbf_clf(self,user_data,item_data,user_feat,item_feat):
    user_data = self.preprocess_data(user_data)[user_feat].astype(np.float64).to_numpy()
    item_data = self.preprocess_data(item_data)[item_feat].astype(np.float64).to_numpy()
    return user_data, item_data
  
  def preprocessing_user_clf(self,item_data,item_feat):
    item_data = self.preprocess_data(item_data)[item_feat].astype(np.float64).to_numpy()
    # item_data['language_score'] = np.expand_dims(np.sum(np.vectorize(self.lang_scorer.predict)(lang),axis = 1),axis = 1)
    # item_data['passion_score'] = np.expand_dims(np.sum(np.vectorize(self.passion_scorer.predict)(passion),axis = 1),axis = 1)
    return item_data
    
    
    
  
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