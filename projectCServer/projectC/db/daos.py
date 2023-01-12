from projectC.db.connections import Engine,CreateDB
from sqlalchemy.orm import Session
from projectC.db.tables import *
from sqlalchemy import select, update, delete
from sqlalchemy.orm import declarative_base


class BasicDao():
    def __init__(self,table=None,connection=None):
        self.connection = connection
        self.table = table

    def setConnection(self,connection):
        self.connection = connection

    def setTable(self,table):
        self.table = table

    def insert(self,data):
        with Session(self.connection) as session:
            session.add_all(data)
            session.commit()

    def delete(self,stmt):
        with Session(self.connection) as session:
            # delete(self.table).where(self.table.id == key)
            session.execute(stmt)
            session.commit()

    def deleteAll(self):
        with Session(self.connection) as session:
            session.execute(delete(self.table))
            session.commit()

    def select(self,stmt):
        with Session(self.connection) as session:
            #stmt = select(self.table).where(self.table.id == key)
            return [client[0] for client in session.execute(stmt)]

    def selectAll(self):
        with Session(self.connection) as session:
            stmt = select(self.table)
            return [client[0] for client in session.execute(stmt)]

    def update(self,data):
        with Session(self.connection) as session:
            values = data.asDict()
            del values['_sa_instance_state']
            session.execute(update(self.table).where(self.table.id == data.id).values(values))
            session.commit()

class ClientDao:
    def __init__(self,basicDao):
        self.basicDao = basicDao
    def insert(self, data):
        return self.basicDao.insert(data)
    def delete(self, id):
        return self.basicDao.delete(delete(self.basicDao.table).where(self.basicDao.table.id == id))
    def deleteAll(self):
        return self.basicDao.deleteAll()
    def select(self, id):
        return self.basicDao.select(select(self.basicDao.table).where(self.basicDao.table.id == id))
    def selectAll(self):
        return self.basicDao.selectAll()
    def update(self, data):
        return self.basicDao.update(data)


class VideoDao:
    def __init__(self,basicDao):
        self.basicDao = basicDao
    def insert(self, data):
        return self.basicDao.insert(data)
    def delete(self, id):
        return self.basicDao.delete(delete(self.basicDao.table).where(self.basicDao.table.id == id))
    def deleteAll(self):
        return self.basicDao.deleteAll()
    def select(self, id):
        return self.basicDao.select(select(self.basicDao.table).where(self.basicDao.table.id == id))
    def selectAll(self):
        return self.basicDao.selectAll()
    def update(self, data):
        return self.basicDao.update(data)

class ObjectDao:
    def __init__(self,basicDao):
        self.basicDao = basicDao
    def insert(self, data):
        return self.basicDao.insert(data)
    def delete(self, videoId):
        return self.basicDao.delete(delete(self.basicDao.table).where(self.basicDao.table.videoId == videoId))
    def deleteAll(self):
        return self.basicDao.deleteAll()
    def select(self,videoId):
        return self.basicDao.select(select(self.basicDao.table).where(self.basicDao.table.videoId == videoId))
    def selectAll(self):
        return self.basicDao.selectAll()
    def update(self, data):
        return self.basicDao.update(data)

class ObjectFrameDataDao:
    def __init__(self,basicDao):
        self.basicDao = basicDao
    def insert(self, data):
        return self.basicDao.insert(data)

    def deleteVideoId(self, videoId):
        return self.basicDao.delete(delete(self.basicDao.table).where(self.basicDao.table.videoId == videoId))
    def delete(self, objectId,videoId):
        return self.basicDao.delete(delete(self.basicDao.table).where(self.basicDao.table.objectId == objectId,self.basicDao.table.videoId == videoId))
    def deleteAll(self):
        return self.basicDao.deleteAll()

    def selectVideoId(self,videoId):
        return self.basicDao.select(select(self.basicDao.table).where(self.basicDao.table.videoId == videoId))
    def select(self,objectId,videoId):
        return self.basicDao.select(select(self.basicDao.table).where(self.basicDao.table.objectId == objectId,self.basicDao.table.videoId == videoId))
    def selectAll(self):
        return self.basicDao.selectAll()
    def update(self, data):
        return self.basicDao.update(data)

class InitDB:
    def __init__(self):
        CreateDB()
        Base = declarative_base()
        engine = Engine().getConnection()
        ClientTable = makeClientsTable(Base)
        Base.metadata.create_all(engine)

class ClientDB():
    def __init__(self,clientId):
        self.Base = declarative_base()
        self.engine = Engine().getConnection()
        self.clientId = clientId
        self.Client = makeClientsTable(self.Base)
        self.Video = makeVideosTable(self.Base,self.clientId)
        self.Object = makeObjectsTable(self.Base,self.clientId)
        self.ObjectFrameData = makeObjectFrameDatasTable(self.Base,self.clientId)
        self.ClientDao = None
        self.VideoDao = None
        self.ObjectDao = None
        self.ObjectFrameDataDao = None

    def createClientTables(self):
        self.Base.metadata.create_all(self.engine)
    def getClientId(self):
        return self.clientId
    def getEngine(self):
        return self.engine
    def getBase(self):
        return self.Base
    def getClientDao(self):
        if self.ClientDao == None:
            self.ClientDao = ClientDao(BasicDao(self.Client,self.engine))
        return self.ClientDao
    def getObjectDao(self):
        if self.ObjectDao == None:
            self.ObjectDao = ObjectDao(BasicDao(self.Object,self.engine))
        return self.ObjectDao

    def getVideoDao(self):
        if self.VideoDao == None:
            self.VideoDao = VideoDao(BasicDao(self.Video,self.engine))
        return self.VideoDao

    def getObjectFrameDataDao(self):
        if self.ObjectFrameDataDao == None:
            self.ObjectFrameDataDao = ObjectFrameDataDao(BasicDao(self.ObjectFrameData,self.engine))
        return self.ObjectFrameDataDao



class LoginDao(ClientDao):
    def __init__(self):
        self.Base = declarative_base()
        self.Client = makeClientsTable(self.Base)
        self.Video = makeVideosTable(self.Base, "null")
        self.Object = makeObjectsTable(self.Base, "null")
        self.ObjectFrameData = makeObjectFrameDatasTable(self.Base, "null")
        self.engine = Engine().getConnection()
        self.ClientsDao = ClientDao(BasicDao(self.Client,self.engine))
        super().__init__(BasicDao(self.Client,self.engine))
