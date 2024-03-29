import os,io, glob
from flask import Flask, render_template, flash, request, redirect, url_for, send_file, Response
from werkzeug.utils import secure_filename

import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.callbacks import EarlyStopping
from keras.layers.core import Dense, RepeatVector
from keras.models import Model, Sequential, load_model
from keras.utils import plot_model
from sklearn.cluster import KMeans
import pandas as pd
from umap import UMAP
matplotlib.use('Agg')

from src.MapInputs import annotateData
from src.MapInputs import dataToAnnotate
from src.CustomizedIntervals import binaryVectorize
from src.Chunking import splitSeq
from src.Autoencoder import createAuto
from src.KMeans import kmean

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_RAW= "./data/rawInput"
app.config['UPLOAD_RAW'] = UPLOAD_RAW

UPLOAD_ACTION = "./data/action"
app.config['UPLOAD_ACTION'] = UPLOAD_ACTION

UPLOAD_TOANNO = "./data/toAnnotate"
app.config['UPLOAD_TOANNO'] = UPLOAD_TOANNO

UPLOAD_ANNOTATED = "./data/annotated"
app.config['UPLOAD_ANNOTATED'] = UPLOAD_ANNOTATED

AUTOENCODER = "./data/autoencoder"
app.config['AUTOENCODER'] = AUTOENCODER

CODE_SRC = "./src"
app.config['CODE_SRC'] = CODE_SRC

IMAGES = "./static/images"
app.config['IMAGES'] = IMAGES

ALLOWED_EXTENSIONS = {'tsv'}

fileName = None

if __name__ == '__main__':
    app.run(debug=True)

def allowed_file(filename):                                                     #check if extension allowed
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def setFileName():
    global fileName
    fileName= str(getLast(UPLOAD_RAW))+".tsv"
    
def getLast(dir):
    files = len(os.listdir(dir))
    return str(files)

@app.route("/getTSV")                                                           #returns annotated tsv file as download
def getTSV():
    if fileName is None:
        return redirect(url_for('noName'))
    fName = fileName
    return send_file(
        os.path.join(app.config['UPLOAD_TOANNO'],fName),
        mimetype = "text/tsv",
        download_name=fName,
        as_attachment=True
    )

@app.route("/")                                                                 #home page
def home():
    try:
        os.remove(os.path.join(app.config['IMAGES'], "plot.png"))
    except:
        pass
    return render_template("home.html", title = "Welcome")

@app.route("/upload")
def uploadFile():
    return render_template("upload.html", title = "How it works?")

@app.route("/predict")
def annotate():
    return render_template("predict.html", title = "Predict your data")

@app.route("/upload/step1")
def step1():
    return render_template("step1.html", title = "")

@app.route("/upload/step2")
def step2():
    setFileName()
    return render_template("step2.html", title = "")

@app.route("/upload/step3")
def step3():
    return render_template("step3.html", title="")

@app.route("/upload/step4")
def step4():
    return render_template("step4.html", title = "")

@app.route("/uploadInput", methods = ['GET', 'POST'])
def uploadInput():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            flash('Please Select File to Upload', 'error')
            return redirect (url_for('step2'))
        elif not allowed_file(f.filename):
            flash('Wrong File Extension Type', 'error')
            return redirect (url_for('step2'))
        else:
            if fileName is None:
                return redirect(url_for('noName'))
            flash('Recorded Input File Added', 'success')
            fName = fileName
            f.save(os.path.join(app.config['UPLOAD_RAW'],fName))    
            annotateData(app.config['UPLOAD_RAW'],app.config['UPLOAD_ACTION'],fName)
            dataToAnnotate(app.config['UPLOAD_RAW'],app.config['UPLOAD_TOANNO'],fName)
            return redirect (url_for('step3'))
            
@app.route("/uploadAnnotation", methods = ['GET', 'POST'])
def uploadAnnotation():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            flash('Please Select File to Upload', 'error')
            return redirect (url_for('step3'))
        elif not allowed_file(f.filename):
            flash('Wrong File Extension Type', 'error')
            return redirect (url_for('step3'))
        else:
            if fileName is None:
                return redirect(url_for('noName'))
            flash('Annotation File Added', 'success')
            fName = fileName
            f.save(os.path.join(app.config['UPLOAD_ANNOTATED'],fName))    
            return redirect (url_for('step4'))

@app.route("/createModel", methods = ['GET', 'POST'])
def createModel():
    if fileName is None:
        return redirect(url_for('noName'))
    fName = fileName
    # fName = "0.tsv"
    clusters = 0
    resample = request.form["resample"]+"ms"
    frames = int(request.form["frames"])
    clusters = int(request.form["clusters"])

    binaryVals = binaryVectorize(app.config['UPLOAD_ACTION'],app.config['UPLOAD_ANNOTATED'],fName,resample)
    x,y=splitSeq(binaryVals,int(frames))

    if frames==4:
        cupheadEnc = keras.models.load_model('cupheadEnc4.h5') 
    else:
        cupheadEnc = createAuto(x)

    encoded = cupheadEnc.predict(x)
    kmean(app.config['IMAGES'], encoded, y, clusters)
    return redirect (url_for('step4'))

@app.route("/keyRec", methods = ["GET","POST"])
def getScript():
    return send_file(
        os.path.join(app.config['CODE_SRC'],'recordKey.py'),
        mimetype = "text/x-python",
        download_name="script.py",
        as_attachment=True
    )

@app.route("/nonName")
def noName():
    flash('An error occurred, please restart your process', 'error')
    return redirect (url_for('step1'))


