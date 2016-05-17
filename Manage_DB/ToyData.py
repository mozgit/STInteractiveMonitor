import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import db
from app.models import st_sector, st_snapshot
import ROOT as R
import pickle
from mongoengine import *
import mongoengine
import datetime as dt
import random
from Create_Maps import IT_Map as IT_Map_f
from Create_Maps import TT_Map as TT_Map_f
from db_info import find_existing_runs
from db_info import list_runs
from manage_db import clear_db

def add_run_toy(run_number, file, datetime = False, alignment_iteration = False):
    random.seed(run_number)
    f_input = R.TFile(file)
    #hist_all_TT_Mon = f_input.Track.Get("STPerf_TTTrackMonitor/AllSectorsUnbiasedResidualHisto")
    #hist_all_TT_Eff = f_input.Track.Get("STPerf_TTHitEfficiency/SummaryEfficiencyPlot")
    #hist_all_TT_nExp = f_input.Track.Get("STPerf_TTHitEfficiency/SummaryNbExpectedPlot")
    #hist_all_TT_nFound = f_input.Track.Get("STPerf_TTHitEfficiency/SummaryNbFoundPlot")
    #hist_all_IT_Mon = f_input.Track.Get("STPerf_ITTrackMonitor/AllSectorsUnbiasedResidualHisto")
    #hist_all_IT_Eff = f_input.Track.Get("STPerf_ITHitEfficiency/SummaryEfficiencyPlot")
    #hist_all_IT_nExp = f_input.Track.Get("STPerf_ITHitEfficiency/SummaryNbExpectedPlot")
    #hist_all_IT_nFound = f_input.Track.Get("STPerf_ITHitEfficiency/SummaryNbFoundPlot")
    hist_all_TT_MonBIAS = f_input.Track.Get("TTTrackMonitor/AllSectorsUnbiasedResidualHisto")
    hist_all_TT_MonRMS = f_input.Track.Get("TTTrackMonitor/AllSectorsResidualHisto")
    hist_all_TT_Eff = f_input.Track.Get("TTHitEfficiency/SummaryEfficiencyPlot")
    hist_all_TT_nExp = f_input.Track.Get("TTHitEfficiency/SummaryNbExpectedPlot")
    hist_all_TT_nFound = f_input.Track.Get("TTHitEfficiency/SummaryNbFoundPlot")
    hist_all_IT_MonBIAS = f_input.Track.Get("ITTrackMonitor/AllSectorsUnbiasedResidualHisto")
    hist_all_IT_MonRMS = f_input.Track.Get("ITTrackMonitor/AllSectorsResidualHisto")
    hist_all_IT_Eff = f_input.Track.Get("ITHitEfficiency/SummaryEfficiencyPlot")
    hist_all_IT_nExp = f_input.Track.Get("ITHitEfficiency/SummaryNbExpectedPlot")
    hist_all_IT_nFound = f_input.Track.Get("ITHitEfficiency/SummaryNbFoundPlot")    
    TT_Map = TT_Map_f()
    IT_Map = IT_Map_f()
    snapshot = []
    for st_id in TT_Map:
        histBIAS = hist_all_TT_MonBIAS.ProjectionY(TT_Map[st_id], st_id+1, st_id+1)
        histRMS = hist_all_TT_MonRMS.ProjectionY(TT_Map[st_id], st_id+1, st_id+1)
        mean = histBIAS.GetMean()
        width = histRMS.GetRMS()
        n_eff = random.gauss(hist_all_TT_nFound.GetBinContent(st_id+1), hist_all_TT_nFound.GetBinContent(st_id+1)**0.5)
        n_res = random.gauss(histBIAS.GetEntries(), histBIAS.GetEntries()**0.5)        
        new_mean = random.gauss(mean,width)
        f = max(hist_all_TT_nFound.GetBinContent(st_id+1)+random.randint(-5,5),0)
        nf = max(hist_all_TT_nExp.GetBinContent(st_id+1) -hist_all_TT_nFound.GetBinContent(st_id+1)+random.randint(-5,5),0)

        #mean = hist.GetEntries()
        #width = (hist.GetEntries())**0.5
        #new_mean = mean
        #f = hist_all_TT_nFound.GetBinContent(st_id+1)
        #nf = hist_all_TT_nExp.GetBinContent(st_id+1) -hist_all_TT_nFound.GetBinContent(st_id+1)

        err_width = histRMS.GetRMSError()
        new_width = random.gauss(width,err_width)                
        tot = f+nf
        try:
            eff = float(f)/float(tot)
            err_eff = (float(f*nf)/float(tot)**3)**0.5
            #eff = float(f)
            #err_eff = eff**0.5
        except:
            eff = 0.001
            err_eff = 0
        print "Efficiency of "+TT_Map[st_id]+" ("+str(st_id)+") is "+str(eff)+" +/- "+str(err_eff)
        st_sector.objects(name = TT_Map[st_id], run = run_number).update_one(set__efficiency = 100 * eff, set__bias = 1000 * new_mean, set__width = 1000 * new_width,
                                                          set__err_efficiency = 100 * err_eff, set__err_bias =1000 * new_width, set__err_width = 1000 * random.gauss(histRMS.GetRMSError(),histRMS.GetRMSError()/10), 
                                                          set__n_eff = n_eff, set__n_res = n_res, upsert=True)
        sector = st_sector.objects.get(name = TT_Map[st_id], run = run_number)
        snapshot.append(sector)
    for st_id in IT_Map:
        histBIAS = hist_all_IT_MonBIAS.ProjectionY(IT_Map[st_id], st_id+1, st_id+1)
        histRMS = hist_all_IT_MonRMS.ProjectionY(IT_Map[st_id], st_id+1, st_id+1)
        mean = histBIAS.GetMean()
        width = histRMS.GetRMS()
        n_eff = random.gauss(hist_all_IT_nFound.GetBinContent(st_id+1), hist_all_IT_nFound.GetBinContent(st_id+1)**0.5)
        n_res = random.gauss(histBIAS.GetEntries(), histBIAS.GetEntries()**0.5)        
        new_mean = random.gauss(mean,width)
        f = max(hist_all_IT_nFound.GetBinContent(st_id+1)+random.randint(-5,5),0)
        nf = max(hist_all_IT_nExp.GetBinContent(st_id+1) -hist_all_IT_nFound.GetBinContent(st_id+1)+random.randint(-5,5),0)

        #mean = hist.GetEntries()
        #width = (hist.GetEntries())**0.5
        #new_mean = mean
        #f = hist_all_IT_nFound.GetBinContent(st_id+1)
        #nf = hist_all_IT_nExp.GetBinContent(st_id+1) -hist_all_IT_nFound.GetBinContent(st_id+1)

        err_width = histRMS.GetRMSError()
        new_width = random.gauss(width,err_width)                
        tot = f+nf
        try:
            eff = float(f)/float(tot)
            err_eff = (float(f*nf)/float(tot)**3)**0.5
            #eff = float(f)
            #err_eff = eff**0.5
        except:
            eff = 0.001
            err_eff = 0
        print "Efficiency of "+IT_Map[st_id]+" ("+str(st_id)+") is "+str(eff)+" +/- "+str(err_eff)
        st_sector.objects(name = IT_Map[st_id], run = run_number).update_one(set__efficiency = 100 * eff, set__bias = 1000 * new_mean, set__width = 1000 * new_width,
                                                          set__err_efficiency = 100 * err_eff, set__err_bias =1000 * new_width, set__err_width = 1000 * random.gauss(histRMS.GetRMSError(),histRMS.GetRMSError()/10), 
                                                          set__n_eff = n_eff, set__n_res = n_res, upsert=True)
        sector = st_sector.objects.get(name = IT_Map[st_id], run = run_number)
        snapshot.append(sector)
    if (datetime and alignment_iteration):
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__datetime = datetime, set__alignment_iteration = alignment_iteration, upsert = True)
    elif (datetime and not alignment_iteration):
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__datetime = datetime, set__alignment_iteration = 0, upsert = True)
    elif (not datetime and alignment_iteration):
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__datetime = dt.datetime.now(), set__alignment_iteration = alignment_iteration, upsert = True)
    else:
        st_snapshot.objects(run = run_number).update_one( set__snapshot = snapshot, set__datetime = dt.datetime.now(), set__alignment_iteration = 0,  upsert = True) 
    return True

if __name__ == "__main__":
    if len(sys.argv)==3:
        clear_db()
        data = sys.argv[1]
        nruns = int(sys.argv[2])
        #r0 = 166531
        r0 = 990531
        for i in range(0, nruns):
            random.seed(i) 
            r0+=random.randint(0, 5) 
            add_run_toy(r0, data)
    else:
        print "Indicate tuple to analyse and number of runs to simulate"    
