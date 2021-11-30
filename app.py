from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import json
import csv

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
#    time = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(40), nullable=False)
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

def loadCities():
    print("Starting Cities Load")
    with open('cities.txt') as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     for row in csv_reader:
         if line_count == 0:
             line_count += 1
         else:
             print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}')
             new_city = City()
             new_city.name = row[0]
             new_city.population = row[1]
             new_city.state = row[2]
             new_city.latitude = row[3]
             new_city.longitide = row[4]
             db.session.add(new_city)
             db.session.commit()
             db.session.close()
             rs = City.query.get(line_count)
             print(rs.latitude)
             line_count += 1
     print(line_count)
     print("Ending Cities Loading")

def loadQuakes():
    print("Starting Quakes Load")
    with open('quakes.txt') as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     for row in csv_reader:
         if line_count == 0:
             line_count += 1
         else:
             print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}')
             new_quake = Earthquake()
             new_quake.epicenter_latitude = row[0]
             new_quake.epicenter_longitide = row[1]
             new_quake.time = row[2]
             new_quake.magnitude = row[3]
             new_quake.depth = row[4]
             db.session.add(new_quake)
             db.session.commit()
             db.session.close()
             rs = Earthquake.query.get(line_count)
             print(rs.magnitude)
             line_count += 1
     print("Ending Quakes Loading")

def buildAffects():
    print("Yee")
    quakes = City.query.all()
    for quake in quakes:
        print(quake.id)
    print("Yuh")

@app.before_first_request
def do_something_only_once():
    print("Yes")
    loadCities()
    loadQuakes()
    buildAffects()

@app.route('/')

def index():

    print("Accessed HTML")
    return render_template('mainpage.html')

@app.route('/impactsave', methods = ['POST'])
def create_impact_record():
    print("SStarting JSON exchange")
    jsdata = request.get_json()
#    jsdata = request.form['sendimpact']
#    parsed = json.loads(jsdata)
#    print(json.dumps(parsed, indent=4, sort_keys=True))
    print("Ending JSON exchange")
    print(jsdata['comments'])
    record = Impact_Record()
    record.rating = 5
    record.comments = jsdata['comments']

    try:
        db.session.add(record)
        db.session.commit()
        # on successful db insert, flash success
#        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    #flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
    finally:
        db.session.close()

    rs = Impact_Record.query.get(1)
    com = rs.id
    print("Added to db: ")
    print(com)
    return "Success"
