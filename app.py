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
    longitude = db.Column(db.Numeric(20,20), nullable=False)
    latitude = db.Column(db.Numeric(20,20), nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Earthquake(db.Model):
    __tablename__ = 'Earthquake'
    id = db.Column(db.Integer, primary_key=True)
    epicenter_longitude = db.Column(db.Numeric(20,20), nullable=False)
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
    time = db.Column(db.String(40), db.ForeignKey('Earthquake.time'), nullable=False)

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
             new_city.longitude = row[4]
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
             new_quake.epicenter_longitude = row[1]
             new_quake.time = row[2]
             new_quake.magnitude = row[3]
             new_quake.depth = row[4]
             db.session.add(new_quake)
             db.session.commit()
#             db.session.close()
             rs = Earthquake.query.get(line_count)
             print(rs.magnitude)
             line_count += 1
     print("Ending Quakes Loading")

def buildAffects():
    print("Yee")
    quakes = Earthquake.query.all()
    cities = City.query.all()
    for quake in quakes:
        for city in cities:
            print("Check it")
            print(quake.id)
            print(city.id)
            if(abs(quake.epicenter_latitude - city.latitude) < 1 and abs(quake.epicenter_longitude - city.longitude) < 1):
               new_affect = Affects()
               new_affect.state = city.state
               new_affect.name = city.name
               new_affect.eq_id = quake.id
               new_affect.time = quake.time
               db.session.add(new_affect)
               db.session.commit()
#               db.session.close()
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

def quake_json(eq_id):
    print("Start lookup")
    quake = Earthquake.query.get(eq_id)
#{"index": 1, "epicenter_longitude": 20, "epicenter_latitude": 20, "datetime": "10/7/21 10:50AM", "magnitude": 3
    data = {}
    print(quake.id)
    data['index'] = quake.id
    data['epicenter_latitude'] = int(quake.epicenter_latitude)
    data['epicenter_longitude'] = int(quake.epicenter_longitude)
    data['datetime'] = quake.time
    data['magnitude'] = int(quake.magnitude)
    data['depth'] = int(quake.depth)
    print(json.dumps(data))
    print("End lookup")
    return json.dumps(data)
    
def delete_by_id(eq_id):
    deleted_quake = Earthquake.query.get(eq_id)
    db.session.delete(deleted_quake)
    db.session.commit()

def update_quake(up_json):
    eq_id = up_json['index']
    quake = Earthquake.query.get(eq_id)
    quake.epicenter_latitude = up_json['epicenter_latitude']
    quake.epicenter_longitude = up_json['epicenter_longitude']
    quake.time = up_json['time']
    quake.magnitude = up_json['magnitude']
    quake.depth = up_json['depth']   
    db.session.commit()

@app.route('/impactsave', methods = ['POST'])
def create_impact_record():
    print("SStarting JSON exchange")
    jsdata = request.get_json()
#    jsdata = request.form['sendimpact']
#    parsed = json.loads(jsdata)
#    print(json.dumps(parsed, indent=4, sort_keys=True))
    print("Ending JSON exchange")
    print(jsdata['comments'])
    im_city = jsdata['city']
    im_state = jsdata['state']
    im_date = jsdata['date']
    im_rating = jsdata['rating']
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
    afs = Affects.query.all()
    for af in afs:
        if (af.time == im_date and af.name == im_city and af.state == im_state):
            new_cause = Causes()
            new_cause.eq_id = af.eq_id
            new_cause.time = af.time
            new_cause.rec_id = record.id
            db.session.add(new_cause)
            db.session.commit()

            new_origin = Originates()
            new_origin.name = af.name
            new_origin.state = af.state
            new_origin.rec_id = record.id
            db.session.add(new_origin)
            db.session.commit()


    rs = Impact_Record.query.get(1)
    com = rs.id
    print("Added to db: ")
    print(com)
    return "Success"


@app.route('/getrecents', methods = ['GET'], strict_slashes=False)
def get_recent_quakes():
    dret = '{"data": [' + quake_json(1) + ',' + quake_json(2) + ',' + quake_json(3) + ']}'
    print(dret)
    ret = '{"data": [{"index": 1, "epicenter_longitude": 20, "epicenter_latitude": 20, "datetime": "10/7/21 10:50AM", "magnitude": 3, "depth": 2.2}, {"index": 2, "epicenter_longitude": 20, "epicenter_latitude": 20, "datetime": "10/7/21 10:50AM", "magnitude": 3, "depth": 2.2}]}'
#    ret2 = '{index: 2, epicenter_longitude: 30, epicenter_latitude: 20, datetime: 10/7/21 10:50AM, magnitude: 3, depth: 2.2}'

    j = json.loads(dret)
#    jst = json.dumps(ret)
    return j

@app.route('/searchloc', methods = ['POST'])
def search_by_loc():
    jsdata = request.get_json() 
    goal_city = jsdata['city']
    goal_state = jsdata['state']
 
    print(goal_city)
    print(goal_state)
    afs = Affects.query.all()
    found_quakes = []
    for af in afs:
        if (af.name == goal_city and af.state == goal_state):
            found_quakes.append(quake_json(af.eq_id))
    quake_list = ",".join(found_quakes)
    dret = '{"data": ['  + quake_list + ']}'
    print(dret)
    return dret

@app.route('/searchdate', methods = ['POST'])
def search_by_date():
    jsdata = request.get_json() 
    goal_time = jsdata['datetime']
    print(goal_time)
    afs = Affects.query.all()
    goal_time = goal_time[5:7] + "/" + goal_time[8:10] + "/" + goal_time[2:4]
    print(goal_time)
    found_quakes = []
    for af in afs:
        print(af.time[0:8])
        if (af.time[0:8] == goal_time[0:8]):
            found_quakes.append(quake_json(af.eq_id))
    quake_list = ",".join(found_quakes)
    dret = '{"data": ['  + quake_list + ']}'
    print(dret)
    return dret

@app.route('/searchid', methods = ['POST'])
def search_by_id():
    jsdata = request.get_json() 
    print(json.dumps(jsdata))
    quake_id = jsdata['eq_id']
    print("heree")
    quake = Earthquake.query.get(1)    
    data = {}
    print(quake.id)
    data['index'] = quake.id
    data['epicenter_latitude'] = int(quake.epicenter_latitude)
    data['epicenter_longitude'] = int(quake.epicenter_longitude)
    data['datetime'] = quake.time
    data['magnitude'] = int(quake.magnitude)
    data['depth'] = int(quake.depth)
    data['city'] = "LA"
    data['state'] = "CA"
    data['pred_impact'] = "2.2"
    data['cur_impact'] = "3.3"
    com = "Good"
    coms = "Bad"
#    coms = '[' + ",".join(com1) + ']'
    data['comments'] = [com,coms]

    afs = Affects.query.all()

    for af in afs:
        if (af.eq_id == quake_id):
            data['location'] = af.name + ", " + af.state
    



    dret = {}
    dret['data'] = data

    print(json.dumps(dret))
    return dret

