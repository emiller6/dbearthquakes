from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy.sql import text
import json
import csv

app = Flask(__name__)
moment = Moment(app)
db = SQLAlchemy(app)
conn = db.session
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
    time = db.Column(db.String(40), db.ForeignKey('Earthquake.time'), nullable=False)
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

def delete_quake(eq_id):
    print("Starting Delet")
    quake_id = eq_id
    deleted_quake = Earthquake.query.get(eq_id)
    db.session.delete(deleted_quake)
    db.session.commit()
    afs = Affects.query.all()
    for af in afs:
        if (af.eq_id == quake_id):
            db.session.delete(af)
            db.session.commit()
    cs = Causes.query.all()
    for c in cs:
        if (c.eq_id == quake_id):
            db.session.delete(c)
            db.session.commit()
    print("Ending Delete")
    return "Success"

def update_quake(up_json):
    eq_id = up_json['eq_id']
    quake = Earthquake.query.get(eq_id)
#    quake.epicenter_latitude = up_json['epicenter_latitude']
#    quake.epicenter_longitude = up_json['epicenter_longitude']
    quake.time = up_json['datetime']
    quake.magnitude = up_json['mag']
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
    im_comments = jsdata['comments']
    record = Impact_Record()
    record.rating = im_rating
    record.comments = im_comments

    try:
        db.session.add(record)
        db.session.commit()
        # on successful db insert, flash success
#        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    #flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
#    finally:
#        db.session.close()

    record_id = 0
    irs = Impact_Record.query.all()
    for ir in irs:
        print("Check:")
        print(ir.rating)
        print(im_rating)
        print(ir.comments + " " + im_comments)
        print(int(ir.rating) == int(im_rating))
        print(ir.comments == im_comments)
        if(int(ir.rating) == int(im_rating) and ir.comments == im_comments):
            record_id = ir.id
    print(record_id)

    afs = Affects.query.all()
    for af in afs:
        print(af.time[0:8] + " " + im_date)
        print(af.name + " " + im_city)
        print(af.state + " " + im_state)
        print(af.time[0:8] == im_date)
        print(af.name == im_city)
        print(af.state == im_state)
        if (af.time[0:8] == im_date and af.name == im_city and af.state == im_state and record_id != 0):
            print("Mathing Game")
            new_cause = Causes()
            new_cause.eq_id = af.eq_id
            new_cause.time = af.time
            new_cause.rec_id = record_id
            db.session.add(new_cause)
            db.session.commit()

            new_origin = Originates()
            new_origin.name = af.name
            new_origin.state = af.state
            new_origin.rec_id = record_id
            db.session.add(new_origin)
            db.session.commit()


    rs = Impact_Record.query.get(1)
    com = rs.id
    print("Added to db: ")
    print(com)
    return "Success"


@app.route('/getrecents', methods = ['GET'], strict_slashes=False)
def get_recent_quakes():
#    dret = '{"data": [' + quake_json(1) + ',' + quake_json(2) + ',' + quake_json(3) + ']}'
    afs = Affects.query.all()
    found_quakes = []
    for af in afs:
        found_quakes.append(quake_json(af.eq_id))
    quake_list = ",".join(found_quakes)
    dret = '{"data": ['  + quake_list + ']}'
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
#maybe use a conn.execute('SELECT eq_id FROM City, Affects WHERE City.name == Affects.name AND City.name == :ci AND City.state == Affects.state AND City.state == :st', {"ci": goal_city, "st": goal_state})
#then use quake_json with eq_ids to pull quakes?

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

