from sqlalchemy import Column, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String,Text
from sqlalchemy.orm import relationship


def makeClientsTable(base):
    class Client(base):
        __tablename__ = "clients"
        id = Column(String(50),primary_key=True)
        pw = Column(Text)

        video = relationship("Video",back_populates="client",cascade="all, delete-orphan")

        def asDict(self):
            return self.__dict__
        def __repr__(self):
            return f"Client(id={self.id!r}, pw={self.pw!r})"
    return Client

def makeVideosTable(base,clientId_):
    class Video(base):
        __tablename__ = f"{clientId_}_videos"
        id = Column(Integer,primary_key=True,autoincrement=True)
        videoName = Column(String(100))
        videoDirectory = Column(String(300))
        clientId = Column(String(50),ForeignKey("clients.id",ondelete='CASCADE'))
        fps = Column(Float)
        totalFrame = Column(Float)
        width = Column(Float)
        height = Column(Float)
        state = Column(Integer)
        image = Column(Text)

        client = relationship("Client",back_populates="video")
        object = relationship("Object",back_populates="video",cascade="all, delete-orphan")
        objectFrameData = relationship("ObjectFrameData", back_populates="video", cascade="all, delete-orphan")

        def asJson(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ["videoDirectory","clientId","id"]}

        def asDict(self):
            return self.__dict__
        def __repr__(self):
            return f"Video(id={self.id!r},videoName={self.videoName!r},videoDirectory={self.videoDirectory!r},clientId={self.clientId})"
    return Video

def makeObjectsTable(base,clientId):
    class Object(base):
        __tablename__ = f"{clientId}_objects"
        id = Column(Integer,primary_key=True,autoincrement=True)
        className = Column(String(50))
        classColor = Column(String(20))
        startFrame = Column(Integer)
        endFrame = Column(Integer)
        prob = Column(Float)
        image = Column(Text)
        videoId = Column(Integer,ForeignKey(f"{clientId}_videos.id",ondelete='CASCADE'),primary_key=True)

        video = relationship("Video",back_populates="object")
        #objectFrameDataVideoId = relationship("ObjectFrameData", back_populates="objectVideoId", cascade="all, delete-orphan")

        def asJson(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ["id","videoId"]}

        def asDict(self):
            return self.__dict__
        def __repr__(self):
            return f"Object(id={self.id!r}, className={self.className!r}, startFrame={self.startFrame}, endFrame={self.endFrame}, videoId={self.videoId}, prob={self.prob})"

    return Object

def makeObjectFrameDatasTable(base,clientId):
    class ObjectFrameData(base):
        __tablename__ = f"{clientId}_objectFrameDatas"
        objectId = Column(Integer,primary_key=True)
        frameNum = Column(Integer,primary_key=True)
        videoId = Column(Integer,ForeignKey(f"{clientId}_videos.id", ondelete='CASCADE'),primary_key=True)
        x1 = Column(Integer)
        x2 = Column(Integer)
        y1 = Column(Integer)
        y2 = Column(Integer)

        video = relationship("Video",back_populates="objectFrameData")

        def asJson(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}

        def asDict(self):
            return self.__dict__
        def __repr__(self):
            return f"ObjectFrameData(objectId={self.objectId!r}, frameNum={self.frameNum!r}, videoId={self.videoId},x1={self.x1},x3={self.x2},y1={self.y1},y2={self.x2})"
    return ObjectFrameData

