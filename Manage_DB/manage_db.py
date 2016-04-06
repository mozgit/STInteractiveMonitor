import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import db
from app.models import st_sector, st_snapshot
import ROOT as R
import pickle
from mongoengine import *
import datetime
import random
from Create_Maps import IT_Map as IT_Map_f
from Create_Maps import TT_Map as TT_Map_f
from db_info import find_existing_runs
from db_info import list_runs

f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/engine/NameList.pkl')
NameList = pickle.load(f)


def fill_random(nNentries=10):
    random.seed(datetime.datetime.now().microsecond)
    
    #client = connect('st_db')
    #dbs = client.st_db
    for i in range(0, nNentries):
        snapshot = []
        for name in NameList['TTNames']:
            sector=st_sector(name = name, run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1),
                                            err_efficiency = random.random()/10, err_bias = (random.random()-0.5)/10, err_width = 0)
            sector.save()
            snapshot.append(sector)

        for name in NameList['ITNames']:
            sector = st_sector(name = name, run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1),
                                            err_efficiency = random.random()/10, err_bias = (random.random()-0.5)/10, err_width = 0)
            sector.save()
            snapshot.append(sector)
        st_snapshot(run = i, snapshot = snapshot).save()
        try:
            f = open('Known_runs.pkl')
            Known_runs = pickle.load(f)
        except:
            Known_runs= []
        if i not in Known_runs:
            Known_runs.append(i)
        with open('Known_runs.pkl', 'wb') as basket:
            pickle.dump(sorted(Known_runs), basket)
    return True

def print_content():
    client = connect('st_db')
    for document in st_sector.objects():
        print document.printsector()
    #for document in st_snapshot.objects():
    #    print document.snapshot

    return True

def clear_db():
    client = connect('st_db')
    st_sector.drop_collection()
    st_snapshot.drop_collection()
    #print "ST_sectors removed, snapshots:"
    #for document in st_sector.objects():
    #    document.delete()
    #client.st_db.st_snapshot.drop()
    #print "ST_snapshots removed, snapshots:"
    #for document in st_snapshot.objects():
    #    document.delete()
    #    print document
    #for document in client.st_db.st_sector.find():
    #   document.remove()
    return True    

def add_run(run_number, file):
    f_input = R.TFile(file)
    hist_all_TT_Mon = f_input.Track.Get("TTTrackMonitor/BySector/AllSectorsUnbiasedResidualHisto")
    hist_all_TT_Eff = f_input.Track.Get("TTHitEfficiency/SummaryEfficiencyPlot")
    hist_all_IT_Mon = f_input.Track.Get("ITTrackMonitor/BySector/AllSectorsUnbiasedResidualHisto")
    hist_all_IT_Eff = f_input.Track.Get("ITHitEfficiency/SummaryEfficiencyPlot")    

    c = R.TCanvas("c","c",600,600)
    hist_all_TT_Eff.Draw("COLZ")
    c.SaveAs("Test.pdf")

    TT_Map = TT_Map_f()
    IT_Map = IT_Map_f()
    snapshot = []
    for st_id in TT_Map:
        hist = hist_all_TT_Mon.ProjectionY(TT_Map[st_id], st_id+1, st_id+1)
        random.seed(datetime.datetime.now().microsecond)
        print "Efficiency of "+TT_Map[st_id]+" ("+str(st_id)+") is "+str(hist_all_TT_Eff.GetBinContent(st_id+1))
        sector = st_sector(name = TT_Map[st_id], run = run_number, efficiency = hist_all_TT_Eff.GetBinContent(st_id+1), bias = hist.GetMean(), width = hist.GetRMS(),
                                                          err_efficiency = hist_all_TT_Eff.GetBinError(st_id+1), err_bias = hist.GetRMS(), err_width = 0)
        sector.save()
        snapshot.append(sector)
    for st_id in IT_Map:
        hist = hist_all_IT_Mon.ProjectionY(IT_Map[st_id], st_id+1, st_id+1)
        random.seed(datetime.datetime.now().microsecond)
        sector = st_sector(name = IT_Map[st_id], run = run_number, efficiency = hist_all_IT_Eff.GetBinContent(st_id+1), bias = hist.GetMean(), width = hist.GetRMS(),
                                                          err_efficiency = hist_all_IT_Eff.GetBinError(st_id+1), err_bias = hist.GetRMS(), err_width = 0)
        sector.save()
        snapshot.append(sector)
    st_snapshot(run = i, snapshot = snapshot).save()

    try:
        f = open('Known_runs.pkl')
        Known_runs = pickle.load(f)
    except:
        Known_runs= []
    Known_runs.append(run_number)

    with open('Known_runs.pkl', 'wb') as basket:
        pickle.dump(Known_runs, basket)

    #t_ITHitMonitor = tree_ITHitMonitor.Get("TrackMonTuple")
    return True

if __name__ == "__main__":
    #client = connect('st_db')
    #dbs = client.st_db
    #fill_random(10)
    #print "Befre clenaing"
    #print_content()
    #print "Cleaning"
    clear_db()
    #print "After cleaning"
    #print_content()
    #add_run(1, "/Users/ilya/TempData/1.root")
    #add_run(2, "/Users/ilya/TempData/2.root")    
    #add_run(3, "/Users/ilya/TempData/3.root")
    #add_run(200, "/Users/ilya/TempData/Brunel-1000ev-histos.root")
    fill_random(100)
    #print find_existing_runs(0, 6)