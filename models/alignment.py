from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from dataStructures import Score
from dataStructures import LocalAlignment
from dataStructures import AlignmentData


app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('FLASK_SETTINGS', silent=True)