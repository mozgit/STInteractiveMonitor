import os
from app.db import db
from app.models import st_sector
import pickle
from mongoengine import *

def find_existing_runs(minr, maxr):
    client = connect('st_db')
    existing_runs = []
    for i in range(minr, maxr+1):
        for d in client.st_db.st_sector.find({"run":i}).limit(1):
            existing_runs.append(i)
    return existing_runs

def list_runs():
    #Return a ilst of all known runs. 
    #May should be a better way to search for it...
    f = open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/Manage_DB/Known_runs.pkl')
    Known_runs = pickle.load(f)
    print Known_runs
    return Known_runs
