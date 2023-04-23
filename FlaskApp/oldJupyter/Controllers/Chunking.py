#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np


# In[53]:


seqLen = 4


# In[54]:


dataFile = "statescupheadkb.tsv"


# In[55]:


def fillDf(dataFile):
    df = pd.read_csv("../Data/ActionState/"+dataFile, sep='\t', header = None, names = ['TS','elapsed', 'crouch', 'dash', 'end', 'jump', 'left', 'lock', 'options', 'right', 'shoot', 'super', 'up', 'annotate'])
    return df.fillna(method="ffill")                                                              #fill all empty vlues in dataframe with previous value


# In[56]:


def dataFrameToArray(dataFile, seqLen):
    df = fillDf(dataFile)                                     #drop unnecessary data columns from dataframe
    df.drop('TS', axis=1, inplace=True)
    df.drop('elapsed', axis = 1, inplace = True)
    df.drop('end', axis = 1, inplace = True)
    annotate = df.annotate[:-seqLen+1]                        #grab the current game state from annotations column as series
    df.drop('annotate', axis = 1, inplace=True)
    arr = df.to_numpy()
    return arr, annotate                                      #return dataframe and annotations


# In[57]:


def splitSeq(dataFile, seqLen, chunk):
    inputArr, annotate= dataFrameToArray(dataFile, seqLen)    #get the binary values for each of the actions and get the annotated data
    window = []
    if not chunk:                                             #if told not to chunkize, set the length of each window to 1              
        seqLen = 1                                            
    for i in range(0,len(inputArr)-seqLen+1):                 #take the values in intervals of size seqLen
        z = inputArr[i:i+seqLen].tolist()                     #convert these intervals to a list
        window.append(z)
    window = np.array(window)                                 #convert window to numpyarray
    print(type(window))
    return window, annotate


# In[58]:


x,y = splitSeq(dataFile,seqLen, True)                         
display(x,y)


# In[59]:


np.savez("../Data/Chunkized/"+dataFile[6:-4], x=x,y=y)      #save as npz file


# In[ ]:




