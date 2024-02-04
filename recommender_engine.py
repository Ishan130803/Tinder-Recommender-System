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
        if data.iloc[row][column] not in self.encoder.categories_[j]:
           self.encoder.categories_[j] = np.append(self.encoder.categories_[j],data.loc[row,column])
    self.write_encoder()
    return self.encoder
  
  def transform(self,data):
    data = self.get_frame(data)
    with open(self.path, 'rb') as f:
      self.encoder = pickle.load(f)
    return self.encoder.transform(data)
  
  def fit_transform(self,data):
    data = self.get_frame(data)
    self.fit(data)
    return self.encoder.transform(data)
    
    
class CommonFeatureEncoding(IndependentFeatureEncoding):
  def __init__(self, path):
    super().__init__(path)
    self.categories = self.encoder.categories_[0].copy()
  
  def fit(self,data):
    data = self.get_frame(data)
    for row in range(len(data)):
      for column in self.encoder.feature_names_in_:
        if data.iloc[row][column] not in self.categories:
           self.categories = np.append(self.categories,data.loc[row,column])
    for i in range(len(self.encoder.categories_)):
      self.encoder.categories_[i] = self.categories
    self.write_encoder()
    return self.encoder
  
  def fit_transform(self,data):
    data = self.get_frame(data)
    self.fit(data)
    return self.encoder.transform(data)
  
  

class DataPreprocessor:
  def __init__(
    self,
    path,
    passions_enc_name,
    lang_enc_name,
    rem_enc_name,
  ):
    self.passion_encoder = CommonFeatureEncoding(os.path.join(path,passions_enc_name))
    self.language_encoder = CommonFeatureEncoding(os.path.join(path,lang_enc_name))
    self.rem_encoder = IndependentFeatureEncoding(os.path.join(path,rem_enc_name))
  
  def get_frame_from_cols(self,dataset,cols):
    return dataset[cols].astype('object', copy = False )
  
  def copy_frame(self,data):
    if isinstance(data,pd.Series):
      frame = pd.DataFrame(data ).T
      return frame
    else:
      return data.copy()
    
  pd.DataFrame().copy
  def preprocess_data(self,_data):
    data = self.copy_frame(_data)
    
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
    _item_data = self.preprocess_data(item_data)[item_feat].astype(np.float64).to_numpy()
    # item_data['language_score'] = np.expand_dims(np.sum(np.vectorize(self.lang_scorer.predict)(lang),axis = 1),axis = 1)
    # item_data['passion_score'] = np.expand_dims(np.sum(np.vectorize(self.passion_scorer.predict)(passion),axis = 1),axis = 1)
    return _item_data
    
  def reset_encoders(self,obj_path,*names):
    for name in names:
        with open (os.path.join(obj_path ,f'dummy_{name}.bin'),'rb') as f:
            dummy = pickle.load(f)
        with open(os.path.join(obj_path ,f'{name}.bin'),'wb') as f:
            pickle.dump(dummy,f)
  def get_data_from_bin(self,path):
    with open (path, 'rb') as f:
      data = pickle.load(f)
    return data

  
class ModelEvaluator:
  def __init__(
    self,
    user_clf_path,
    cbf_model_path,
    obj_path,
    passions_enc_name,
    lang_enc_name,
    rem_enc_name,
    
  ) -> None:
    self.user_clf = load_model(user_clf_path)
    self.cbf_model = load_model(cbf_model_path)
    self.pre = DataPreprocessor(obj_path,passions_enc_name,lang_enc_name,rem_enc_name)
    
  def get_user_clf_pred(self,data):
    _data = self.pre.preprocessing_user_clf(data,model_features.user_clf_features)
    return self.user_clf.predict(_data)
  
  def get_cbf_pred(self,data):
    user_data = self.pre.get_data_from_bin('D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/data/user_data.bin')
    _data = self.pre.preprocessing_cbf_clf(user_data,data, model_features.user_clf_features, model_features.user_clf_features)
    return self.user_clf.predict(_data)
  
    
  
  


# pre.reset_encoders('D:/Programming Languages/Python/.Python Projects/TInder Recommendation system/obj','lang_enc','rem_enc','passions_enc')