from mongoengine import *
from app import db
from app.models import st_sector

def doallthethings(name, Drawing_Mode):
    print "DOING JOB FOR "+name
    #Drawing_mode = {'hist':'', 'prop':'', 'start_run':'', 'end_run':''}
    hist = Drawing_Mode['hist']
    start_run = Drawing_Mode['start_run']
    end_run = Drawing_Mode['end_run']
    for document in db.st_sector.find():
        print document
    return {'Name':name, 'Histograms':{}, 'is_masked':False}

