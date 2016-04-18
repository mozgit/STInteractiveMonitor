#!/bin/sh
#It is assumed, that these steps were done in advance:
#cd $HOME
#mkdir ST_Monitor
#cd ST_Monitor
#git clone https://github.com/mozgit/STInteractiveMonitor.git
#(How else you can call this script, right?)
#
cd $HOME
#Installation of pip
curl https://bootstrap.pypa.io/get-pip.py > $HOME/get-pip.py
python get-pip.py

#installation of virtualenv
sudo pip install virtualenv

#creating virtualenv 
virtualenv Env_For_STMonitor
source Env_For_STMonitor/bin/activate

#Installing required packages
pip install Flask==0.10.1
pip install Flask-Login==0.3.2
pip install flask-mongoengine==0.7.5
pip install Flask-Script==2.0.5
pip install Flask-WTF==0.12
pip install gevent==1.1.1
pip install greenlet==0.4.9
pip install itsdangerous==0.24
pip install Jinja2==2.8
pip install joblib==0.9.4
pip install MarkupSafe==0.23
pip install mongoengine==0.10.6
pip install pymongo==2.8
pip install setuptools 20==6.7
pip install uWSGI==2.0.12
pip install Werkzeug==0.11.5
pip install wheel==0.29.0
pip install WTForms==2.1

#Packages for root
sudo yum install git make gcc-c++ gcc binutils \
libX11-devel libXpm-devel libXft-devel libXext-devel

sudo yum install gcc-gfortran openssl-devel pcre-devel \
mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel mysql-devel \
fftw-devel cfitsio-devel graphviz-devel \
avahi-compat-libdns_sd-devel libldap-dev python-devel \
libxml2-devel gsl-static

#Installing root
git clone http://root.cern.ch/git/root.git
cd root
git tag -l
git checkout -b v5-34-32 v5-34-32
./configure --enable-soversion --all
make -j2
cd bin
source thisroot.sh
cd $HOME

#Installing NGINX
sudo yum install nginx

#Configure mongod:
sudo cp $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/mongod.conf /etc/

#Configure uWSGI
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/apps-available
sudo cp $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/uwsgi.ini /etc/uwsgi/apps-available/
sudo cp $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/uwsgi.service /usr/lib/systemd/system/

#Configure NGINX
sudo mkdir /etc/nginx/sites-enabled
sudo cp $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/nginx.conf /etc/nginx/
sudo cp $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/default /etc/nginx/sites-enabled

#Add update of the DB task to CRON
sudo cp $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/CheckAndUpdate.sh /etc/cron.hourly/

#Start application
source $HOME/ST_Monitor/STInteractiveMonitor/ServerSide/StartServer.sh
