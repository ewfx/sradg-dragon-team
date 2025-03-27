from keras.src.losses import MeanSquaredError
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
from data_processing.process_data import  DataProcessing
import tensorflow as tf
from model.model import Model
import keras
from sklearn.model_selection import train_test_split
import numpy as np


class Autoencoder(Model):
    _model = None
    def __init__(self, **kwargs):
        tf.config.list_physical_devices('CPU')
        super().__init__(**kwargs)


    def __autoencoder_anomaly_detection(self,df, encoding_dim, epochs, batch_size):

          scaled_data = self.scale_data(df)
          x_train, x_val = train_test_split(scaled_data, test_size=0.2, random_state=42)


          input_dim = scaled_data.shape[1]
          input_layer = keras.layers.Input(shape=(input_dim,))
          encoder = keras.layers.Dense(encoding_dim, activation="relu", kernel_regularizer=keras.regularizers.l2(0.001))(input_layer)
          decoder = keras.layers.Dense(input_dim, activation="sigmoid")(encoder)

          autoencoder = keras.Model(inputs=input_layer, outputs=decoder)
          autoencoder.compile(optimizer=keras.optimizers.Adam(learning_rate=0.05), loss=MeanSquaredError())

          early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

          autoencoder.fit(x_train, x_train, epochs=epochs, batch_size=batch_size, shuffle=True, validation_data=(x_val, x_val), callbacks=[early_stopping], verbose=0)
          self._model = autoencoder
          autoencoder.save('data/model/autoencoder_model.h5')
          return autoencoder



    def scale_data(self,df, scaler=StandardScaler()):
        scaled_df = scaler.fit_transform(df)
        return scaled_df

    def generate_model(self,**kwargs):
        try:
            df = kwargs['df']
            encoding_dim, epochs, batch_size = kwargs['encoding_dim'], kwargs['epochs'], kwargs['batch_size']
            autoencoder = self.__autoencoder_anomaly_detection(df, encoding_dim, epochs, batch_size)
            return autoencoder
        except Exception as e:
            print(e)


    def get_model(self,file="data/train_data.csv"):
        if self._model is None:
            try:
                custom_objects = {'mse': MeanSquaredError()}
                self._model = keras.models.load_model('data/model/autoencoder_model.h5',custom_objects=custom_objects)
            except FileNotFoundError:
                data_frame,_ = DataProcessing(file).process_data_cleanup()
                self._model = self.generate_model(df=data_frame,encoding_dim=2, epochs=2, batch_size=32)
        return self._model


    def predict(self,test_df,y_true):
        scaled_data = self.scale_data(test_df)
        model = self.get_model()
        reconstructions = model.predict(scaled_data, verbose=0)
        mse = np.mean(np.power(scaled_data - reconstructions, 2), axis=1)
        mse_scores= pd.Series(mse)
        threshold = np.percentile(mse_scores, 93)
        anomalies_autoencoder = (mse_scores > threshold).astype(int)
        return anomalies_autoencoder


