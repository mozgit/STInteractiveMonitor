from app import app
from flask import *
from json import dumps as json_dump
from engine.colors.Color_Mapping import *
from engine.detectors.CreateDetectors import *
from werkzeug import secure_filename
import pickle
import sys
import json
from app.models import *
#from app.auth import *
from app import histos, collection, coll_it_d, coll_tt_d, Drawing_mode
from app import db
from models import st_sector
import os
from Manage_DB.manage_db import find_existing_runs
from Manage_DB.manage_db import list_runs

# Load the list of unique sector names
f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/engine/NameList.pkl')
NameList = pickle.load(f)

#Need this
@app.route("/",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello():
    global histos

    if request.method == 'POST':
        """
        On post user defines:
        - Histogram to look at 
        - Color schema 
        - Run range
        """
        Drawing_mode = {'hist':'', 'prop':'', 'start_run':'', 'end_run':''}
        for m in ['hist', 'prop', 'start_run', 'end_run']:
            try:
                Drawing_mode[m]=request.form[m]
                if request.form[m] == "":
                    return redirect(url_for('hello'))
                if m in ['start_run', 'end_run']:
                    try:
                        a = int(request.form[m])
                    except:
                        return redirect(url_for('hello'))
            except:
                return redirect(url_for('hello'))
        """
        After drawing mode configured, shapshots need to be updated.
        snapshot_tt = Update_tt(Drawing_mode)
        snapshot_it = Update_it(Drawing_mode)
        collection = Normalize_Colours(snapshot_tt, snapshot_it)
        histos - list of histogrmas, no need in update
        """

        snapshot_tt = create_TT(Drawing_mode)
        snapshot_it = create_IT(Drawing_mode)
        collection = Normalize_Colours(snapshot_tt, snapshot_it)
        existing_runs = find_existing_runs(int(Drawing_mode['start_run']),int(Drawing_mode['end_run']))
        return render_template('index.html', tt = snapshot_tt, it=snapshot_it, dm = Drawing_mode, collections = collection, hist_coll = histos,  existing_runs = existing_runs, all_runs = list_runs())
    Drawing_mode = {'hist':'', 'prop':'', 'start_run':'', 'end_run':''}
    suppl_dm = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':5}
    existing_runs = find_existing_runs(int(suppl_dm['start_run']),int(suppl_dm['end_run']))
    collection = {}
    return render_template('index.html', dm = Drawing_mode, collections = collection, hist_coll = histos, tt = create_TT(suppl_dm), it = create_IT(suppl_dm), existing_runs = existing_runs, all_runs = list_runs())

#@app.route("/",methods = ('GET', 'POST'))
@app.route("/test",methods = ('GET', 'POST'))
#@app.route("/index",methods = ('GET', 'POST'))
def hello_lite():
    global histos
    return render_template('test.html', tt = create_TT_lite(), it = create_IT_lite())

@app.route('/rounding/<query1>____<query2>.json')
def round_json(query1,query2):
    interval =smart_interval(float(query1),float(query2),2)
    print [str(interval[0]),str(interval[1])]
    return Response(json_dump([str(interval[0]),str(interval[1])]), mimetype='application/json')

@app.route('/results/<query1>____<query2>.json')
def s_json(query1, query2):
    existing_runs=find_existing_runs(int(query1),int(query2))
    return Response(json_dump(get_info_lite(existing_runs)), mimetype='application/json')
    #return Response(json_dump({'p_names':p_names}), mimetype='application/json')

@app.route('/all_runs/<query>.json')
def ar_json(query):
    return Response(json_dump(list_runs()), mimetype='application/json')

@app.route('/existing_runs/<query1>____<query2>.json')
def er_json(query1, query2):
        return Response(json_dump(find_existing_runs(int(query1),int(query2))), mimetype='application/json')


@app.route("/<d>",methods = ('GET', 'POST'))
def Detector(d):
    if d in NameList['TTNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "TT", name = d, sec=p_name, det = coll_tt_d)
    if d in NameList['ITNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "IT", name = d, sec=p_name, det = coll_it_d)
    return redirect(url_for('hello'))
