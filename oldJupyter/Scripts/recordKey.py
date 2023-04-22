from pynput.keyboard import Key, Listener, KeyCode
import datetime
import pandas as pd

keyPressed = []
inputDf = None

def saveFile():
    inputDf = pd.DataFrame.from_records(keyPressed, columns = ["TS", "Key", "Activity"])
    inputDf.to_csv("cupheadkb.tsv", sep = '\t', header = False, index = False)

def on_press(key):
    if key == Key.delete:
        saveFile()
        return False
    try:
        key = key.char.lower()
    except:
        pass
    if len(keyPressed)==0:
        keyPressed.append((datetime.datetime.now(),key,"pressed"))
    elif keyPressed[-1][2]!="pressed":
        keyPressed.append((datetime.datetime.now(),key,"pressed"))
    elif keyPressed[-1][1]!=key:
        keyPressed.append((datetime.datetime.now(),key,"pressed"))

def on_release(key):
    # print('{0} release'.format(
    #     key.lower()))
    # print(datetime.datetime.now())
    try:
        key = key.char
    except:
        pass
    keyPressed.append((datetime.datetime.now(),key,"released"))

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()