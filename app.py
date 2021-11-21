from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)
db = SQLAlchemy(app)

migration = Migrate(app, db)
 
class City(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True)
    population = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(20), nullable=False)
    longitide = db.Column(db.Numeric(20,20), nullable=False)
    latitude = db.Column(db.Numeric(20,20), nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Earthquake(db.Model):
    __tablename__ = 'Earthquake'
    id = db.Column(db.Integer, primary_key=True)
    epicenter_longitide = db.Column(db.Numeric(20,20), nullable=False)
    epicenter_latitude = db.Column(db.Numeric(20,20), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    magnitude = db.Column(db.Numeric(20,20), nullable=False)
    depth = db.Column(db.Numeric(20,20), nullable=False)

class Impact_Record(db.Model):
    __tablename__ = 'Impact_Record'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(120), nullable=False)

class Causes(db.Model):
    __tablename__ = 'Causes'
    id = db.Column(db.Integer, primary_key=True)
    eq_id = db.Column(db.Integer, db.ForeignKey('Earthquake.id'), nullable=False)
    time = db.Column(db.DateTime, db.ForeignKey('Earthquake.time'), nullable=False)
    rec_id = db.Column(db.Integer, db.ForeignKey('Impact_Record.id'), nullable=False)

class Affects(db.Model):
    __tablename__ = 'Affects'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), db.ForeignKey('City.state'), nullable=False)
    name = db.Column(db.String(120), db.ForeignKey('City.name'),  nullable=False)
    eq_id = db.Column(db.Integer, db.ForeignKey('Earthquake.id'), nullable=False)
    time = db.Column(db.DateTime, db.ForeignKey('Earthquake.time'), nullable=False)

class Originates(db.Model):
    __tablename__ = 'Originates'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), db.ForeignKey('City.state'), nullable=False)
    name = db.Column(db.String(120), db.ForeignKey('City.name'),  nullable=False)
    rec_id = db.Column(db.Integer, db.ForeignKey('Impact_Record.id'), nullable=False)

db.create_all()
db.session.commit()

@app.route('/')
 
def index():
#    return "Hello, welcome to the coolest zone!"
    return render_template('mainpage.html')

def create_impact_record():
    record = Impact_Record()
    record.rating = 10
    record.comments = "Very bad do not do"

    try:
        print("Heyoy")
        db.session.add(record)
        db.session.commit()
        # on successful db insert, flash success
#        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        print("Leyoy")
        db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    #flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
    finally:
        db.session.close()

    rs = Impact_Record.query.get(1)
    com = rs.comments
    return com