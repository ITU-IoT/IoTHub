from app import db
from app.models import Song


def GetSongUrl(id):
    song = Song.query.get(id)
    return song.link
