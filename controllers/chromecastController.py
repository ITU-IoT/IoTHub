import time
from app.models import Song,Room,CC
from app import db
import pychromecast


CHROMECASTS = pychromecast.get_chromecasts() #Takes time to load!
print("Done loading chromecasts")

def IsPlaying(cast):
  for chromecast in CHROMECASTS:
    if cast == chromecast.device.friendly_name:
      return chromecast.media_controller.status.player_state == 'PLAYING'
  return False

def PlaySong(roomIds,song, songTime=0):
  chromecasts = db.session.query(CC).filter(CC.roomId.in_(roomIds)).all()
  not_chromecasts = db.session.query(CC).filter(~CC.roomId.in_(roomIds)).all()

  for ccast in not_chromecasts:
    chromecast = GetChromecast(ccast.name)
    if chromecast is None:
      continue
    mc = chromecast.media_controller
    if IsPlaying(chromecast):
      mc.pause()

  for ccast in chromecasts:
    chromecast = GetChromecast(ccast.name)
    if chromecast is None:
      continue
    mc = chromecast.media_controller
    if IsPlaying(chromecast) and mc.status.content_id == song:
      print("I am already playing")
      continue
    print("I need to play this song: ", song)
    mc.play_media(song,"audio/mp3",current_time=songTime)


def GetChromecast(name):
  for chromecast in CHROMECASTS:
    if name == chromecast.device.friendly_name:
      return chromecast
  return None

def ChangeRoom(roomIds):
  chromesasts = db.session.query(CC).all()
  timestamp = 0
  song = None

  for ccast in chromesasts:
    chromecast = GetChromecast(ccast.name)
    if IsPlaying(chromecast.name):
      mc = chromecast.media_controller
      song = mc.status.content_id
      timestamp = mc.status.adjusted_current_time
      break

  if song is None:
    return

  PlaySong(roomIds, song, timestamp)
  return
'''
  for ccast in chromesasts:
    chromecast = GetChromecast(ccast.name)
    if chromecast is None:
      continue
    status = IsPlaying(chromecast.name)
    print("Name: ", chromecast.device.friendly_name, " Status: ", status )
    if status and any(roomId for roomId in roomIds if ccast.roomId == roomId):
      if chromecast.media_controller.status.content_id != song:
        PlaySong(roomIds,song,timestamp)
      continue
    elif not status and any(roomId for roomId in roomIds if ccast.roomId == roomId):
      print("TimeStamp: ", timestamp, " Song: ", song)
      PlaySong(roomIds,song,timestamp)
    elif status and not any(roomId for roomId in roomIds if ccast.roomId == roomId):
      chromecast.media_controller.pause()
    else:
      continue
      '''



