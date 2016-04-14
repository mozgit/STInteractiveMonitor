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
from db_info import list_runs, get_latest_date, get_latest_run
from AddOneFill import add_run, get_run_from_name, get_alignment_iteration_from_name, get_datetime_from_name
from ToyData import add_run_toy
import datetime
import glob

if __name__ == "__main__":
    kwargs = dict(x.split('=', 1) for x in sys.argv[1:])    
    if not 'year' in kwargs:
        year = str(datetime.datetime.now().year)
    else:
        year = str(kwargs['year'])

    test_data = "Brunel-50000ev-histos.root"
    path = "/hist/Savesets/"+year+"/LHCbA/AligWrk_Tracker/"#10/20/
    #files = sorted(glob.iglob('/Users/ilya/*/*.root'), key=os.path.getctime, reverse=True)
    #for i in files:
    #    print i
    files = sorted(glob.iglob(path+"*/*/*.root"), key=os.path.getctime, reverse=True)
    latest_run = get_latest_run()
    latest_alignment_iteration = st_snapshot.objects.get(run = latest_run).alignment_iteration
    latest_date = get_latest_date()
    latest_timestamp = str(latest_date.year).zfill(4)+str(latest_date.month).zfill(2)+str(latest_date.day).zfill(2)+"T"+str(latest_date.hour).zfill(2)+str(latest_date.minute).zfill(2)+str(latest_date.second).zfill(2)
    #print latest_timestamp
    need_to_add = []
    for f in files:
        fdate = get_datetime_from_name(f)
        if fdate > latest_date:
            need_to_add.append(f)
        #else:
        #    break
    for name in reversed(need_to_add):
        add_run_toy(get_run_from_name(name), test_data, get_datetime_from_name(name), get_alignment_iteration_from_name(name))
        #add_run(get_run_from_name(name), name, get_datetime_from_name(name), get_alignment_iteration_from_name(name))