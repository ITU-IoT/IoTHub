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
  print("RoomIds:", roomIds)
  ccC.ChangeRoom(roomIds)




def UpdateLocationData(json):
  devices = json['devices']
  print("Devices", devices)
  satelliteName = json['name'] 
  
  satellite = db.session.query(Satellite.roomId).filter(Satellite.name == satelliteName).first()
  print(satellite.roomId)

  #update db
  currentSignal = db.session.query(CurrentSignals,Mobile.name).join(Mobile,Mobile.id == CurrentSignals.mobileId).filter(CurrentSignals.roomId == satellite.roomId).all()
  # print(devices['name'])
  #already in db
  for d in devices:
    a = devices[d]
    deviceName = a['name']
    deviceRssi = a['rssi']
    
    print("Device name    ", deviceName)
    UpdateSignal = None

    for signal, name in currentSignal:
      if deviceName == name and signal.roomId == satellite.roomId:
        signal.rssi = deviceRssi
        signal.timestamp = datetime.now()
        UpdateSignal = signal
        db.session.commit()
        break

    #Create
    if UpdateSignal is None:
      mobile = Mobile.query.filter(Mobile.name == deviceName).first()
      print(mobile)
      print(deviceName)
      if mobile is None:
        continue
      s = CurrentSignals(mobileId=mobile.id,roomId=satellite.roomId,rssi=deviceRssi,timestamp=datetime.now())
      db.session.add(s)
      db.session.commit()
      break

  for signal, name in currentSignal:
    if not any(d for d in devices if deviceName == name):
      db.session.delete(signal)
      db.session.commit()
      break

  
