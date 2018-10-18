import math
from app.models import CurrentSignals, Mobile
from app import db
from sqlalchemy import func

bestRssi = dict()
currentRoom = dict()

def determineRoom():
  current_signals = db.session.query(CurrentSignals.roomId,func.max(CurrentSignals.rssi)).group_by(CurrentSignals.mobileId).all()
  
  for signal in current_signals:
    print(signal)
