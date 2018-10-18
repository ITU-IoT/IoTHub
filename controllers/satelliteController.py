from app import db
from app.models import Satellite
from flask import request

from forms import forms as f


def connect(request):
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


def disconnect(id):
  try:
      sat = Satellite.query.get(id)
      db.session.delete(sat)
      db.session.commit()
      return True
  except:
      return False
