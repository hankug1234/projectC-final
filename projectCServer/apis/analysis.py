from flask import request,Blueprint
from flask_restx import Api, Resource
from projectC.background.background import BackgroundService
from projectC.service.analysisManger.manager import AnalysisManger
from projectC.service.videoDataManager.manager import VideoDataManager
from projectC.db.daos import ClientDB
from multiprocessing import Queue,Lock


blueprint = Blueprint("analysis",__name__)
analysisApi = Api(blueprint)

class QueueManager:
    def __init__(self):
        self.repository = {}

    def getVideoList(self,clientId):
        try:
            result = list(self.repository[clientId].keys())
        except KeyError:
            result = []
        return result

    def setQueue(self,clientId,videoId,queue):
        if clientId in list(self.repository.keys()):
            with Lock():
                self.repository[clientId][videoId] = queue
        else:
            with Lock():
                self.repository[clientId] = {videoId:queue}

    def getProgress(self,clientId,videoId):
        try:
            queue = self.repository[clientId][videoId]
            progress = queue.get()
            if progress["type"] == "done":
                del self.repository[clientId][videoId]
            return progress

        except KeyError:
            return {"type":"none","progress":0}

queueManager = QueueManager()

@analysisApi.route('/info/<string:clientId>/<int:videoId>')
class AnalysisManager(Resource):
    def post(self,clientId,videoId):
        client = ClientDB(clientId)
        analysisInfo = AnalysisManger(clientDB=client).selectAnalysisData(videoId,{"type":request.form["types"].split(","),"color":request.form["colors"].split(",")})
        analysisInfo["info"] = VideoDataManager(clientDB=client).selectVideoData(videoId)
        return analysisInfo

@analysisApi.route('/progress/<string:clientId>/<int:videoId>')
class Progress(Resource):
    def get(self,clientId,videoId):
        return queueManager.getProgress(clientId,videoId)

@analysisApi.route('/progress/<string:clientId>')
class ProgressList(Resource):
    def get(self,clientId):
        return {"result":queueManager.getVideoList(clientId)}

@analysisApi.route('/execute/<string:clientId>/<int:videoId>')
class DoAnalysis(Resource):
    def get(self,clientId,videoId):
        video = VideoDataManager(ClientDB(clientId)).selectVideoData(videoId)
        if video["state"] == 2:
            return {"type":"done"}
        queue = Queue()
        process = BackgroundService(clientId,queue,videoId,75)
        process.start()
        queueManager.setQueue(clientId, videoId, queue)
        return {"type":"success"}
