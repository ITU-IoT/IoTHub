from flask import render_template,request,flash,redirect,url_for
from app import app,db
from controllers import postController as pC
from controllers import lightsController as lC
from controllers import formsController as fC
from controllers import locationController as locC
from controllers import chromecastController as ccC
from controllers import songController as songC
from app.models import Satellite, Mobile,Song, Room
import pychromecast
import json
import flask
from forms import forms as f
import time

# @app.route("/", methods=['POST','GET'])
# def notmain():
#   return "work ples"

@app.route("/", methods=['POST','GET'])
def main():
  form = f.ConnectSatellite()
  ccForm = f.ConnectCC()
  ccForm.room.choices = f.GetRooms()
  mobileForm = f.ConnectMobile()
  lightForm = f.ConnectLight()
  lightForm.room.choices = f.GetRooms()
  songForm = f.ConnectSong()
  roomForm = f.ConnectRoom()
  r = Room.query.all()
  return render_template('info.html',rooms=r, form=form, ccForm=ccForm, mobileForm=mobileForm, lightForm=lightForm, songForm=songForm,roomForm=roomForm)


@app.route("/<int:id>")
def disconnect(id):
  res = fC.disconnectSat(id)
  if res:
    flash("Succefully disconnected")
  else:
    flash("Something went wrong, trying updating site!")
  r = Room.query.all()
  form = f.ConnectForm()
  return render_template("info.html", rooms=r, form=form)


@app.route("/connectSat", methods=['POST'])
def connectSat():
  form = f.ConnectSatellite()
  formValidate = f.ConnectSatelliteValidate()

  if request.method == 'POST':
    if formValidate.validate() == False:
      flash('All fields are required')
      return redirect(url_for('main'))
    else:
      res = fC.connectSat(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return redirect(url_for('main'))
  else:
      return redirect(url_for('main'))

@app.route("/connectCC", methods=['POST'])
def connectCC():
  form = f.ConnectCC()
  formValidate = f.ConnectCCValidate() 
 
  if request.method == 'POST':
    if formValidate.validate() == False:
      flash('All fields are required')
      return redirect(url_for('main'))
    else:
      res = fC.connectLight(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return redirect(url_for('main'))
  else:
      return redirect(url_for('main'))

@app.route("/connectLight", methods=['POST'])
def connectLight():
  form = f.ConnectLight()
  formValidate = f.ConnectLightValidate() 
 
  if request.method == 'POST':
    if formValidate.validate() == False:
      flash('All fields are required')
      return redirect(url_for('main'))
    else:
      res = fC.connectLight(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return redirect(url_for('main'))
  else:
      return redirect(url_for('main'))

@app.route("/connectSong", methods=['POST'])
def connectSong():
  form = f.ConnectSong()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required')
      return redirect(url_for('main'))
    else:
      res = fC.connectSong(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return redirect(url_for('main'))
  else:
      return redirect(url_for('main'))
    
@app.route("/connectMobile", methods=['POST'])
def connectMobile():
  form = f.ConnectMobile()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required')
      return redirect(url_for('main'))
    else:
      res = fC.connectMobile(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return redirect(url_for('main'))
  else:
      return redirect(url_for('main'))
        
@app.route("/connectRoom", methods=['POST'])
def connectRoom():
  form = f.ConnectMobile()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required')
      return redirect(url_for('main'))
    else:
      res = fC.connectRoom(request)
      if res:
        flash("Success")
      else:
        flash("Fail")
      return redirect(url_for('main'))
  else:
      return redirect(url_for('main'))

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

@app.route("/music")
def music():
  form = f.ConnectSatellite()
  ccForm = f.ConnectCC()
  ccForm.room.choices = f.GetRooms()
  mobileForm = f.ConnectMobile()
  lightForm = f.ConnectLight()
  lightForm.room.choices = f.GetRooms()
  songForm = f.ConnectSong()
  roomForm = f.ConnectRoom()
  songs = Song.query.all()
  return render_template('songs.html',songs=songs, form=form, ccForm=ccForm, mobileForm=mobileForm, lightForm=lightForm, songForm=songForm,roomForm=roomForm)


@app.route("/music/play/<int:songId>", methods=['GET'])
def play(songId):
    songs = Song.query.all()
    ccC.StopCCs()
    roomIds = locC.GetCurrentRoomIds()
    songUrl = songC.GetSongUrl(songId)
    ccC.PlaySong(roomIds, songUrl)
    flash("Song is now playing")
    return redirect(url_for('music'))

@app.route("/music/stop", methods=['GET'])
def stop():
    songs = Song.query.all()
    ccC.StopCCs()
    flash("Song is now stopped")
    return redirect(url_for('main'))

@app.route("/music/volume/<int:roomId>/<int:volume>", methods=['PUT'])
def volume(roomId, volume):
    room = Room.query.filter(Room.id == roomId).first()
    room.volume = volume
    db.session.commit()
    ccC.SetVolume(roomId, volume)
    return ''

@app.route("/music/pause/<int:roomId>/<int:paused>", methods=['GET'])
def pause(roomId, paused):
    room = Room.query.filter(Room.id == roomId).first()
    room.paused = paused
    db.session.commit()
    ccC.SetPaused(roomId, paused)
    return redirect(url_for('main'))
    

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
