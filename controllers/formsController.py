from app import db
from app.models import Satellite,CC,Mobile,Song,Room,Light
from flask import request

from forms import forms as f


def connectSat(request):
  name = request.form.get("name")
  ip = request.form.get("ip")
  port = request.form.get("port")
  s = Satellite.query.filter(Satellite.ip == ip).filter(Satellite.port == port)
  if not s.first(): #if no results found
    satellite = Satellite(ip=ip,port=port,name=name)
    db.session.add(satellite)
    db.session.commit()
    return True #added
  return False


def disconnectSat(id):
  try:
      sat = Satellite.query.get(id)
      db.session.delete(sat)
      db.session.commit()
      return True
  except:
      return False

def connectCC(request):
  name = request.form.get('name')
  roomId = request.form.get('room') 
  print(type(roomId))
  cc = CC.query.filter(CC.name == name).filter(CC.roomId == roomId)
  print(cc)
  if not cc.first():
    cc = CC(name=name, roomId=roomId)
    db.session.add(cc)
    db.session.commit()
    return True
  return False
  
def connectLight(request, name):
  print("name    ", name[0])
  
  lightId = request.form.get('name')
  roomId = request.form.get('room')
  print("light id    ", lightId, "   roomId ", roomId)
  existingLight = Light.query.filter(str(Light.uuid) == lightId)
  if not existingLight.first():
    light = Light(name=name[0], uuid = lightId, roomId=roomId)
    db.session.add(light)
    db.session.commit()
    return True
  return False

def connectMobile(request):
  name = request.form.get('name')
  mac = request.form.get('mac') 
  mobile = Mobile.query.filter(Mobile.name == name).filter(Mobile.mac == mac)
  if not mobile.first():
    m = Mobile(name=name, mac=mac)
    db.session.add(m)
    db.session.commit()
    return True
  return False
  

def connectSong(request):
  title = request.form.get('title')
  artist = request.form.get('artist') 
  link = request.form.get('link') 
  song = Song.query.filter(Song.title == title).filter(Song.artist == artist).filter(Song.link == link)
  if not song.first():
    s = Song(title=title, artist=artist, link=link)
    db.session.add(s)
    db.session.commit()
    return True
  return False
  
def connectRoom(request):
  name = request.form.get('name')
  room = Room.query.filter(Room.name == name)
  if not room.first():
    r = Room(name=name)
    db.session.add(r)
    db.session.commit()
    return True
  return False