def calc_pred_impact_db(eq_id):
    eq_id = str(eq_id)
    avg_impacts_by_quake = text("CREATE VIEW avg_impacts AS "
                                    "SELECT eq_id, AVG(rating) AS Rate "
                                    "FROM Impact_Record, Causes "
                                    "WHERE rec_id == Impact_Record.id "
                                    "GROUP BY Causes.eq_id ")
    conn.execute(avg_impacts_by_quake)
    sim_cities = text("CREATE VIEW similar_cities AS "
                                    "SELECT magnitude, depth, rate "
                                    "FROM City, Affects, Earthquake, avg_impacts "
                                    "WHERE population < (SELECT population  "
                                                            "FROM City, Affects "
                                                            "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == "+eq_id+") + 1000 "
                                        "AND population > (SELECT population  "
                                                                "FROM City, Affects "
                                                                "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == "+eq_id+") - 1000 "
                                        "AND latitude < (SELECT latitude  "
                                                            "FROM City, Affects "
                                                            "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == "+eq_id+") + 20 "
                                        "AND latitude > (SELECT latitude  "
                                                                "FROM City, Affects "
                                                                "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == "+eq_id+") - 20 "
                                        "AND City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == Earthquake.id AND avg_impacts.eq_id == Affects.eq_id ")
    conn.execute(sim_cities)
    prev_quakes = text("CREATE VIEW prev_quakes AS "
                                    "SELECT magnitude, depth, rate "
                                    "FROM City, Affects, Earthquake, avg_impacts "
                                    "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == Earthquake.id AND avg_impacts.eq_id == Affects.eq_id AND City.name = (SELECT City.name  "
                                                                                                                                                                                        "FROM City, Affects "
                                                                                                                                                                                        "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == "+eq_id+") AND City.state = (SELECT City.state  "
                                                                                                                                                                                                                                                                                                        "FROM City, Affects "
                                                                                                                                                                                                                                                                                                        "WHERE City.name == Affects.name AND City.state == Affects.state AND Affects.eq_id == "+eq_id+") ")
    conn.execute(prev_quakes)
    prev_comp = text("CREATE VIEW prev_comparison AS "
                                    "SELECT prev_quakes.magnitude AS mag, prev_quakes.depth AS dep, Earthquake.magnitude AS difmag, Earthquake.depth AS difdep, prev_quakes.rate AS rate "
                                    "FROM prev_quakes, Earthquake "
                                    "WHERE Earthquake.id = "+eq_id+" ")
    conn.execute(prev_comp)
    sim_comp = text("CREATE VIEW sim_comparison AS "
                                    "SELECT similar_cities.magnitude AS mag, similar_cities.depth AS dep, Earthquake.magnitude AS difmag, Earthquake.depth AS difdep, similar_cities.rate AS rate "
                                    "FROM similar_cities, Earthquake "
                                    "WHERE Earthquake.id = "+eq_id+" ")
    conn.execute(sim_comp)
    math_1 = text("UPDATE prev_comparison "
                    "SET difdep = abs(dep - difdep) ")
    conn.execute(math_1)
    math_2 = text("UPDATE prev_comparison "
                    "SET difmag = -1*(2*abs(mag - difmag) + 1*difdep)+3 ")
    conn.execute(math_2)
    math_3 = text("UPDATE prev_comparison "
                    "SET rate = rate*difmag ")
    conn.execute(math_3)
    math_1 = text("UPDATE sim_comparison "
                    "SET difdep = abs(dep - difdep) ")
    conn.execute(math_1)
    math_2 = text("UPDATE sim_comparison "
                    "SET difmag = -1*(2*abs(mag - difmag) + 1*difdep)+3 ")
    conn.execute(math_2)
    math_3 = text("UPDATE sim_comparison "
                    "SET rate = rate*difmag ")
    conn.execute(math_3)
    p1 = text("SELECT SUM(rate) "
                "FROM sim_comparison")
    sim_num = conn.execute(p1).fetchall()
    p2 = text("SELECT SUM(difmag) "
                "FROM sim_comparison")
    sim_den = conn.execute(p2).fetchall()
    p3 = text("SELECT SUM(rate) "
                "FROM prev_comparison")
    prev_num = conn.execute(p3).fetchall()
    p4 = text("SELECT SUM(difmag) "
                "FROM prev_comparison")
    prev_den = conn.execute(p4).fetchall()
    db.session.commit()
    return (sim_num/sim_den)*0.25 + 0.75*(prev_num/prev_den)

