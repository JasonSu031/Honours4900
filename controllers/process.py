import pandas as pd
import csv
import json

key_mapping = {"w": "FWD", "a": "LEFT", "s": "BACK", "d": "RIGHT",
               "shift": "WALK", "ctrl_l": "CROUCH", "space": "JUMP",
               "f": "INTRACT", "4": "OBJ",
               "r": "RLD", "(0, -1)": "WPN_SWTCH", "(0, 1)": "WPN_SWTCH",
               "!": "WPN_SWTCH",
               "1": "WPN_SWTCH", "2": "WPN_SWTCH", "e": "WPN_SWTCH", "3": "KNIFE",
               "q": "SKL", "c": "SKL", "h": "SKL", "x": "SKL",
               "left": "SHOOT", "right": "AIM"}

dataFile = "Keyboard.tsv"

def annotateData(dataFile):
    with open(dataFile, newline='') as f:
        df = pd.read_csv(dataFile, sep = '\t')
        with open('annotedData.tsv', 'w', newline='') as f_output:
            #for index, row in df.iterrows():
                for key, value in key_mapping.items():
                    if (pd.read_csv(dataFile, header = None, sep = '\t')[1]== key).bool():
                        print(key)
                    #     tsv_output = csv.writer(f_output, delimiter = '\t')
                    #     tsv_output.writerow(row.append(value))
                    
                
    #print(pd.read_csv(dataFile, header = None, sep = '\t'))


annotateData(dataFile)
