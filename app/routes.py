from flask import render_template,request,flash
from app import app,db
from controllers import postController as pC
from controllers import lightsController as lC
from controllers import satelliteController as sC
from controllers import locationController as locC
from controllers import chromecastController as ccC
from app.models import Satellite, Mobile,Song
import pychromecast
import json
import flask
from forms import forms as f
import time

@app.route("/", methods=['POST','GET'])
def main():
  form = f.ConnectForm()
  s = Satellite.query.all()


  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('info.html',sats=s, form=form)
    else:
      res = sC.connect(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      s = Satellite.query.all()
      return render_template('info.html',sats=s, form=form)
  else:
    return render_template('info.html',sats=s, form=form)

@app.route("/<int:id>")
def disconnect(id):
  res = sC.disconnect(id)
  if res:
    flash("Succefully disconnected")
  else:
    flash("Something went wrong, trying updating site!")
  s = Satellite.query.all()
  form = f.ConnectForm()
  return render_template("info.html", sats=s, form=form)
  

@app.route("/home")
def home():
  return render_template("front.html")

@app.route("/lights/<int:number>", methods=['PUT'])
def updateLight(number):
    lC.UpdateLight(number, request.data)


@app.route("/h")
def h():
  ccC.PlaySong([1],"http://iot.alssys.dk/sample.mp3")  
  return ""   

@app.route("/sensor/light", methods=['POST'])
def light():
    json = request.json

    if 'value' not in json:
        return "failure, missing value"

    print("Received light sensor value: ")
    print(json['value'])
    
    return("")

@app.route("/sensor/beacon", methods=['POST'])
def beacon():
    json = request.json

    if 'devices' not in json:
        return "failure, missing devices"
    if 'name' not in json:
        return "failure, missing id"
      
    # print("Received beacon sensor value from "+json['id']+": ")
    # print(json['devices'])
    locC.UpdateLocationData(json)
    locC.determineRoom()
    return ""


@app.route("/sensor/beacon/device", methods=['GET'])
def getMac():
  print("getting devices")
  macs = Mobile.query.all()
  print("creating list of devices")
  dict_list = [row2dict(m) for m in macs]
  print("returning devices")
  return flask.jsonify({"devices" : dict_list})

@app.route("/new")
def new():
  form = f.ConnectForm()
  songs = Song.query.all()
  return render_template('songs.html',form=form, songs=songs)


def connectPOST(request):
    if not request.json:
        return "wrong"
    #print(request.json)
    #return json.dumps(request.json)
    return pC.decode(request)
def connectGET(request):
    return request.method


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
