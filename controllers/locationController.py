import math
from app.models import CurrentSignals, Mobile, Room, CC,Satellite
from app import db
from controllers import chromecastController as ccC
from sqlalchemy import func
import collections
from datetime import datetime
import json

MUSIC_START_TIME = 0

def determineRoom():
  roomIds = GetCurrentRoomIds()
  ccC.ChangeRoom(roomIds)



def UpdateLocationData(json):
  devices = json['devices']
  satelliteName = json['name'] 
  satellite = db.session.query(Satellite.roomId).filter(Satellite.name == satelliteName).first()
  currentSignal = db.session.query(CurrentSignals,Mobile.name).join(Mobile,Mobile.id == CurrentSignals.mobileId).filter(CurrentSignals.roomId == satellite.roomId).all()
  
  for d in devices.values():
    val = d
    deviceName = val['name']
    deviceRssi = val['rssi']

    CreateSignal(currentSignal,satellite,deviceName, deviceRssi)
    UpdateSignal(currentSignal,deviceName,deviceRssi,satellite)

  DeleteSignal(devices, currentSignal)
   
def CreateSignal(currentSignals, satellite, deviceName, deviceRssi):
  mobile = Mobile.query.filter(Mobile.name == deviceName).first()
  if not mobile:
    return "One or more phones are note added to the db"
  mobileId = mobile.id
  #add only if unique mobileId and roomId
  if not any(sig for sig,name in currentSignals if (sig.mobileId == mobileId and sig.roomId == satellite.roomId)) :
    s = CurrentSignals(mobileId=mobileId,roomId=satellite.roomId,rssi=deviceRssi,timestamp=datetime.now())
    db.session.add(s)
    db.session.commit()
    return

  #only add if the array is empty
  if not currentSignals:
    s = CurrentSignals(mobileId=mobileId,roomId=satellite.roomId,rssi=deviceRssi,timestamp=datetime.now())
    db.session.add(s)
    db.session.commit()
    return


'''
Der skal opdateres når:
- navnet på device findes i nuværende signaler
- roomID er det samme både på satelliten og på de nuværende signaler
'''
def UpdateSignal(currentSignals,deviceName,deviceRssi,satellite):
  for signal, name in currentSignals:
    if signal is None:
      continue
    if deviceName == name and signal.roomId == satellite.roomId:
      signal.rssi = deviceRssi
      signal.timestamp = datetime.now()
      db.session.commit()

def DeleteSignal(devices, currentSignal):
  for signal, name in currentSignal:
    if not any(d for d in devices.values() if d['name'] == name):
      db.session.delete(signal)
      db.session.commit()
      continue


def GetCurrentRoomIds():
  current_signals = db.session.query(CurrentSignals.roomId,func.max(CurrentSignals.rssi)).group_by(CurrentSignals.mobileId).all()
  roomIds = [s for s,x in current_signals]
  return roomIds

def GetCurrentRooms():
  rooms = Room.query.all()
  roomNames = [s for s in rooms]
  return roomNames
