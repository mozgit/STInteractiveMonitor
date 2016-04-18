import os
from app.db import db
from app.models import st_sector, st_snapshot
import pickle
from mongoengine import *

def find_existing_runs(minr, maxr):
    client = connect('st_db')
    existing_runs = []
    for i in range(minr, maxr+1):
        if st_snapshot.objects(run = i).first():
            existing_runs.append(i)
    return existing_runs

def list_runs():
    Known_runs = []
    for i in st_snapshot.objects.only('run'):
        if int(i.run) not in Known_runs:
            Known_runs.append(int(i.run))
    return sorted(Known_runs)

def get_latest_date():
    #Return date of latest saved histogram file
    try:
        run = list_runs()[-1]
        return st_snapshot.objects.get(run = run).datetime
    except:
        return False

def get_latest_run():
    #Return latest saved run
    try:
        return list_runs()[-1]
    except:
        return False
