from app import app
import os
import zipfile
import copy
from app.models import *
from engine.adding_data.Add_Folder import *
from engine.adding_data.Add_Pkl import *
from engine.adding_data.Add_NTuple import *
from app import histos, collection
from app import coll_it_d as it_d
from app import coll_tt_d as tt_d
from engine.colors.Color_Mapping import *
from engine.detectors.CreateDetectors import *

def save_to_db(or_det, histos):
    for h in or_det:
        try:
            MappedPlot.objects.get(name=h).delete()
        except:
            pass
        data = {}
        if or_det[h]['dtype'] == 'TT':
            data = copy.deepcopy(or_det[h])
            for layer in or_det[h]:
                if layer not in ["dtype"]:
                    for side in or_det[h][layer]:
                        if side not in ["layer_info"]:
                            for sector in or_det[h][layer][side]:
                                if sector not in ["side_info"]:
                                    data[layer][side][sector]['Histograms']={}
                                    if h in or_det[h][layer][side][sector]['Histograms']:
                                        data[layer][side][sector]['Histograms'][h]=copy.deepcopy(or_det[h][layer][side][sector]['Histograms'][h])
        if or_det[h]['dtype'] == 'IT':
            data = copy.deepcopy(or_det[h])
            for station in or_det[h]:
                if station not in ["dtype"]:
                    for side in or_det[h][station]:
                        if side not in ["station_info"]:
                            for layer in or_det[h][station][side]:
                                if layer not in ["side_info"]:
                                    for sector in or_det[h][station][side][layer]:
                                        if sector not in ["layer_info"]:
                                            data[station][side][layer][sector]['Histograms']={}
                                            if h in or_det[h][station][side][layer][sector]['Histograms']:
                                                data[station][side][layer][sector]['Histograms'][h]=copy.deepcopy(or_det[h][station][side][layer][sector]['Histograms'][h])
        mp = MappedPlot(
            name = h,
            dtype = or_det[h]['dtype'],
            body = data,
            h_props = histos[or_det[h]['dtype'].lower()][h])
        try:
            mp.save()
            print h+"  saved to DB"
        except:
            print "Unable to save entry to DB"
    return

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def add_file(filename):
    global collection
    minihistos = {'it':{}, 'tt':{}}
    if filename.rsplit('.', 1)[1] == 'pkl':
        if "TT" in filename:
            pickle_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            hist_name = filename.rsplit('.', 1)[0]
            Add_Pkl(tt_d, pickle_file, hist_name,minihistos)
            collection = Normalize_Colours(tt_d, it_d)

        if "IT" in filename:
            pickle_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            hist_name = filename.rsplit('.', 1)[0]
            Add_Pkl(it_d, pickle_file, hist_name,minihistos)
            collection = Normalize_Colours(tt_d, it_d)

    if filename.rsplit('.', 1)[1] == 'root':
        Add_NTuple(os.path.join(app.config['UPLOAD_FOLDER'], filename), it_d, tt_d,minihistos)
        collection = Normalize_Colours(tt_d, it_d)
    if filename.rsplit('.', 1)[1] == 'zip':
        file_address = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        fh = open(file_address, 'rb')
        z = zipfile.ZipFile(fh)
        outpath = os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0])
        if not os.path.exists(outpath):
            os.system("mkdir "+outpath)
        for name in z.namelist():
            z.extract(name, outpath)
        Add_Folder(outpath, it_d, tt_d,minihistos)
        collection = Normalize_Colours(tt_d, it_d)
    for dt in minihistos:
        for h in minihistos[dt]:
            histos[dt][h]=minihistos[dt][h]
    print tt_d
    print it_d
    save_to_db(tt_d, histos)
    save_to_db(it_d, histos)
    return

def Update_histos():
    return True

def Update_tt(Drawing_mode):
    """
    This should create snapshot of detector with just one histogram and just one function
    """
    return create_TT()

def Update_it(Drawing_mode):
    return create_IT()