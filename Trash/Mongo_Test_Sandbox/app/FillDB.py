from __init__ import db
from models import st_sector
from GetSTNameFromBin import *
import pickle
import datetime
import random
import ROOT as R
f = open('/Users/ilya/ST_Monitor/Mongo_Test_Sandbox/app/NameList.pkl')
NameList = pickle.load(f) 

#ss = st_snapshot(run = "1", body = {})
#ss.save()

#k = st_snapshot().create("2")
#k.save()

#st_snapshot(run = "3", body = {}).save()
        
random.seed(datetime.datetime.now().microsecond)

for i in range(0, 100):
    for name in NameList['TTNames']:
        st_sector(name = name, run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1)).save()
    for name in NameList['ITNames']:
        st_sector(name = name, run = i, efficiency = random.random(), bias = (random.random()-0.5), width = random.random()/(i+1)).save()


from mongoengine import *
client = connect('st_db')
for document in client.st_db.st_sector.find():
    print document

def FillDB(file_address="Moni_2012.root", run_number=17):
    file = R.TFile(file_address)
    #list_of_histograms = {"Histogram name":{"address":"Addres in Brunel file","type":"IT/TT", "WhatToLookAt":"efficiency/bias/width"}}
    list_of_histograms = {}
    #temp_snapshot = {"SectorName":{"efficiency": "bias": "width": }}
    temp_snapshot ={}
    for name in NameList['TTNames']:
        temp_snapshot[name]={"efficiency":-1, "bias":-1, "width":-1}
    for name in NameList['ITNames']:
        temp_snapshot[name]={"efficiency":-1, "bias":-1, "width":-1}

    for h in list_of_histograms.keys():
        hist_2D = file.Get(list_of_histograms[h]["address"]+h)
        nBins = hist_2D.GetNbinsX()
        for i in range(1, nBins):            
            if list_of_histograms[h]["type"] == "IT":
                if GetITNameFromBin(i-1) in NameList['ITNames']:
                    hist_1D = hist_2D.ProjectionY(GetITNameFromBin(i-1), i, i)
                    temp_snapshot[GetITNameFromBin(i-1)][list_of_histograms[h]["WhatToLookAt"]] = ExtractInfo(hist_1D, list_of_histograms[h]["WhatToLookAt"])
            elif list_of_histograms[h]["type"] == "TT":
                if GetTTNameFromBin(i-1) in NameList['TTNames']:
                    hist_1D = hist_2D.ProjectionY(GetTTNameFromBin(i-1), i, i)
                    temp_snapshot[GetTTNameFromBin(i-1)][list_of_histograms[h]["WhatToLookAt"]] = ExtractInfo(hist_1D, list_of_histograms[h]["WhatToLookAt"])
            else:
                continue
    for s in temp_snapshot:
        st_sector(name = s, run = run_number, efficiency = temp_snapshot[s]["efficiency"], bias = temp_snapshot[s]["bias"], width = temp_snapshot[s]["width"]).save()
    return


def ExtractInfo(hist, mode="efficiency"):
    if (mode == "width"):
        return hist.GetRMS()
    if (mode == "bias"):
        return hist.GetMean()
    if (mode == "efficiency"):
        return hist.GetMean()
    return -1
