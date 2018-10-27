from flask import render_template,request,flash
from app import app,db
from controllers import postController as pC
from controllers import lightsController as lC
from controllers import formsController as fC
from controllers import locationController as locC
from controllers import chromecastController as ccC
from controllers import songController as songC
from app.models import Satellite, Mobile,Song
import pychromecast
import json
import flask
from forms import forms as f
import time

@app.route("/", methods=['POST','GET'])
def main():
  form = f.ConnectForm()
  ccForm = f.ConnectCC()
  s = Satellite.query.all()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('info.html',sats=s, form=form, ccForm=ccForm)
    else:
      res = sC.connect(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      s = Satellite.query.all()
      return render_template('info.html',sats=s, form=form, ccForm=ccForm)
  else:
    return render_template('info.html',sats=s, form=form, ccForm=ccForm)

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

@app.route("/connectCC", methods=['POST'])
def connectCC():
  ccForm  = f.ConnectCC()
  s = Satellite.query.all()
  form = f.ConnectForm()

  if request.method == 'POST':
    if request.form.get('name') == "" or ccForm.room is None:
      flash('All fields are required')
      return render_template('info.html', sats=s, form=form, ccForm=ccForm)
    else:
      res = fC.connectCC(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return render_template('info.html',sats=s, form=form, ccForm=ccForm)
  else:
    return render_template('info.html',sats=s, form=form, ccForm=ccForm)
    
  
    


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
    lC.SetAmbientBrightness(json['value'])
    
    return("")

@app.route("/ttt")
def ttt():
  return str(ccC.IsPlaying("Bumboks"))

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
  macs = Mobile.query.all()
  dict_list = [row2dict(m) for m in macs]
  return flask.jsonify({"devices" : dict_list})

@app.route("/new")
def new():
  deviceForm = f.ConnectForm()
  songs = Song.query.all()
  return render_template('songs.html',form=deviceForm, songs=songs)

@app.route("/play/<int:songId>", methods=['GET'])
def play(songId):
    deviceForm = f.ConnectForm()
    songs = Song.query.all()
    ccC.StopCCs()
    roomIds = locC.GetCurrentRoomIds()
    songUrl = songC.GetSongUrl(songId)
    ccC.PlaySong(roomIds, songUrl)
    flash("Song is now playing")
    return render_template('songs.html',form=deviceForm, songs=songs)

@app.route("/music/pause", methods=['GET'])
def pause():
    deviceForm = f.ConnectForm()
    songs = Song.query.all()
    ccC.PauseCCs()
    flash("Song is now paused")
    return render_template('songs.html',form=deviceForm, songs=songs)


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
