from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Table
# from flask.ext.script import Manager
# from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pcalderon:root@localhost:5432/postgres'
    # 'postgres://jtawbodqmjuxhw:Jy_s4DMd9jxqpRu1GkpQs1PVP0@ec2-54-235-92-236.compute-1.amazonaws.com:5432/d9noa5jj4opojt'
app.secret_key = 'root'
db = SQLAlchemy(app)


# Create the Post Class
class referenceType(db.Model):
    __table_args__ = {'schema': 'alignments'}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))

    def __init__(self, type):
        self.type = type
