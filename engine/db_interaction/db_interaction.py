"""
This function quieres db
"""

import pickle
from mongoengine import *
from app.models import st_sector
from flask.ext.mongoengine import MongoEngine

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
    #print json.dumps(summary)
    return summary
