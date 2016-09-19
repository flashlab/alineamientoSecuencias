import os
from flask import Flask, render_template, request, redirect, url_for, abort, session
from app import app
from controllers import alineamientoLocal
from werkzeug import secure_filename
from sys import argv

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


@app.route('/')
def homepage():
    title = "Epic Tutorials"
    paragraph = [
        "wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!",
        "wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!"]
    try:
        return render_template("index.html", title=title, paragraph=paragraph)
    except Exception, e:
        return str(e)


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
    print("Hello")
    print(errors)
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

@app.route('/about')
def aboutpage():
    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)


@app.route('/about/contact')
def contactPage():
    title = "About this site"
    paragraph = ["blah blah blah memememememmeme blah blah memememe"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)
