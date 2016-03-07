from app import app
from flask import render_template
from flask import abort, redirect, url_for, request, flash
from engine.colors.Color_Mapping import *
from engine.detectors.CreateDetectors import *
from werkzeug import secure_filename
import pickle
import sys
import json
from app.models import *
from app.auth import *
from app import histos, collection, coll_it_d, coll_tt_d, Drawing_mode
from app import db
from models import st_sector
import os
from Manage_DB.manage_db import find_existing_runs


# Load the list of unique sector names
f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/engine/NameList.pkl')
NameList = pickle.load(f)

#Need this
@app.route("/",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello():
    global Drawing_mode
    global coll_tt_d
    global coll_it_d
    global g_tt_d
    global g_it_d
    global collection
    global histos

    if request.method == 'POST':
        """
        On post user defines:
        - Histogram to look at 
        - Color schema 
        - Run range
        """
        for m in ['hist', 'prop', 'start_run', 'end_run']:
            try:
                Drawing_mode[m]=request.form[m]
            except:
                pass
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
        return render_template('index.html', tt = snapshot_tt, it=snapshot_it, dm = Drawing_mode, collections = collection, hist_coll = histos,  existing_runs = existing_runs)
    suppl_dm = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':5}
    existing_runs = find_existing_runs(int(suppl_dm['start_run']),int(suppl_dm['end_run']))
    return render_template('index.html', dm = Drawing_mode, collections = collection, hist_coll = histos, tt = create_TT(suppl_dm), it = create_IT(suppl_dm), existing_runs = existing_runs)



@app.route("/<d>",methods = ('GET', 'POST'))
def Detector(d):
    if d in NameList['TTNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "TT", name = d, sec=p_name, det = coll_tt_d)
    if d in NameList['ITNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "IT", name = d, sec=p_name, det = coll_it_d)
    return redirect(url_for('hello'))