def calc_pred_impact(eq_id):
    quake = Earthquake.query.get(eq_id)

    #Make an array of the average impact for each earthquake
    avg_imps = []
    qs = Earthquake.query.all()
    for q in qs:
        count = 0.0
        sum = 0.0
        cs = Causes.query.all()
        for c in cs:
            if(q.id == c.eq_id):
                imp_rec = Impact_Record.query.get(c.rec_id)
                count = count + 1
                sum = sum + imp_rec.rating
        if(count > 0.0):
            avg_imps.append(sum/count)
        else:
            avg_imps.append(0.0)

    #finds my_city, which is the location of the earthquake of interest
    find_my_city_affects = Affects.query.all()
    my_city_name = ""
    for a in find_my_city_affects:
        if(a.eq_id == eq_id):
            my_city_name = a.name + a.state

    my_city = Affects.query.get(1)
    find_my_city = City.query.all()
    for c in find_my_city:
        if(c.name + c.state == my_city_name):
            my_city = c


    similar_quakes = []
    similar_cities = []
    city_check = City.query.all()
    for c in city_check:
        right_size = abs(c.population - my_city.population) < 100000
        right_place_lat = abs(c.latitude - my_city.latitude) < 20
        right_place_lon = abs(c.longitude - my_city.longitude) < 20
        if(right_size and right_place_lat and right_place_lon):
            similar_cities.append(c.name + c.state)

    sim_city_quake_check = Affects.query.all()
    for af in sim_city_quake_check:
        if(similar_cities.count(af.name + af.state) > 0):
            sim_quake = Earthquake.query.get(af.eq_id)
            sim_quake_index_num = int(eq_id)
            similar_quakes.append([sim_quake.magnitude, sim_quake.depth, avg_imps[sim_quake_index_num-1]])


    # similar_quakes is an array of arrays that contains (in order) the mag, depth, and avg rating

    return 3

@app.route('/searchid', methods = ['POST'])
def search_by_id():
    jsdata = request.get_json()
    print(json.dumps(jsdata))
    quake_id = jsdata['eq_id']
    print("heree")
    quake = Earthquake.query.get(quake_id)
    data = {}
#could we do conn.execute('SELECT Affects.eq_id, Earthquake.epicenter_latitude, Earthquake.epicenter_longitude, Earthquake.time, Earthquake.magnitude, Earthquake.depth, Affects.name, Affects.state FROM Earthquake, Affects WHERE Earthquake.id == Affects.eq_id AND Earthquake.id == :id', {"id": eq_id})
#then for current impact do conn.execute('SELECT Earthquake.id, SUM(Impact_Record.rating) FROM Earthquake, Impact_Record, Causes WHERE Earthquake.id == Causes.eq_id AND Causes.rec_id == Impact_Record.id AND Earthquake.id == :quake GROUP BY Earthquake.id', {"quake": eq_id})
#could do similar for comments but without sum
    print(quake.id)
    data['index'] = quake.id
    data['epicenter_latitude'] = int(quake.epicenter_latitude)
    data['epicenter_longitude'] = int(quake.epicenter_longitude)
    data['datetime'] = quake.time
    data['magnitude'] = int(quake.magnitude)
    data['depth'] = int(quake.depth)
    data['city'] = "LA"
    data['state'] = "CA"
    data['pred_impact'] = calc_pred_impact_db(quake_id)
    data['cur_impact'] = calc_pred_impact(quake_id)
    com = "Good"
    coms = "Bad"
#    coms = '[' + ",".join(com1) + ']'
    data['comments'] = [com,coms]

    afs = Affects.query.all()

    for af in afs:
        if (af.eq_id == quake.id):
            data['city'] = af.name
            data['state'] = af.state

    all_com = []
    count = 0
    total_imp = 0
    cs = Causes.query.all()
    for c in cs:
        if (c.eq_id == quake.id):
            count = count + 1
            total_imp = total_imp + Impact_Record.query.get(c.rec_id).rating
            all_com.append(Impact_Record.query.get(c.rec_id).comments)
    if(count != 0):
        data['cur_impact'] = total_imp/count
        data['comments'] = all_com

    dret = {}
    dret['data'] = data

    print(json.dumps(dret))
    return dret

@app.route('/deleteid', methods = ['POST'])
def delete_by_id():
    jsdata = request.get_json()
    print(json.dumps(jsdata))
    quake_id = jsdata['eq_id']
    delete_quake(quake_id)
    return "Success"


@app.route('/updateid', methods = ['POST'])
def update_by_id():
    jsdata = request.get_json()
    print(json.dumps(jsdata))
#    quake_id = jsdata['eq_id']
    update_quake(jsdata)
    return "Success"
