from flask import request,Blueprint
from flask_restx import Api, Resource
from projectC.service.clientManager.manager import ClientManager

blueprint = Blueprint("client",__name__)
clientApi = Api(blueprint)

@clientApi.route('/signUp')
class SignUpManager(Resource):
    def get(self):
        parameters = request.args.to_dict()
        clientId = parameters["clientId"]
        clientManager = ClientManager()
        result = clientManager.checkDuplicated(clientId)
        return {"result":result}

    def post(self):
        clientId = request.form["clientId"]
        clientPw = request.form["clientPw"]
        clientManager = ClientManager()
        clientManager.makeNewClient(clientId,clientPw)
        return {"result": True}

@clientApi.route('/signIn')
class SignInManager(Resource):
    def post(self):
        clientId = request.form["clientId"]
        clientPw = request.form["clientPw"]
        clientManager = ClientManager()
        check = clientManager.checkDuplicated(clientId)
        if check:
            pw = clientManager.selectPassword(clientId)
            if clientPw == pw:
                return {"result":True}
        return {"result":False}

@clientApi.route('/info/<string:clientId>')
class ClientInfo(Resource):
    def get(self,clientId):
        clientManager = ClientManager()
        check = clientManager.checkDuplicated(clientId)
        if check:
            pw = clientManager.selectPassword(clientId)
            return {"result":True,"clientId":clientId,"clientpw":pw}
        return {"result":False}