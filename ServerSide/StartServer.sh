#!/bin/sh
source $HOME/Env_For_STMonitor/bin/activate
source $HOME/root/root/bin/thisroot.sh
sudo service mongod start
sudo service uwsgi start
sudo service ngonx start
