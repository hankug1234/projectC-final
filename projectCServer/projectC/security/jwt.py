import jwt,hashlib,time,random

class TokenManager:
    def __init__(self):
        self.secrets = {}

    @staticmethod
    def makeSecret(clientId):
        return hashlib.sha256(str(hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest())+clientId+str(random.random()))

    def makeToken(self,clientId):
        self.secrets[clientId] = TokenManager.makeSecret(clientId)
        json = {"clientId": clientId}
        encoded = jwt.encode(json,self.secrets[clientId] , algorithm="HS256")
        return encoded

    def checkToken(self,encoded,clientId):
        try:
            decoded = jwt.decode(encoded,self.secrets[clientId], algorithms="HS256")
            if decoded["clientId"] == clientId:
                return True
            else:
                return False
        except KeyError:
            return False