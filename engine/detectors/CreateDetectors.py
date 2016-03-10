import pickle
from engine.module_based_naming.TTModules import *
from TT_info import *
from IT_info import *
from joblib import Parallel, delayed
from mongoengine import *
from app.models import st_sector
from flask.ext.mongoengine import MongoEngine
from app import app
from app import dbs as db
from multiprocessing import Pool
import matplotlib.pyplot as plt
import json
from Manage_DB.manage_db import find_existing_runs

def doallthethings(name, Drawing_Mode, db):
    #print "DOING JOB FOR "+name
    #Drawing_mode = {'hist':'', 'prop':'', 'start_run':'', 'end_run':''}
    hist = Drawing_Mode['hist']
    existing_runs = find_existing_runs(int(Drawing_Mode['start_run']),int(Drawing_Mode['end_run']))
    start_run = Drawing_Mode['start_run']
    end_run = Drawing_Mode['end_run']
    trend = {}
    err_trend = {}
    comb_trend = {}
    for i in existing_runs:
        for document in db.st_sector.find({"name":name, "run":i}).limit(1):
            trend[document['run']] = document[Drawing_Mode['hist']]
            comb_trend[document['run']] = [document[Drawing_Mode['hist']],document["err_"+Drawing_Mode['hist']]]
            err_trend[document['run']] = [document[Drawing_Mode['hist']]-document["err_"+Drawing_Mode['hist']],document[Drawing_Mode['hist']]+document["err_"+Drawing_Mode['hist']]]
        #print str(document['run'])+": "+str(document[Drawing_Mode['hist']])
    if Drawing_Mode['prop'] == 'mean':
        if float(len(trend.values()))!=0:
            found_value = float(sum(trend.values()))/float(len(trend.values()))
        else:
            found_value = 0
    elif Drawing_Mode['prop'] == 'min':
        if float(len(trend.values()))!=0:
            found_value = min(trend.values())
        else:
            found_value = 0
    elif Drawing_Mode['prop'] == 'max':
        if float(len(trend.values()))!=0:
            found_value = max(trend.values())
        else:
            found_value = 0
    else:
        found_value = 0
    #plt.plot([1,2,3,4])

    #plt.bar(range(start_run,end_run), trend.values())
    #plt.savefig("app/static/plots/"+name+".png")   

    #for document in db.st_sector.find():
        #print document
    #print "output from 'doallthethings' "
    #print trend.keys()
    path_to_the_plot = "plots/"+name+".png"
    return {'Name':name, 'Histograms':{Drawing_Mode['hist']:{
                                       "plot":path_to_the_plot,
                                       "properties":{Drawing_Mode['prop']:found_value},
                                       "init_properties":{Drawing_Mode['prop']:found_value},
                                       "hist_as_dict":{'runs':comb_trend.keys(),'values':trend.values(),'errors':err_trend.values()}
                                       }}, 'is_masked':False}

def mf_wrap(args):
    return doallthethings(*args)

def create_TT(Drawing_Mode):
    #Drawing_Mode = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':3}
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f) 
    #Needed to be fixed for higher number of cores in flask
    client = connect('st_db')
    db = client.st_db
    #fl = [(name, Drawing_Mode, db) for name in  NameList['TTNames']]
    #_pool = Pool(processes =4 )
    #sector_collection = {f[0]:_pool.apply_async(mf_wrap, f) for f in fl}
    #sector_collection = {k: v.get(timeout=60) for k, v in sector_collection.items()}
    values = Parallel(n_jobs=1, backend="threading")(delayed(doallthethings)(name, Drawing_Mode, db) for name in NameList['TTNames'])
    sector_collection = dict(zip(NameList['TTNames'], values))
    TT = {'dtype':'TT'}
    layer = ['TTaU','TTaX','TTbV','TTbX']
    side = ['RegionA','RegionB','RegionC']
    for l in layer:
        TT[l]={'layer_info':TT_layer_info(l)}
        for si in side:
            TT[l][si]={'side_info': TT_side_info(l,si)}
            for s in TT_reg_len(l,si):
                #ADD histo fill from st_snaphots DB here!
                #Info = {'Name':l+si+'Sector'+str(s), 'div_info':TT_div_info(l,si,s),'Histograms':{}, 'is_masked':False}
                #if a+r+'Sector'+str(s) in NameList['TTNames']:
                TT[l][si][str(s)] = sector_collection[l+si+'Sector'+str(s)]
                TT[l][si][str(s)]['div_info'] = TT_div_info(l,si,s)
                    #print a+r+'Sector'+str(s)
    return TT


