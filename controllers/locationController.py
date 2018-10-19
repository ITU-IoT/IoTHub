import math
from app.models import CurrentSignals, Mobile, Room, CC,Satellite
from app import db
from controllers import chromecastController as ccC
from sqlalchemy import func
from datetime import datetime

MUSIC_START_TIME = 0

def determineRoom():
  current_signals = db.session.query(CurrentSignals.roomId,func.max(CurrentSignals.rssi)).group_by(CurrentSignals.mobileId).all()
  roomIds = [s for s,x in current_signals]
  print(roomIds)
  ccC.ChangeRoom(roomIds)




def UpdateLocationData(json):
  devices = json['devices']
  satelliteName = json['name'] 

  satellite = db.session.query(Satellite.roomId).filter(Satellite.name == satelliteName).first()
  # print(satellite.roomId)

  #update db
  currentSignal = db.session.query(CurrentSignals,Mobile.name).join(Mobile,Mobile.id == CurrentSignals.mobileId).filter(CurrentSignals.roomId == satellite.roomId).all()
  # print(devices['name'])
  #already in db
  for d in devices:
    UpdateSignal = None

    for signal, name in currentSignal:
      if d['name'] == name:
        signal.rssi = d['rssi']
        signal.timestamp = datetime.now()
        UpdateSignal = signal
        db.session.commit()
        break

    #Create
    if UpdateSignal is None:
      mobile = Mobile.query.filter(Mobile.name == d['name']).first()
      s = CurrentSignals(mobileId=mobile.id,roomId=satellite.roomId,rssi=d['rssi'],timestamp=datetime.now())
      db.session.add(s)
      db.session.commit()
      break

  for signal, name in currentSignal:
    if not any(d for d in devices if d['name'] == name):
      db.session.delete(signal)
      db.session.commit()
      break

  
