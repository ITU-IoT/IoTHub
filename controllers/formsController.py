from app import db
from app.models import Satellite,CC
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
  
