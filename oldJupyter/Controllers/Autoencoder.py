#!/usr/bin/env python
# coding: utf-8

# In[78]:


import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import EarlyStopping
from keras.layers import LSTM,GRU, Dense, RepeatVector, TimeDistributed, UpSampling1D
from keras.models import Model, Sequential
from keras.utils import plot_model
import tensorflow as tf


# In[79]:


a = np.load("../Data/Chunkized/cupheadkb.npz", allow_pickle=True)["x"]                 #take the keyboard inputs displayed as 0 and 1
print(a.shape)


# In[80]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Define model
seq = a.shape[1]                                   # Sequence length
features = a.shape[2]                              #number of features

model = Sequential()
model.add(GRU(seq*3, input_shape=(seq , features)))   #using GRU, convert to vector of size 12 (encoding)
model.add(RepeatVector(seq))                          #(decode by reshaping vector to size 4,12)
model.add(GRU(features,return_sequences=True))        #change shape to 4,10 to match the original
model.compile(optimizer='adam', loss='mse')           #compile model
# Print model summary
model.summary()


# In[81]:


es = EarlyStopping(patience=10, monitor="loss")           #using early stop run the autoencoder epoch number of times
h = model.fit(a, a, epochs=150, callbacks=[es])


# In[82]:


def plot_loss(history):                                   #function to plot loss data
    plt.plot(history.history['loss'], label='loss')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.legend()


# In[83]:


plot_loss(h)


# In[84]:


encoder = Model(inputs=model.inputs, outputs=model.layers[0].output)           #create encoder


# In[85]:


encoder1 = encoder.predict(np.load("../Data/Chunkized/cupheadkb.npz", allow_pickle=True)["x"])    #predict data using encoder


# In[86]:


np.save("../Data/AutoEncoded/cup1Enc", encoder1)


# In[ ]:




