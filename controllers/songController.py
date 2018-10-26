from app.models import Song
from app import db

def GetSongUrl(id):
    song = Song.query.get(id)
    return song.link
