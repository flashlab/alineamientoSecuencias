from flask import Flask
from flask_bootstrap import Bootstrap
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['ALLOWED_EXTENSIONS'] = set(['fasta'])
from app import views