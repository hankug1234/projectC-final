from projectC.db.daos import LoginDao
from projectC.db.daos import ClientDB
class ClientManager:
    def __init__(self):
        self.LoginDao = LoginDao()

    def checkDuplicated(self,userId):
        result = self.LoginDao.select(userId)
        if len(result) == 0:
            return False
        else:
            return True

    def makeNewClient(self,id,pw):
        if self.checkDuplicated(id):
            return False
        else:
            self.LoginDao.insert([self.LoginDao.Client(id=id,pw=pw)])
            result = ClientDB(id)
            result.createClientTables()
            return result

    def deleteClient(self,clientDB):
        Base = clientDB.getBase()
        client = clientDB.getClientDao()
        client.delete(clientDB.getClientId())
        Base.metadata.drop_all(bind=clientDB.getEngine(), tables=[clientDB.ObjectFrameData.__table__,clientDB.Object.__table__,clientDB.Video.__table__])
        return True

    def updateClient(self,data):
        self.LoginDao.update(data)
        return True

    def selectPassword(self,clientId):
        client = self.LoginDao.select(clientId)[0]
        return client.pw



