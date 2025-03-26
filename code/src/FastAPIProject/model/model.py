from abc import ABC, abstractmethod

from sklearn.preprocessing import StandardScaler


class Model(ABC):

    def __init__(self, model):
        self.model = model

    @abstractmethod
    def scale_data(self,df,scaler=StandardScaler()):
        pass

    @abstractmethod
    def generate_model(self,**kwargs):
        pass
    @abstractmethod
    def get_model(self):
        pass
    @abstractmethod
    def predict(self,test_df,y_true):
        pass
