from app import app
from ROOT import *
from flask import render_template
from flask import abort, redirect, url_for, request, flash
from engine.colors.Color_Mapping import *
from app.supplimentaryfunctions import *
from werkzeug import secure_filename
import pickle
import sys
import json
from app.models import *
#from app.auth import requires_auth
from app.auth import *
#from app import it_d as g_it_d
#from app import tt_d as g_tt_d
from app import histos, collection, coll_it_d, coll_tt_d, Drawing_mode
from app import db
from models import st_sector

# Avoid spawning canvases
gROOT.SetBatch(kTRUE)

# Make stylish plots
gROOT.ProcessLine(".x engine/histo_drawing/lhcbStyle.C")

# Load the list of unique sector names

f = open('engine/NameList.pkl')
NameList = pickle.load(f)

#Don't need this
@app.route("/configure",methods = ('GET', 'POST'))
def configure():
    global histos
    global coll_tt_d
    global coll_it_d
    global collection
    if request.method == 'POST':
        if request.form['btn'] == 'Edit histograms list':
            existing_plots_IT = []
            existing_plots_TT = []
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    existing_plots_TT.append(mp.__unicode__())
                if mp.dtype == 'IT':
                    existing_plots_IT.append(mp.__unicode__())
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos))
        if request.form['btn'] == 'Configure':
            for mp in MappedPlot.objects.all():
                mp.remove_from_detector()
                if mp.__unicode__() in request.form:
                    if request.form[mp.__unicode__()] == 'on':
                        if not mp.is_loaded():
                            mp.add_to_detector()
            collection = Normalize_Colours(coll_tt_d, coll_it_d)
            return redirect(url_for('hello'))
    existing_plots_IT = []
    existing_plots_TT = []
    for mp in MappedPlot.objects.all():
        if mp.dtype == 'TT':
            existing_plots_TT.append(mp.__unicode__())
        if mp.dtype == 'IT':
            existing_plots_IT.append(mp.__unicode__())
    return render_template('Configure.html', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos)





#Don't need this
@app.route("/edit",methods = ('GET', 'POST'))
@requires_auth
def edit():
    global histos
    global coll_tt_d
    global coll_it_d
    global collection
    global Drawing_mode
    if request.method == 'POST':
        if request.form['btn'] == 'Upload':
            files = request.files.getlist("file[]")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_address = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_address)
                    add_file(filename)
                    os.system("rm "+file_address)
            existing_plots_IT = []
            existing_plots_TT = []
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    existing_plots_TT.append(mp.__unicode__())
                if mp.dtype == 'IT':
                    existing_plots_IT.append(mp.__unicode__())
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos, dm = Drawing_mode))
        if request.form['btn'] == 'Remove':
            for mp in MappedPlot.objects.all():
                mp.remove_from_detector()
                if mp.__unicode__() in request.form:
                    MappedPlot.objects.get(name=mp.__unicode__()).delete()
            existing_plots_IT = []
            existing_plots_TT = []
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    existing_plots_TT.append(mp.__unicode__())
                if mp.dtype == 'IT':
                    existing_plots_IT.append(mp.__unicode__())
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos, dm = Drawing_mode))
        """
        for m in ['start_run', 'end_run']:
            try:
                Drawing_mode[m]=request.form[m]
            except:
                pass
            files = request.files.getlist("file[]")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_address = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_address)
            add_file(filename)
            os.system("rm "+file_address)
            existing_plots_IT = []
            existing_plots_TT = []
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    existing_plots_TT.append(mp.__unicode__())
                if mp.dtype == 'IT':
                    existing_plots_IT.append(mp.__unicode__())
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos, dm = Drawing_mode))
        """
    existing_plots_IT = []
    existing_plots_TT = []
    for mp in MappedPlot.objects.all():
        if mp.dtype == 'TT':
            existing_plots_TT.append(mp.__unicode__())
        if mp.dtype == 'IT':
            existing_plots_IT.append(mp.__unicode__())
    return render_template('Edit.html', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos, dm = Drawing_mode)




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
    g_tt_d = create_TT()
    g_it_d = create_IT()

    if request.method == 'POST':
        """
        On post user defines:
        - Histogram to look at 
        - Color schema 
        - Run range
        """
        Drawing_Mode = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':3}
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
        #Drawing_Mode = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':3}
        snapshot_tt = create_TT(Drawing_mode)
        snapshot_it = create_IT(Drawing_mode)
        collection = Normalize_Colours(snapshot_tt, snapshot_it)
        return render_template('index.html', tt = snapshot_tt, it=snapshot_it, dm = Drawing_mode, collections = collection, hist_coll = histos)
    #collection = Normalize_Colours(coll_tt_d, coll_it_d)
    Drawing_Mode = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':3}
    return render_template('index.html', dm = Drawing_mode, collections = collection, hist_coll = histos, tt = g_tt_d, it = g_it_d)



@app.route("/<d>",methods = ('GET', 'POST'))
def Detector(d):
    if d in NameList['TTNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "TT", name = d, sec=p_name, det = coll_tt_d)
    if d in NameList['ITNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "IT", name = d, sec=p_name, det = coll_it_d)
    return redirect(url_for('hello'))
