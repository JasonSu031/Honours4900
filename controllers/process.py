import pandas as pd
import csv
import json

key_mapping = {"w": "FWD", "a": "LEFT", "s": "BACK", "d": "RIGHT",                        #keys and what they do taken from pubG
               "shift": "WALK", "ctrl_l": "CROUCH", "space": "JUMP",
               "f": "INTRACT", "4": "OBJ",
               "r": "RLD", "(0, -1)": "WPN_SWTCH", "(0, 1)": "WPN_SWTCH",
               "!": "WPN_SWTCH",
               "1": "WPN_SWTCH", "2": "WPN_SWTCH", "e": "WPN_SWTCH", "3": "KNIFE",
               "q": "SKL", "c": "SKL", "h": "SKL", "x": "SKL",
               "left": "SHOOT", "right": "AIM",
              }

uniqueList = []                                                                         

def createUnique(dataFile):                                                             #this method creates a unique list of key inputs entered by user      
    with open(dataFile, newline='') as f:                                               #not very useful so please ignore
        df = pd.read_csv(dataFile, sep='\t', header=None)
        for index, row in df.iterrows():
            temp = row[1]
            if(uniqueList.count(temp)==0):
                uniqueList.append(temp)
    print(uniqueList)

    
    
def annotateData(dataFile):                                                             #this method annotates the keys pressed given file name
    with open(dataFile, newline='') as f:                                               #open the file to be annotated
        df = pd.read_csv(dataFile, sep = '\t', header=None)                             #create a dataframe of file that needs annotation
        #df.to_csv(dataFile, index=False, sep='\t')
        #print(df)
        keyCol = df.iloc[:,-2]                                                          #this only takes the column of user inputs (ex. w, a, s, d)
        #print(keyCol)
        #print(df)
        keyCol = keyCol.map(key_mapping).to_frame().fillna("other")                     #match the user inputs with the key_mapping json data, then convert it to a dataframe and replace all NaN values with other
                                                                                        #this creates the annotations
        df2 = pd.merge(df, keyCol, left_index=True, right_index=True)                   #merge the original file that needs annotations with the annotations
#         print(df2.to_string)
        df2.to_csv("annotated"+dataFile,sep = '\t', header=None, index = False)         #create a new csv file and place the annotated data within it
            


#createUnique(dataFile)
annotateData("Keyboard.tsv")                                                            #run the code on Keyboard.tsv and mouse.tsv
annotateData("mouse.tsv")

