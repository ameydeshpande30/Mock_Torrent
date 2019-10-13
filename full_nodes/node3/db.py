from peewee import *
import datetime


# db = SqliteDatabase('torrent.db')
db = SqliteDatabase('torrent.db')
class BaseModel(Model):
    class Meta:
        database = db


class Torrent(BaseModel):
    id = PrimaryKeyField(AutoField)
    name = CharField(max_length=150)
    parts = IntegerField(default=5)
    ext = CharField(max_length=10)
    file_hash = CharField(max_length=100)

class Peer(BaseModel):
    id = PrimaryKeyField(AutoField)
    name = CharField(max_length=150)
    ip = CharField(max_length=150)


db.connect()
db.create_tables([Torrent, Peer])

def addData(name, parts, file_hash, ext, ip):
    Torrent.create(name=name, parts=parts, file_hash=file_hash, ext=ext)
    db.commit()
    addPeer(ip, name)

def addPeer(ip, name):
    Peer.create(name=name, ip=ip)
    db.commit()

def getTorrent(name):
    out = Torrent.select().where(Torrent.name == name).get()
    data = {}
    data["name"] = out.name
    data["file_hash"] = out.file_hash
    data["parts"] = out.parts
    return(data)

def getPerrs(name):
    out = Peer.select().where(Peer.name == name)
    print(out)
    allip = list(out)
    all = [t for t in out]
    print(all)
    IP = []
    for i in all:
        IP.append(i.ip)
    return IP