def create_IT(Drawing_Mode):
    #Drawing_Mode = {'hist':'efficiency', 'prop':'mean', 'start_run':0, 'end_run':3}
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f) 
    client = connect('st_db')
    db = client.st_db
    values = Parallel(n_jobs=1, backend="threading")(delayed(doallthethings)(name, Drawing_Mode, db) for name in NameList['ITNames'])
    sector_collection = dict(zip(NameList['ITNames'], values))
    #print json.dumps(sector_collection,sort_keys=True, indent=4)
    IT = {'dtype':'IT'}
    station = ['IT1','IT2','IT3']
    side = ['ASide','CSide','Bottom','Top']
    layer = ['X1','X2','U','V']
    for st in station:
        IT[st]={'station_info':IT_station_info(st)}
        for s in side:
            IT[st][s]= {'side_info':IT_side_info(st,s)}
            for l in layer:
                IT[st][s][l]={'layer_info':IT_layer_info(st,s,l)}
                for n in range(1,8):
                    IT[st][s][l][str(n)] = sector_collection[st+s+l+'Sector'+str(n)]
                    IT[st][s][l][str(n)]['div_info'] = IT_div_info(st,s,l,n)
    #values = Parallel(n_jobs=1, backend="threading")(delayed(doallthethings)(name, Drawing_Mode, db) for name in NameList['ITNames'])
    #sector_collection = dict(zip(NameList['ITNames'], values))
    #IT = {'dtype':'IT'}
    #station = ['IT1','IT2','IT3']
    #side = ['ASide','CSide','Bottom','Top']
    #layer = ['X1','X2','U','V']
    #for st in station:
        #IT[st]={'station_info':IT_station_info(st)}
        #for s in side:
            #IT[st][s]= {'side_info':IT_side_info(st,s)}
            #for l in layer:
                #IT[st][s][l]={'layer_info':IT_layer_info(st,s,l)}
                #for n in range(1,8):
                    #IT[st][s][l][str(n)] = sector_collection[st+s+l+'Sector'+str(n)]
                    #IT[st][s][l][str(n)]['div_info'] = IT_div_info(st,s,l,n)
    return IT


def get_info_lite(existing_runs):
    #Create dictionary:
    #{<sector_name>:{eff:[]
    #                err_eff:[]
    #                mean:[]
    #                err_mean:[]
    #                width:[]
    #                err_width:[]}
    #}
    client = connect('st_db')
    db = client.st_db
    f = open('engine/NameList.pkl')
    variables = ['width', 'bias', 'efficiency']
    NameList = pickle.load(f) 
    summary = {}
    for det in NameList:
        print det
        for s in NameList[det]:
            print s
            summary[s]={'stats':{}}
            for v in variables:
                summary[s][v]=[]
                summary[s]["err_"+v]=[]
                summary[s]['stats'][v]={}
            for i in existing_runs:
                for document in db.st_sector.find({"name":s, "run":i}).limit(1):
                    for v in variables:
                        val = document[v]
                        err = document['err_'+v]
                        summary[s][v].append(val)
                        summary[s]['err_'+v].append([val-err, val+err])
            for v in variables:
                if len(summary[s][v])>0:
                    summary[s]['stats'][v]['mean']=float(sum(summary[s][v]))/float(len(summary[s][v]))
                    summary[s]['stats'][v]['min']=float(min(summary[s][v]))
                    summary[s]['stats'][v]['max']=float(max(summary[s][v]))
                else:
                    summary[s]['stats'][v]['mean']="empty"
                    summary[s]['stats'][v]['min']="empty"
                    summary[s]['stats'][v]['max']="empty"
    print json.dumps(summary)
    return summary


def create_TT_lite():
    TT = {'dtype':'TT'}
    layer = ['TTaU','TTaX','TTbV','TTbX']
    side = ['RegionA','RegionB','RegionC']
    for l in layer:
        TT[l]={'layer_info':TT_layer_info(l)}
        for si in side:
            TT[l][si]={'side_info': TT_side_info(l,si)}
            for s in TT_reg_len(l,si):
                TT[l][si][str(s)] =  {'Name':l+si+'Sector'+str(s)}
                TT[l][si][str(s)]['div_info'] = TT_div_info(l,si,s)
                    #print a+r+'Sector'+str(s)
    return TT


def create_IT_lite():
    IT = {'dtype':'IT'}
    station = ['IT1','IT2','IT3']
    side = ['ASide','CSide','Bottom','Top']
    layer = ['X1','X2','U','V']
    for st in station:
        IT[st]={'station_info':IT_station_info(st)}
        for s in side:
            IT[st][s]= {'side_info':IT_side_info(st,s)}
            for l in layer:
                IT[st][s][l]={'layer_info':IT_layer_info(st,s,l)}
                for n in range(1,8):
                    IT[st][s][l][str(n)] = {'Name':st+s+l+'Sector'+str(n)}
                    IT[st][s][l][str(n)]['div_info'] = IT_div_info(st,s,l,n)
    return IT

