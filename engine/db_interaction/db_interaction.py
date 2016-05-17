"""
This function quieres db
"""
#import os
#import sys
#sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pickle
from mongoengine import *
from app.models import st_sector, st_snapshot
from flask.ext.mongoengine import MongoEngine

def get_info_lite_sector_based(existing_runs):
    #Create dictionary:
    #{<sector_name>:{eff:[]
    #                err_eff:[]
    #                mean:[]
    #                err_mean:[]
    #                width:[]
    #                err_width:[]}
    #}
    print "from get_info_lite"
    print existing_runs
    client = connect('st_db')
    db = client.st_db
    #f = open('../../engine/NameList.pkl')
    f = open('../engine/NameList.pkl')
    variables = ['width', 'bias', 'efficiency']
    NameList = pickle.load(f) 
    summary = {}
    for det in NameList:
        #print det
        for s in NameList[det]:
            #print s
            summary[s]={'stats':{}}
            for v in variables:
                summary[s][v]=[]
                summary[s]["err_"+v]=[]
                summary[s]['stats'][v]={}
            for i in existing_runs:
                #print "running in runs: "+str(i)
                document = st_sector.objects.get(name =s, run = i)
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
    #print json.dumps(summary)
    return summary

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
    f = open('../engine/NameList.pkl')
    NameList = pickle.load(f) 
    variables = ['width', 'bias', 'efficiency']
    n_vars = ['n_eff', 'n_res']
    summary = {}
    for det in NameList:
        for s in NameList[det]:
            summary[s]={'stats':{}}
            for v in variables+n_vars:
                #print v
                summary[s][v]=[]
                summary[s]["err_"+v]=[]
                summary[s]['stats'][v]={}    
    for i in existing_runs:
        document=st_snapshot.objects.get(run=i)
        for sct in document['snapshot']:
            for v in variables:
                val = sct[v]
                err = sct['err_'+v]
                summary[sct.name][v].append(val)
                summary[sct.name]['err_'+v].append([val-err, val+err])
            for v in n_vars:
                val = abs(sct[v])
                err = abs(sct[v])**0.5
                summary[sct.name][v].append(val)
                summary[sct.name]['err_'+v].append([val-err, val+err])

    for det in NameList:
        for s in NameList[det]:
            for v in variables + n_vars:
                if len(summary[s][v])>0:
                    summary[s]['stats'][v]['mean']=float(sum(summary[s][v]))/float(len(summary[s][v]))
                    summary[s]['stats'][v]['min']=float(min(summary[s][v]))
                    summary[s]['stats'][v]['max']=float(max(summary[s][v]))
                else:
                    summary[s]['stats'][v]['mean']="empty"
                    summary[s]['stats'][v]['min']="empty"
                    summary[s]['stats'][v]['max']="empty"
    return summary

if __name__ == "__main__":
    from datetime import datetime
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.db import db
    from app.models import st_sector, st_snapshot

    print "Testing sector-based access:"
    start = datetime.now()
    get_info_lite(range(0, 100))
    end = datetime.now()
    print "Search took {}".format(end-start)
    print "\n"
    print "Testing snapshot-based access:"
    start = datetime.now()
    get_info_lite_test(range(0, 100))
    end = datetime.now()
    print "Search took {}".format(end-start)
