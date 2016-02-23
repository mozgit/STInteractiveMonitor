from app import app
from flask import render_template
from flask import abort, redirect, url_for, request, flash

# Here is some flask magic
@app.route("/",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello():
    return render_template('index.html')
