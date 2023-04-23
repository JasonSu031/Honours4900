#!/usr/bin/env python
# coding: utf-8

# In[2]:
import os
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib 
from umap import UMAP
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# In[3]:

def kmean(iPath,encoded,y, clusters):
    actionList = []  # add all actions to list of actions
    for act in y:
        actionList.append(act)
    unique = []
    for act in y:
        if not act in unique:
            unique.append(act)

    colorMapping = ['red', 'blue','green','brown','tan','slategray','aqua','violet','mediumpurple','black']  # json for colors
    colors = np.array([colorMapping[unique.index(color)] for color in actionList])
    reducer = UMAP()
    dataTrans = reducer.fit_transform(encoded)
    kmeans = KMeans(n_clusters=clusters,
                    random_state=0, n_init="auto").fit(dataTrans)
    centers = kmeans.cluster_centers_
    centerX = centers[:, 0]
    centerY = centers[:, 1]
    x = dataTrans[:, 0]
    y = dataTrans[:, 1]
    
    plt.figure(figsize=(16,16))  # set the size of figure
    ax = plt.subplot(111)

    for i in range(len(unique)):
        ax.plot(colorMapping[i], label=unique[i])
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.scatter(  # plot the gameplay data
        x, y, c=colors
    )
    plt.scatter(  # plot the centroids
        centerX, centerY, c='orange'
    )
    plt.savefig(os.path.join(iPath,"plot.png"))
    plt.clf()

# take x coordinates and y coordinates from the gameplay data


# In[4]:


# actions = np.load("../Data/Chunkized/cupheadkb.npz", allow_pickle=True)["y"]


# In[5]:

# In[7]:

# colorMapping = {'loading':'red', 'death':'black','map':'brown','play':'blue','win':'green'} #json for colors
# colors = np.array([colorMapping[color] for color in actionList])                            #maps the state of the game to colors
# print(colors)

# In[68]:


# reducer = UMAP()                         #create a new UMAP


# In[69]:


# dataTrans = reducer.fit_transform(a)     #fit the data points to the UMAP


# In[76]:


# create a k means
# kmeans = KMeans(n_clusters=len(colorMapping), random_state=0, n_init="auto").fit(dataTrans)


# In[79]:


# get the data for the center of the clusters
# centers = kmeans.cluster_centers_


# In[80]:


# take x coordinates and y coordinates from k-means center data
# centerX = centers[:,0]
# centerY = centers[:,1]


# In[82]:


# x = dataTrans[:, 0]        #take x coordinates and y coordinates from the gameplay data
# y = dataTrans[:,1]
# plt.pyplot.figure(figsize=(16,16))  #set the size of figure
# plt.pyplot.scatter(                 #plot the gameplay data
#     x,y,c = colors
# )
# plt.pyplot.scatter(                 #plot the centroids
#     centerX, centerY, c = 'yellow'
# )


# In[ ]:
