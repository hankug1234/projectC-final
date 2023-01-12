from multiprocessing import Process
from projectC.db.daos import ClientDB
from projectC.service.analysisManger.manager import AnalysisManger
from projectC.service.videoDataManager.manager import VideoDataManager

class BackgroundService(Process):
    def __init__(self,clientId,queue,videoId,batchSize=150):
        super(BackgroundService, self).__init__()
        self.clientId = clientId
        self.batchSize = batchSize
        self.videoId = videoId
        self.queue = queue

    def run(self):
        client = ClientDB(self.clientId)
        analysisManager = AnalysisManger(client)
        videoDataManager = VideoDataManager(client)
        videoPath = videoDataManager.getVideoPath(self.videoId)
        for result in analysisManager.executeService(videoPath,self.videoId,self.batchSize):
            self.queue.put(result)
        videoDataManager.changeState(self.videoId,2)