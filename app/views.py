import os
from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from app import app
from controllers import alineamientoLocal
from controllers import entrezApi
# from controllers import pExample
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
from os.path import join, dirname, realpath
# import subprocess as sub

# app.config['UPLOAD_FOLDER'] = '/app/uploads/'
# These are the extension that we are accepting to be uploaded
# app.config['ALLOWED_EXTENSIONS'] = set(['fasta'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def read_file(filename):
    filename = secure_filename(filename)
    fastaFile = open(app.config['UPLOAD_FOLDER']+filename)
    fastaFile.readline()
    genArray = []
    for line in fastaFile:
        genArray.append(line)
    return ''.join(genArray)

def read_README():
    filename = secure_filename('README.md')
    file = open(filename)
    fileArray = []
    for line in file:
        fileArray.append(line)
        fileArray.append("<br>")
    return ''.join(fileArray)

@app.route('/')
def homepage():
    return render_template("alignment.html")


@app.route('/gen/comparison')
def genComparison():
    return render_template("alignment.html")

def hasFile(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    return False

@app.route('/runAlignment', methods=['POST'])
def runAlignment():
    errors = ''
    genA = ''
    genB = ''
    fileA = request.files['genAFile']
    fileB = request.files['genBFile']
    if hasFile(fileA):
        genA = read_file(fileA.filename)
    elif request.form['genA']:
        genA = request.form['genA']
    else:
        errors += 'Please enter a valid first gen'
    if hasFile(fileB):
        genB = read_file(fileB.filename)
    elif request.form['genB']:
        genB = request.form['genB']
    else:
        errors += 'Please enter a valid second gen'
    if not genA and not genB:
        errors = 'Please enter valid gen text/file'
    if not errors:
        result = alineamientoLocal.generateLocalAlignment(genA, genB)
        return render_template("resultAlignment.html",
                               genA = genA,
                               genB = genB,
                               substring1 = result[0],
                               substring2 = result[1],
                               stringMinor = result[2],
                               simt = result[3])
    else:
        return render_template("alignment.html", errors=errors)


@app.route('/readme')
def readme():
    readmeFile = read_README()
    return render_template("readme.html", readmeText=readmeFile)

@app.route('/about')
def aboutpage():
    return render_template("about.html")


@app.route('/about/contact')
def contactPage():
    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)

@app.route('/entrezAPI')
def entrezAPI():
    return render_template("entrezAPI.html")

@app.route('/searchFasta', methods=['POST'])
def searchFasta():
    myList = entrezApi.searchByTerm(request.form['term'])
    # for i in myList:
    #     print (i)
    return render_template("entrezAPI.html", list=myList)
    # return jsonify(list=myList)

@app.route('/selectElement', methods=['POST'])
def selectElement():
    fastaString = entrezApi.getFastaInfo(request.form['genItem'])
    return render_template("alignment.html", genA=fastaString )


@app.route('/runParallel', methods=['POST'])
def runParallel():
    os.system('cd')
    os.system("cd app/controllers; python pExample.py "+request.form['workers'])
    # i = request.form['workers']
    # binary = os.urandom(7)
    # # i = int(i)
    # results = pExample.sum_parallel(i)
    return render_template("parallel.html")


@app.route('/parallel')
def parallel():
    return render_template("parallel.html")
