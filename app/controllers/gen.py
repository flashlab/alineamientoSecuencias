from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError
# from flask.ext.script import Manager
# from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/ResistanceGen'
app.secret_key = 'root'
db = SQLAlchemy(app)


# Create the Post Class
class Gen(db.Model):
    __table_args__ = {'schema': 'PatternResistance'}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    fasta = db.Column(db.String(), nullable=False)
    ncbi_id = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre, fasta, ncbi_id):
        # self.id = id
        self.nombre = nombre
        self.fasta = fasta
        self.ncbi_id = ncbi_id

    def add(self, gen):
        db.session.add(gen)
        return self.session_commit()

    def update(self):
        return self.session_commit()

    def delete(self, gen):
        db.session.delete(gen)
        return self.session_commit()

    def all(self):
        db.
    def session_commit(self):
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            reason = str(e)
            print reason
