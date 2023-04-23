#!/usr/bin/env python
# coding: utf-8

# In[49]:

import os
import pandas as pd
import csv
import json
from datetime import datetime
import datetime


# In[50]:


fileName = "Cuphead.json"


# In[51]:


def defineMap(fileName):                                        #open json file and return it
    with open(fileName, 'r') as f:
        keyMapping = json.load(f)
        return keyMapping


# In[52]:


# try:                                                            #try to open json file
#     keyMapping = defineMap(fileName)
# except:
#     print("json file does not exist")


# In[53]:


def readFile(dataFile):                                        #read file and return action column data "jump", "dash"
    df = pd.read_csv("../Data/UserInput/"+dataFile, sep = '\t', header=None)
    actionCol = df.iloc[:,-1]
    return actionCol


# In[54]:


def addInterval(dataframe):                                   #return time passed since start of recording
    elapsed = dataframe
    elapsed = elapsed.rename("elapsed")
    start = elapsed.iloc[0]                                   #timestamp of beginning of recording
    elapsed = elapsed.apply(lambda x:str(datetime.timedelta(seconds=(x-start).seconds))+":"+str(int((x-start).microseconds/1000)))   #find difference of current time and start time for each time
    return elapsed


# In[55]:


def clean_inputs(keyCol):                                     #remove the useless letters from keys ie. remove Button from Button.J
    keyCol = keyCol.str.replace("Button\.", '', regex=True)
    keyCol = keyCol.str.replace("Key\.", '', regex=True)
    return keyCol


# In[56]:


def annotateData(iPath,oPath,dataFile):                                              #open the file to be annotated
    df = pd.read_csv(os.path.join(iPath,dataFile), sep = '\t', header=None, names = ["TS", "key", "action"])                             #create a dataframe of file that needs annotation
    df.TS = df.TS.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))  #change Timestamp string to date format
    keyCol = df.iloc[:,-2]                                                          #this only takes the column of user inputs (ex. w, a, s, d)
    cleanedKey = clean_inputs(keyCol)                                               #clean the inputs by removing Button. and Key. from key inputs
    keyCol = cleanedKey.copy()
    keyCol = keyCol.map(defineMap("Cuphead.json")).to_frame().fillna("other")                      #match the user inputs with the key_mapping json data, then convert it to a dataframe and replace all NaN values with other
    df2 = pd.merge(df, keyCol, left_index=True, right_index=True)                   #merge the original file that needs annotations with the annotations
    df2.insert(1, "col1",cleanedKey)                                                #insert the clenaed inputs
    df2 = df2.drop("key_x", axis = 1)                                               #drop old key column
    df2 = df2.drop(df2[df2.action =="other"].index)                                 #drop all rows with other keys
    # print(df2)
    df2.to_csv(os.path.join(oPath,dataFile),sep = '\t', header=None, index = False)


# In[57]:


def dataToAnnotate(iPath,oPath,dataFile):
    df = pd.read_csv(os.path.join(iPath,dataFile), sep = '\t', header = None, names = ["TS", "Key", "Action"])   #
    df = df.iloc[:,0]                                                                                             #get timestamp row
    df = df.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))                                 #change timestamp string to datetime
    elapsed = addInterval(df)                                                                                     #get the time elapsed data column
    toAnnotate = pd.concat([df, elapsed], axis = 1)                                                               #add elapsed data to original dataframe
    # print(toAnnotate)
    toAnnotate.to_csv(os.path.join(oPath,dataFile), sep = '\t', header = None, index = False)  #save file with actions performed data


# In[59]:



# In[110]:


# try:
#     dataToAnnotate("cupheadkb.tsv")
# except:
#     print("Failed to annotate keyboard data")


# In[ ]:




