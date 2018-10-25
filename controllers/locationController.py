import math
from app.models import CurrentSignals, Mobile, Room, CC,Satellite
from app import db
from controllers import chromecastController as ccC
from sqlalchemy import func
from datetime import datetime
import json

MUSIC_START_TIME = 0

def determineRoom():
  current_signals = db.session.query(CurrentSignals.roomId,func.max(CurrentSignals.rssi)).group_by(CurrentSignals.mobileId).all()
  roomIds = [s for s,x in current_signals]
  ccC.ChangeRoom(roomIds)




def UpdateLocationData(json):
  devices = json['devices']
  satelliteName = json['name'] 
  
  satellite = db.session.query(Satellite.roomId).filter(Satellite.name == satelliteName).first()

  #update db
  currentSignal = db.session.query(CurrentSignals,Mobile.name).join(Mobile,Mobile.id == CurrentSignals.mobileId).filter(CurrentSignals.roomId == satellite.roomId).all()
  # print(devices['name'])
  #already in db
  for d in devices:
    a = devices[d]
    deviceName = a['name']
    deviceRssi = a['rssi']
    
    UpdateSignal = None

    for signal, name in currentSignal:
      if deviceName == name and signal.roomId == satellite.roomId:
        if signal is None:
          continue 
        signal.rssi = deviceRssi
        signal.timestamp = datetime.now()
        UpdateSignal = signal
        db.session.commit()
        
    #Create
    if UpdateSignal is None:
      mobile = Mobile.query.filter(Mobile.name == deviceName).first()
      if mobile is None:
        continue
      s = CurrentSignals(mobileId=mobile.id,roomId=satellite.roomId,rssi=deviceRssi,timestamp=datetime.now())
      db.session.add(s)
      db.session.commit()

  for signal, name in currentSignal:
    if not any(dvc for dvc in devices if devices[dvc]['name'] == name):
      db.session.delete(signal)
      db.session.commit()
      continue

  
