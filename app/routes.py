import json
import time

import flask
import pychromecast
from flask import flash, redirect, render_template, request, url_for

from app import app, db
from app.models import Mobile, Room, Satellite, Song, Light
from controllers import chromecastController as ccC
from controllers import formsController as fC
from controllers import lightsController as lC
from controllers import locationController as locC
from controllers import postController as pC
from controllers import songController as songC
from forms import forms as f

# @app.route("/", methods=['POST','GET'])
# def notmain():
#   return "work ples"


@app.route("/", methods=['POST', 'GET', 'PUT'])
def main():
    form = f.ConnectSatellite()
    ccForm = f.ConnectCC()
    ccForm.room.choices = f.GetRooms()
    mobileForm = f.ConnectMobile()
    lightForm = f.ConnectLight()
    lightForm.room.choices = f.GetRooms()
    lightForm.name.choices = f.GetLights()
    songForm = f.ConnectSong()
    roomForm = f.ConnectRoom()
    r = Room.query.all()
    lights = Light.query.all()
    songs = Song.query.all()
    return render_template(
        'info.html',
        rooms=r,
        Lights = lights,
        form=form,
        songs=songs,
        ccForm=ccForm,
        mobileForm=mobileForm,
        lightForm=lightForm,
        songForm=songForm,
        roomForm=roomForm)


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


@app.route("/lights/<int:number>", methods=['PUT'])
def updateLight(number):
    lC.UpdateLight(number, request.data)


@app.route("/lights/toggle/<int:number>", methods=['GET'])
def toogleLight(number):
    lC.ToggleLights(number)
    return redirect(url_for('main'))


@app.route("/sensor/light", methods=['POST'])
def light():
    json = request.json

    if 'value' not in json:
        return "failure, missing value"

    print("Received light sensor value: ")
    print(json['value'])
    lC.SetAmbientBrightness(json['value'])

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
    macs = Mobile.query.all()
    dict_list = [row2dict(m) for m in macs]
    return flask.jsonify({"devices": dict_list})


@app.route("/music/play/<int:songId>", methods=['GET'])
def play(songId):
    songs = Song.query.all()
    ccC.StopCCs()
    roomIds = locC.GetCurrentRoomIds()
    songUrl = songC.GetSongUrl(songId)
    ccC.PlaySong(roomIds, songUrl)
    flash("Song is now playing")
    return redirect(url_for('main'))


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

@app.route("/light/color/<int:lightId>/<string:color>", methods=['PUT','GET'])
def coloring(lightId, color):
    if request.method == 'GET':
        return redirect(url_for('main'))
    elif request.method == 'PUT':
        print(color)
        light = db.session.query(Light).filter(Light.uuid == lightId).first()
        light.hex = color
        db.session.commit()
        print(color)
        xy = lC.ConvertHexToXY(color)
        lC.ChangeColor(lightId, xy)
        return redirect(url_for('main'))

def connectPOST(request):
    if not request.json:
        return "wrong"
    # print(request.json)
    # return json.dumps(request.json)
    return pC.decode(request)


def connectGET(request):
    return request.method


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
