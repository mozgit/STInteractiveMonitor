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
import datetime

#f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/engine/NameList.pkl')
#NameList = pickle.load(f)


def add_run(run_number, file, datetime = False, alignment_iteration = False):
    f_input = R.TFile(file)
    hist_all_TT_MonBIAS = f_input.Track.Get("STPerf_TTTrackMonitor/AllSectorsUnbiasedResidualHisto")
    hist_all_TT_MonRMS = f_input.Track.Get("STPerf_TTTrackMonitor/AllSectorsResidualHisto")
    hist_all_TT_Eff = f_input.Track.Get("STPerf_TTHitEfficiency/SummaryEfficiencyPlot")
    hist_all_TT_nExp = f_input.Track.Get("STPerf_TTHitEfficiency/SummaryNbExpectedPlot")
    hist_all_TT_nFound = f_input.Track.Get("STPerf_TTHitEfficiency/SummaryNbFoundPlot")
    hist_all_IT_MonBIAS = f_input.Track.Get("STPerf_ITTrackMonitor/AllSectorsUnbiasedResidualHisto")
    hist_all_IT_MonRMS = f_input.Track.Get("STPerf_ITTrackMonitor/AllSectorsResidualHisto")
    hist_all_IT_Eff = f_input.Track.Get("STPerf_ITHitEfficiency/SummaryEfficiencyPlot")
    hist_all_IT_nExp = f_input.Track.Get("STPerf_ITHitEfficiency/SummaryNbExpectedPlot")
    hist_all_IT_nFound = f_input.Track.Get("STPerf_ITHitEfficiency/SummaryNbFoundPlot")
    TT_Map = TT_Map_f()
    IT_Map = IT_Map_f()
    snapshot = []
    for st_id in TT_Map:
        histBIAS = hist_all_TT_MonBIAS.ProjectionY(TT_Map[st_id], st_id+1, st_id+1)
        histRMS = hist_all_TT_MonRMS.ProjectionY(TT_Map[st_id], st_id+1, st_id+1)
        mean = histBIAS.GetMean()        
        width = histRMS.GetRMS()
        n_eff = hist_all_TT_nFound.GetBinContent(st_id+1)
        n_res = histBIAS.GetEntries()
        f = hist_all_TT_nFound.GetBinContent(st_id+1)
        nf = hist_all_TT_nExp.GetBinContent(st_id+1) -hist_all_TT_nFound.GetBinContent(st_id+1)
        tot = hist_all_TT_nExp.GetBinContent(st_id+1)
        try:
            eff = float(f)/float(tot)
            err_eff = (float(f*nf)/float(tot)**3)**0.5
            #eff = float(f)
            #err_eff = eff**0.5
        except:
            eff = -1
            err_eff = 0
        print "Efficiency of "+TT_Map[st_id]+" ("+str(st_id)+") is "+str(eff)+" +/- "+str(err_eff)
        #sector = st_sector(name = TT_Map[st_id], run = run_number, efficiency = eff, bias = mean, width = width,
        #                                                  err_efficiency = err_eff, err_bias =width, err_width = hist.GetRMSError())
        #sector.save()
        st_sector.objects(name = TT_Map[st_id], run = run_number).update_one(set__run = run_number, set__efficiency = 100 * eff, set__bias = 1000 * mean, set__width = 1000 * width,
                                                          set__err_efficiency = 100 * err_eff, set__err_bias = 1000 * histBIAS.GetMeanError(), set__err_width = 1000 * histRMS.GetRMSError(), 
                                                          set__n_eff = n_eff, set__n_res = n_res, upsert = True)
        sector = st_sector.objects.get(name = TT_Map[st_id], run = run_number)
        snapshot.append(sector)
    for st_id in IT_Map:
        histBIAS = hist_all_IT_MonBIAS.ProjectionY(IT_Map[st_id], st_id+1, st_id+1)
        histRMS = hist_all_IT_MonRMS.ProjectionY(IT_Map[st_id], st_id+1, st_id+1)
        mean = histBIAS.GetMean()        
        width = histRMS.GetRMS()
        n_eff = hist_all_IT_nFound.GetBinContent(st_id+1)
        n_res = histBIAS.GetEntries()
        f = hist_all_IT_nFound.GetBinContent(st_id+1)
        nf = hist_all_IT_nExp.GetBinContent(st_id+1) -hist_all_IT_nFound.GetBinContent(st_id+1)
        tot = hist_all_IT_nExp.GetBinContent(st_id+1)
        try:
            eff = float(f)/float(tot)
            err_eff = (float(f*nf)/float(tot)**3)**0.5
            #eff = float(f)
            #err_eff = eff**0.5
        except:
            eff = -1
            err_eff = 0
        print "Efficiency of "+IT_Map[st_id]+" ("+str(st_id)+") is "+str(eff)+" +/- "+str(err_eff)
        #sector = st_sector(name = IT_Map[st_id], run = run_number, efficiency = eff, bias = mean, width = width,
        #                                                  err_efficiency = err_eff, err_bias =width, err_width = hist.GetRMSError())
        #sector.save()
        st_sector.objects(name = IT_Map[st_id], run = run_number).update_one(set__run = run_number, set__efficiency = 100 * eff, set__bias = 1000 * mean, set__width = 1000 * width,
                                                          set__err_efficiency = 100 * err_eff, set__err_bias = 1000 * histBIAS.GetMeanError(), set__err_width = 1000 * histRMS.GetRMSError(), 
                                                          set__n_eff = n_eff, set__n_res = n_res, upsert = True)
        sector = st_sector.objects.get(name = IT_Map[st_id], run = run_number)
        snapshot.append(sector)
    if (datetime and alignment_iteration):
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__datetime = datetime, set__alignment_iteration = alignment_iteration, upsert = True)
    elif (datetime and not alignment_iteration):
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__datetime = datetime, upsert = True)
    elif (not datetime and alignment_iteration):
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__alignment_iteration = alignment_iteration, upsert = True)
    else:
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, upsert = True)
    return True

def get_run_from_name(name):
    #AligWrk_Tracker-16687102-20151030T202059-EOR.root
    try:
        run = int(name.split("/")[-1].split('-')[1][:-2])
    except:
        run = -1
    return run

def get_alignment_iteration_from_name(name):
    #AligWrk_Tracker-16687102-20151030T202059-EOR.root
    try:
        it = int(name.split("/")[-1].split('-')[1][-2:])
    except:
        it = -1
    return it

def get_datetime_from_name(name):
    #AligWrk_Tracker-16687102-20151030T202059-EOR.root
    try:
        raw_date = name.split("/")[-1].split('-')[2].split("T")[0]
        raw_time = name.split("/")[-1].split('-')[2].split("T")[1]
        year = int(raw_date[:4])
        month = int(raw_date[4:6])
        day = int(raw_date[6:])
        hour = int(raw_time[:2])
        minute = int(raw_time[2:4])
        second = int(raw_time[4:])
        timestamp = datetime.datetime(year, month, day, hour, minute, second)
    except:
        timestamp =  datetime.datetime.now()
    return timestamp


if __name__ == "__main__":
    if len(sys.argv)==2:
        data = sys.argv[1]
        add_run(get_run_from_name(data), data, get_datetime_from_name(data), get_alignment_iteration_from_name(data))
    else:
        print "Indicate tuple to analyse"    
