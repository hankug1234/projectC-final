from modelCollection.modelFactory import ClassifyModelsFactory
from projectC.service.analysisManger.analysis import AnalysisCore
import base64,cv2

class AnalysisManger:
    def __init__(self,clientDB=None):
        self.clientDB = clientDB
        self.objectDao = self.clientDB.getObjectDao()
        self.objectFrameDataDao = self.clientDB.getObjectFrameDataDao()
        self.videoPath = None
        self.state = False

    def loadCore(self,analysisCore=AnalysisCore(),name="car"):
        if not self.state:
            self.classifyModelsFactory = ClassifyModelsFactory(name)
            self.analysisCore = analysisCore
            self.models = self.classifyModelsFactory.getClassifyModels()
            self.labels = self.classifyModelsFactory.getLabels()
            self.state = True

    def reset(self):
        if not self.state:
            self.analysisCore.reset()

    def removeCore(self):
        if not self.state:
            self.analysisCore.removeCore()
            del self.models
            del self.classifyModelsFactory
            self.state = False

    def setModels(self,models):
        self.models = models

    def setLabels(self,labels):
        self.labels = labels

    def setName(self,name):
        self.name = name

    def getVideoPath(self):
        return self.videoPath

    def getName(self):
        return self.name

    def getModels(self):
        return self.models

    def getLabels(self):
        return self.labels

    def saveObjectFrameDatas(self,videoId,datas):
        objectFrameDatas = [self.clientDB.ObjectFrameData(objectId=key, videoId=videoId, frameNum=obj[-1], x1=obj[0], y1=obj[1],x2=obj[2], y2=obj[3]) for key in datas.keys() for obj in datas[key]]
        self.objectFrameDataDao.insert(objectFrameDatas)

    def saveObjectDatas(self,videoId,datas):
        images = datas["images"]
        objectId = datas["objectId"]
        framePeriod = datas["period"]
        probs = datas["probs"]
        images = [base64.b64encode(cv2.imencode('.jpg',cv2.resize(image, dsize=(50,50), interpolation=cv2.INTER_AREA))[1]) for image in images]
        className = [self.labels["type"][index] for index in datas["type"]] if len(datas["type"]) !=0 else [None for _ in range(len(objectId))]
        classColor = [self.labels["color"][index] for index in datas["color"]] if len(datas["color"]) !=0 else [None for _ in range(len(objectId))]
        objectList = [self.clientDB.Object(id=objectId, className=type, classColor=color, startFrame=period[0],endFrame=period[1], videoId=videoId, prob=probs,image=image) for objectId,type,color,period,probs,image in zip(objectId,className,classColor,framePeriod,probs,images)]
        self.objectDao.insert(objectList)


    def executeService(self,videoPath,videoId,batchSize=150):
        self.videoPath = videoPath
        self.loadCore()
        self.reset()
        for result in self.analysisCore.excuteAnalysisBatch(videoPath,self.models,batchSize):
            if result["type"] == "tracking-progress":
                self.saveObjectFrameDatas(videoId,result["result"])
            elif result["type"] == "labeling-progress":
                self.saveObjectDatas(videoId,result["result"])
            else:
                pass
            yield {"type":result["type"],"progress":result["progress"]}


    def selectAnalysisData(self,videoId,condition):
        result = {"videoId":videoId,"datas":{}}
        objectInfo = self.objectDao.select(videoId)
        framedatas = self.objectFrameDataDao.selectVideoId(videoId)
        for obj in objectInfo:
            if obj.className in condition["type"] and obj.classColor in condition["color"]:
                result["datas"][f"{obj.id}"] = obj.asJson()
                result["datas"][f"{obj.id}"]["frameData"] = {}

        for frame in framedatas:
            try:
                result["datas"][f"{frame.objectId}"]["frameData"][f"{frame.frameNum}"] = {"x1":str(frame.x1),"y1":str(frame.y1),"x2":str(frame.x2),"y2":str(frame.y2)}
            except KeyError:
                pass
        return result

    def deleteAnalysis(self, videoId):
        self.objectFrameDataDao.deleteVideoId(videoId)
        self.objectDao.delete(videoId)

    def deleteAllAnalysis(self):
        self.objectFrameDataDao.deleteAll()
        self.objectDao.deleteAll()


