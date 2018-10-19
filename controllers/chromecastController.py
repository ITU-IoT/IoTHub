import time
from app.models import Song,Room,CC
from app import db
import pychromecast


CHROMECASTS = pychromecast.get_chromecasts() #Takes time to load!
print("Done loading CCs")

def IsPlaying(cast):
  for c in CHROMECASTS:
    if cast == c.device.friendly_name:
      return c.media_controller.status.player_state == 'PLAYING'
  return False

def PlaySong(roomIds,song, songTime=0):
  ccs = db.session.query(CC).filter(CC.roomId.in_(roomIds)).all()
  not_ccs = db.session.query(CC).filter(~CC.roomId.in_(roomIds)).all()

  for cast in not_ccs:
    c = GetChromecast(cast.name)
    if c is None:
      return
    mc = c.media_controller
    mc.pause() 

  for cast in ccs:
    c = GetChromecast(cast.name)
    if c is None:
      return
    mc = c.media_controller
    mc.play_media(song,"audio/mp3",current_time=songTime)
      
    
def GetChromecast(name):
  for cast in CHROMECASTS:
    if name == cast.device.friendly_name:
      return cast
  return None

def ChangeRoom(roomIds):
  ccs = db.session.query(CC).all()
  timestamp = 0
  song = None
  for c in ccs:
    cast = GetChromecast(c.name)
    if cast is None:
      continue
    status = IsPlaying(cast.name)
    print("Name: ", cast.device.friendly_name, " Status: ", status )
    if status and any(cr for cr in roomIds if c.roomId == cr):
      continue
    elif status:
      mc = cast.media_controller
      song = mc.status.content_id
      timestamp = mc.status.adjusted_current_time
      print("TimeStamp: ", timestamp, " Song: ", song)
      PlaySong(roomIds,song,timestamp)
    else:
      continue
      

 
