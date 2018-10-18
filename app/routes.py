from flask import render_template,request,flash
from app import app,db
from controllers import postController as pC
from controllers import lightsController as lC
from controllers import satelliteController as sC
from controllers import locationController as locC
from app.models import Satellite, Mobile
import pychromecast
import json
from forms import forms as f

CHROMECASTS = pychromecast.get_chromecasts() #Takes time to load!
print("Done loading CCs")
CC_NAME = "TT"

@app.route("/sensor/beacon", methods=['POST'])
def beacon():
    json = request.json

    if 'devices' not in json:
        return "failure, missing devices"
    if 'id' not in json:
        return "failure, missing id"
      
    print("Received beacon sensor value from "+json['id']+": ")
    print(json['devices'])
    locC.determineRoom(json['id'], json['devices'])
    return ""


@app.route("/sensor/beacon/device", methods=['GET'])
def getMac():
  macs = Mobile.query.all()

  

  return json.JSONEncoder().encode({"devices" : macs})

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

@app.route("/music/play", methods=['POST'])
def play():
    if not ccReady():
        return "Chromecast not found"

    mc, _ = getMediaController()
    
    json = request.json
    
    if 'url' not in json or not json['url'].endswith(".mp3"):
        return "You must provide url to an mp3 file"

    time = 0
    if 'time' in json:
        time = json['time']

    # current time must be set to be able to seek music later
    mc.play_media(json['url'], 'audio/mp3', current_time = time)
    
    return "success"

@app.route("/music/update", methods=['POST'])
def update():
    if not ccReady():
        return "Chromecast not found"

    mc, cast = getMediaController()

    json = request.json

    if 'time' in json:
        mc.seek(json['time'])

    if 'volume' in json:
        cast.set_volume(json['volume'])

    return "success"

@app.route("/music/pause", methods=['POST'])
def pause():
    if not ccReady():
        return ("Chromecast not found")

    mc, _ = getMediaController()

    mc.pause()

    return "success"

@app.route("/h")
def h():
  locC.determineRoom()
  return ""   

@app.route("/sensor/light", methods=['POST'])
def light():
    json = request.json

    if 'value' not in json:
        return "failure, missing value"

    print("Received light sensor value: ")
    print(json['value'])
    
    return ""

def connectPOST(request):
    if not request.json:
        return "wrong"
    #print(request.json)
    #return json.dumps(request.json)
    return pC.decode(request)
def connectGET(request):
    return request.method

def ccReady():
    if len(CHROMECASTS) == 0:
        return False
    casts = [cc for cc in CHROMECASTS if cc.device.friendly_name == CC_NAME]
    if len(casts) == 0:
        return False
    return True

def getMediaController():
    cast = next(cc for cc in CHROMECASTS if cc.device.friendly_name == CC_NAME)
    cast.wait()
    return cast.media_controller, cast


 
