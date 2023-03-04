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

uniqueKeys = []
# def writeToFile():
#     with open('output.tsv', 'w', newline='') as f_output:
#         tsv_output = csv.writer(f_output, delimiter=' ')
#         tsv_output.writerow(data)

def createUniqueList():                                                 #this function strips '' from keys and outputs all the unique keys
    with open('Keyboard.tsv', newline = '') as f:                       #not sure if this function is necessary or not
        reader = csv.reader(f)
        with open('uniqueKeys.tsv', 'w', newline='') as fOutput:
            
            for row in reader:
                curKey = row[1].split()[1]
                if curKey[0]=='\'':
                    curKey = curKey[1:-1]
                if uniqueKeys.count(curKey)==0:
                    uniqueKeys.append(curKey)
                    unique_output = csv.writer(fOutput)
                    unique_output.writerow([curKey])
                    


def addAnnotation():
    with open('Keyboard.tsv', newline='') as f:                             #open the Keyboard.tsv file to annotate
        reader = csv.reader(f)
        with open('output.tsv', 'w', newline='') as f_output:               #create a new output file called output.tsv
            for row in reader:                                              #read each row in Keyboard.tsv file
                if(row[1].split()[1]=='w'):                                 #if the button pressed is w, find what command w is mapped to in the json data stored in var mapping
                     tsv_output = csv.writer(f_output, delimiter = ' ')     
                     row.append(json.loads(json.dumps(mapping))[0]["w"])    #append this command and output it to output.tsv
                     tsv_output.writerow(row)                               
                elif(row[1].split()[1]=='a'):                               #if the button pressed is a, find what command a is mapped to in the json data stored in var mapping
                    tsv_output = csv.writer(f_output, delimiter = ' ')     
                    row.append(json.loads(json.dumps(mapping))[1]["a"])     #append this command and output it to output.tsv
                    tsv_output.writerow(row)
                elif(row[1].split()[1]=='a'):                               #if the button pressed is s, find what command s is mapped to in the json data stored in var mapping
                    tsv_output = csv.writer(f_output, delimiter = ' ')
                    row.append(json.loads(json.dumps(mapping))[2]["s"])     #append this command and output it to output.tsv
                    tsv_output.writerow(row)
                elif(row[1].split()[1]=='d'):
                    tsv_output = csv.writer(f_output, delimiter = ' ')      #same thing but with d
                    row.append(json.loads(json.dumps(mapping))[3]["d"])
                    tsv_output.writerow(row)

createUniqueList()
#addAnnotation()
