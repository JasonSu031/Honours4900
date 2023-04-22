import os,io
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

if __name__ == '__main__':
    app.run(debug=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getLast(dir):
    files = os.listdir(dir)
    paths = [os.path.join(dir, basename) for basename in files]
    return max(paths, key=os.path.getctime)

@app.route("/getTSV")
def getTSV():
    return send_file(
        os.path.join(app.config['UPLOAD_TOANNO'],"cupheadkb.tsv"),
        mimetype = "text/tsv",
        download_name="cupheadkb.tsv",
        as_attachment=True
    )

@app.route("/test")
def displayLast():
    g=getLast(app.config['UPLOAD_RAW'])
    return  g

@app.route("/")
def home():
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
            flash('No file uploaded', 'error')
            return redirect (url_for('step2'))
        elif not allowed_file(f.filename):
            flash('Wrong file extension type', 'error')
            return redirect (url_for('step2'))
        else:
            flash('File Added', 'success')
            fName = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_RAW'],fName))    
            annotateData(app.config['UPLOAD_RAW'],app.config['UPLOAD_ACTION'],fName)
            dataToAnnotate(app.config['UPLOAD_RAW'],app.config['UPLOAD_TOANNO'],fName)
            return redirect (url_for('step3'))
            
@app.route("/uploadAnnotation", methods = ['GET', 'POST'])
def uploadAnnotation():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            flash('No file uploaded', 'error')
            return redirect (url_for('step3'))
        elif not allowed_file(f.filename):
            flash('Wrong file extension type', 'error')
            return redirect (url_for('step3'))
        else:
            flash('File Added', 'success')
            fName = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_ANNOTATED'],fName))    
            return redirect (url_for('step4'))

@app.route("/createModel", methods = ['GET', 'POST'])
def createModel():
    resample = request.form["resample"]+"ms"
    frames = request.form["frames"]
    binaryVals = binaryVectorize(app.config['UPLOAD_ACTION'],app.config['UPLOAD_ANNOTATED'],"cupheadkb.tsv",resample)
    x,y=splitSeq(binaryVals,int(frames))
    # createAuto(x,y)
    cupheadEnc = keras.models.load_model('cupheadEnc.h5')
    encoded = cupheadEnc.predict(x)
    kmean(app.config['IMAGES'], encoded, y)
    return redirect (url_for('step4'))

@app.route("/keyRec", methods = ["GET","POST"])
def getScript():
    return send_file(
        os.path.join(app.config['CODE_SRC'],'recordKey.py'),
        mimetype = "text/x-python",
        download_name="script.py",
        as_attachment=True
    )