from flask import request,Blueprint
from flask_restx import Api, Resource
from projectC.service.clientManager.manager import ClientManager
from projectC.service.videoDataManager.manager import VideoDataManager
from projectC.db.daos import ClientDB

blueprint = Blueprint("video",__name__)
videoApi = Api(blueprint)

@videoApi.route("/list/<string:clientId>")
class VideoManager(Resource):
    def get(self,clientId):
        return VideoDataManager(ClientDB(clientId)).selectVideoDatas()

@videoApi.route('/file/<string:clientId>')
class UploadFile(Resource):
    def post(self,clientId):
        clientManager = ClientManager()
        result = clientManager.checkDuplicated(clientId)
        if result:
            VideoDataManager(ClientDB(clientId)).fileSaver(request)
            return {"result":"success"}
        else:
            return {"result":"fail"}

@videoApi.route('/file/<string:clientId>/<int:videoId>')
class DownLoadFile(Resource):
    def get(self,clientId,videoId):
        return VideoDataManager(ClientDB(clientId)).fileSender(videoId)

@videoApi.route('/delete/<string:clientId>/<int:videoId>')
class DeleteVideo(Resource):
    def get(self,clientId,videoId):
        VideoDataManager(ClientDB(clientId)).deleteFile(videoId)
        return {"result":"success"}
