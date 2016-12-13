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
class Gen(db.Model):
    __table_args__ = {'schema': 'alignments'}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    fasta = db.Column(db.String(), nullable=False)
    ncbi_id = db.Column(db.String(255), nullable=False)
    compared = db.Column(db.Boolean)
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, fasta, ncbi_id, compared, type):
        # self.id = id
        self.nombre = nombre
        self.fasta = fasta
        self.ncbi_id = ncbi_id
        self.compared = compared
        self.type = type

    def add(self, gen):
        db.session.add(gen)
        return self.session_commit()

    def update(self):
        return self.session_commit()

    def delete(self, gen):
        db.session.delete(gen)
        return self.session_commit()

    def session_commit(self):
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            reason = str(e)
            print reason
