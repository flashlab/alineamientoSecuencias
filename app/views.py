import os, json
from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, make_response
from app import app
from controllers import gen as D
from controllers import referenceType as R
from controllers import globalData as G
from controllers import globalIdentity as I
from controllers import alineamientoLocal
from controllers import entrezApi
from controllers import a as alignment2
from werkzeug import secure_filename
import pandas_highcharts
import pandas as pd
from pandas_highcharts.core import serialize


from flask_bootstrap import Bootstrap
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy

app.config['SECRET_KEY'] = 'root'
    #'Jy_s4DMd9jxqpRu1GkpQs1PVP0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pcalderon:pcalderon@localhost:5432/postgres'
    #'postgres://jtawbodqmjuxhw:Jy_s4DMd9jxqpRu1GkpQs1PVP0@ec2-54-235-92-236.compute-1.amazonaws.com:5432/d9noa5jj4opojt'
db = SQLAlchemy(app)

@app.route('/')
def homepage():
    gI = I.GlobalIdentity.query.all()
    refArray = []
    for g in gI:
        refArray.append(R.referenceType.query.get(g.type))
    return render_template("alignment.html", types=refArray)


@app.route('/resistanceTest')
def resistanceTest():
    gI = I.GlobalIdentity.query.all()
    refArray = []
    for g in gI:
        refArray.append(R.referenceType.query.get(g.type))
    return render_template("alignment.html", types= refArray)

@app.route('/runAlignment', methods=['POST'])
def runAlignment():
    errors = ''
    genA = ''
    genB = ''
    fileB = request.files['genBFile']
    genA = getReferenceGen(request.form['genA'])
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


@app.route('/runAlignment2', methods=['POST'])
def runAlignment2():
    errors = ''
    genA = ''
    genB = ''
    fileB = request.files['genBFile']
    genA = getReferenceGen(request.form['genA'])
    if hasFile(fileB):
        genB = read_file(fileB.filename)
    elif request.form['genB']:
        genB = request.form['genB']
    else:
        errors += 'Please enter a valid gen'
    if not genA and not genB:
        errors = 'Please enter valid gen text/file'
    if not errors:
        result = alignment2.testAlign2(genA, genB)
        sizel = len(result)
        return render_template("resultAlignment.html",
                               genA = genA,
                               genB = genB,
                               result = result,
                               sizel = sizel)
    else:
        return render_template("alignment.html", errors=errors)


@app.route('/readme')
def readme():
    readmeFile = readREADME()
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

@app.route('/searchFasta', methods=['GET'])
def searchFasta():
    term = request.args.get('term')
    myList = entrezApi.searchByTerm(term)
    return json.dumps(myList)


@app.route('/searchFastaSA', methods=['GET'])
def searchFastaSA():
    term = request.args.get('term')
    myList = entrezApi.searchByTerm(term)
    return render_template("entrezAPI.html", list=myList)

@app.route('/selectElement', methods=['GET'])
def selectElement():
    a = request.args.get('genNames')
    print a
    fastaString = entrezApi.getFastaInfo(a)
    response = make_response(fastaString)
    response.headers["Content-Disposition"] = "attachment; filename="+a+".txt"
    return response


@app.route('/generateIdentity', methods=['POST'])
def generateIdentity():
    addGlobalIdentity()
    done = "Global Identity Succesfully Created"
    myTypes = R.referenceType.query.all()
    ref = getTypeForRefs()
    return render_template("references.html", types=myTypes, references=ref, done = done)

@app.route('/saveReference', methods=['POST'])
def saveReference():
    nombre = request.form['name']
    ncbi = request.form['ncbi']
    fasta = request.files['genFile']
    type = request.form['type']
    if hasFile(fasta):
        genFile = read_file(fasta.filename)
    addGlobalData(genFile, type)
    newGen = D.Gen(nombre, genFile, ncbi, False, type)
    newGen.add(newGen)
    myTypes = R.referenceType.query.all()
    ref = getTypeForRefs()
    return render_template("references.html", types=myTypes, references=ref)


@app.route('/reference')
def reference():
    types = R.referenceType.query.all()
    ref = getTypeForRefs()
    return render_template("references.html", types=types, references=ref)

@app.route('/graphics')
def graphics():
    gI = G.GlobalData.query.all()
    newArray = []
    for i in gI:
        print i
        dicA = { 'Quantity': i.qty,'Position':i.position, 'Letter': i.letter, 'Type':i.type }
        newArray.append(dicA)
    df = pd.DataFrame(newArray)

    chart = serialize(df, render_to='my-chart', output_type='json')
    return render_template("graphics.html", chart=chart)

# ///////////////////
# HELPERS
# //////////////////

def getTypeForRefs():
    myReferences = D.Gen.query.all()
    ref = []
    for x in myReferences:
        newRef = []
        newRef.append(x.nombre)
        newRef.append(x.ncbi_id)
        newRef.append(getTypeReference(x.type))
        ref.append(newRef)
    return ref

def getTypeReference(id):
    refType = R.referenceType.query.all()
    for x in refType:
        if x.id == id:
            return x.type

def addGlobalData(seq, type):

    index = 0
    for x in seq:
        idPosition = getPositionCreated(index, type, x)
        if (idPosition > 0):
            updateData = G.GlobalData.query.get(idPosition)
            updateData.qty += 1
            updateData.update()
        else:
            newData = G.GlobalData(index, x, type, 1)
            newData.add(newData)
        index+= 1

def getPositionCreated(i, type, x):
    globalData = G.GlobalData.query.all()
    for g in globalData:
        if g.position == i and g.type == int(type) and str(g.letter) == x:
            return g.id
    return -1

def getReferenceGen(genType):
    gI = I.GlobalIdentity.query.filter(I.GlobalIdentity.type == genType)
    for g in gI:
        return g.sequence

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
    return ''.join(genArray).replace('\n', '')

def readREADME():
    gen = D.Gen.query.all()
    print gen
    filename = secure_filename('README.md')
    file = open(filename)
    fileArray = []
    for line in file:
        fileArray.append(line)
        fileArray.append("<br>")
    return ''.join(fileArray)


def hasFile(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    return False

def addGlobalIdentity():
    if D.Gen.query.filter(D.Gen.compared == False).count() > 0:
        types = R.referenceType.query.all()
        for t in types:
            data = G.GlobalData.query.order_by(G.GlobalData.position).filter(G.GlobalData.type==t.id)
            seqArray = []
            seqString = ""
            for d in data:
                seqArray.append(getMaxPositionLetter(data, d.position))
            seqString =''.join(seqArray)
            if len(seqString) > 0:
                if I.GlobalIdentity.query.filter(I.GlobalIdentity.type == t.id).count() > 0:
                    updateGlobalIdentity(t.id, seqString)
                else:
                    newIdentity = I.GlobalIdentity(seqString, t.id)
                    newIdentity.add(newIdentity)
            genList = D.Gen.query.filter(D.Gen.type==t.id)
            for g in genList:
                g.compared = True
                g.update()


def updateGlobalIdentity(type, seq):
    gI = I.GlobalIdentity.query.filter(I.GlobalIdentity.type == type)
    for g in gI:
        updateGI = I.GlobalIdentity.query.get(g.id)
        updateGI.sequence = seq
        updateGI.update()



def getMaxPositionLetter(data, pos):
    max = -1
    letter = 'N'
    for d in data:
        if d.position == pos and d.qty > max:
            letter = d.letter
            max = d.qty
    return letter


