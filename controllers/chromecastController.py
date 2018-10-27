import time
from app.models import Song,Room,CC
from app import db
import pychromecast


CHROMECASTS = pychromecast.get_chromecasts() #Takes time to load!
print("Done loading chromecasts")

def StopCCs():
  chromecasts = db.session.query(CC).all()

  for ccast in chromecasts:
    chromecast = GetChromecast(ccast.name)
    mc = chromecast.media_controller
    mc.stop()
    
def PauseCCs():
  chromecasts = db.session.query(CC).all()

  for ccast in chromecasts:
    chromecast = GetChromecast(ccast.name)
    mc = chromecast.media_controller
    mc.pause()
    
 

def PlaySong(roomIds,song, songTime=0):
  chromecasts = db.session.query(CC).filter(CC.roomId.in_(roomIds)).all()
  not_chromecasts = db.session.query(CC).filter(~CC.roomId.in_(roomIds)).all()

  for ccast in not_chromecasts:
    chromecast = GetChromecast(ccast.name)
    if chromecast is None:
      continue
    mc = chromecast.media_controller
    if IsPlaying(chromecast.name):
      mc.pause()

  for ccast in chromecasts:
    chromecast = GetChromecast(ccast.name)
    if chromecast is None:
      continue
    mc = chromecast.media_controller
    if IsPlaying(chromecast.name) and song == mc.status.content_id:
      continue
    mc.play_media(song,"audio/mp3",current_time=songTime)


def ChangeRoom(roomIds):
  chromesasts = db.session.query(CC).all()
  timestamp = 0
  song = None

  for cast in chromesasts:
    chromecast = GetChromecast(cast.name)
    if chromecast is None:
      continue
    if IsPlaying(chromecast.device.friendly_name):
      mc = chromecast.media_controller
      song = mc.status.content_id
      timestamp = mc.status.adjusted_current_time
      break

  if song is None:
    return

  PlaySong(roomIds, song, timestamp)
  return


def GetChromecast(name):
  for chromecast in CHROMECASTS:
    if name == chromecast.device.friendly_name:
      return chromecast
  return None

def IsPlaying(name):
  for chromecast in CHROMECASTS:
    if name == chromecast.device.friendly_name:
      return chromecast.media_controller.status.player_state == 'PLAYING'
        #return True
  return False




