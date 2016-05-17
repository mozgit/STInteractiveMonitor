from appl import app
from json import dumps as json_dump
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.roundings.roundings import smart_interval
from engine.detectors.CreateDetectors import create_IT_lite, create_TT_lite
from engine.db_interaction.db_interaction import get_info_lite
from Manage_DB.db_info import find_existing_runs
from Manage_DB.db_info import list_runs
from flask import render_template
from flask import Response
from mongoengine import *
from flask.ext.mongoengine import MongoEngine
# Load the list of unique sector names
#f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/engine/NameList.pkl')
#NameList = pickle.load(f)



@app.route("/",methods = ('GET', 'POST'))
@app.route("/test",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello_lite():
    #global histos
    return render_template('test.html', tt = create_TT_lite(), it = create_IT_lite())

@app.route('/rounding/<query1>____<query2>.json')
def round_json(query1,query2):    
    try: 
        interval =smart_interval(float(query1),float(query2),2)
        #print [str(interval[0]),str(interval[1])]
        return Response(json_dump([str(interval[0]),str(interval[1])]), mimetype='application/json')
    except:
        return False

@app.route('/results/<query1>____<query2>.json')
def s_json(query1, query2):
    try:
        existing_runs=find_existing_runs(int(query1),int(query2))
        print "collecting info_lite"
        info_lite = get_info_lite(existing_runs)
        print "info collected"
        return Response(json_dump(get_info_lite(existing_runs)), mimetype='application/json')
    except:
        return False
        #return Response(json_dump({'p_names':p_names}), mimetype='application/json')

@app.route('/all_runs/<query>.json')
def ar_json(query):
    #print json_dump(list_runs())
    try:
        return Response(json_dump(list_runs()), mimetype='application/json')
    except:
        return False

@app.route('/existing_runs/<query1>____<query2>.json')
def er_json(query1, query2):
    try:
        return Response(json_dump(find_existing_runs(int(query1),int(query2))), mimetype='application/json')
    except:
        return False


#@app.route("/<d>",methods = ('GET', 'POST'))
#def Detector(d):
#    if d in NameList['TTNames']: 
#        p_name = Parse_Name(d)
#        return render_template('Sector.html', dtype = "TT", name = d, sec=p_name, det = coll_tt_d)
#    if d in NameList['ITNames']: 
#        p_name = Parse_Name(d)
#        return render_template('Sector.html', dtype = "IT", name = d, sec=p_name, det = coll_it_d)
#    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.run(debug=True,
    host = '0.0.0.0')