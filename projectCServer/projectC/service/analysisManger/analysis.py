import numpy as np
import cv2
from tracker.sort import Sort
from modelCollection.modelFactory import DetectorFactory
import torch

class AnalysisCore:
    def __init__(self, tracker=Sort()):
        self.detectorFactory = DetectorFactory()
        self.tracker = tracker
        self.detector = self.detectorFactory.getDetector()
        self.filterNums = self.detectorFactory.getFilterNums()
        self.objectFrames = {}
        self.objects = {}
        self.frameCount = 0

    def removeCore(self):
        del self.detector
        del self.detectorFactory
        del self.tracker

    def resetObject(self):
        self.objectFrames = {}
    
    def reset(self,tracker = Sort()):
        del self.objectFrames
        del self.objects
        del self.tracker

        self.tracker = tracker
        self.objectFrames = {}
        self.objects = {}
        self.frameCount = 0

    def setTracker(self,tracker):
        self.tracker = tracker
    def setDetector(self,detector):
        self.detector = detector
    def setFilterNums(self,filterNums):
        self.filterNums = filterNums

    def getObjectFrames(self):
        return self.objectFrames
    def getObjects(self):
        return self.objects

    def readBetch(self,video,batchSize):
        results = []
        for i in range(batchSize):
            ret,frame = video.read()
            if ret:
                results.append(frame)
            else:
                break
        return results

    def getFrame(self, video, num):
        video.set(1, num)
        _, frame = video.read()
        return frame

    def getFrameBatch(self, video, index, batch):
        totalFrames = len(index)
        maxIter = int(totalFrames / batch) if totalFrames % batch == 0 else (int(totalFrames / batch) + 1)
        for i in range(maxIter):
            start = i * batch
            end = start + batch
            if end > totalFrames:
                yield [(i,self.getFrame(video, i)) for i in index[start:]]
            else:
                yield [(i,self.getFrame(video, i)) for i in index[start:end]]

    def getObjectImagesBatch(self, video, batch):
        objects = self.getObjects()
        framesPerobjectsInfo = {}
        processed = 0
        for key in objects.keys():
            try:
                framesPerobjectsInfo[objects[key]["num"]].append(
                    {"objectId": key, "location": objects[key]["location"],"start":objects[key]["start"],"end":objects[key]["end"],"prob":objects[key]["prob"]})
            except KeyError:
                framesPerobjectsInfo[objects[key]["num"]] = [
                    {"objectId": key, "location": objects[key]["location"],"start":objects[key]["start"],"end":objects[key]["end"],"prob":objects[key]["prob"]}]

        frameList = sorted(list(framesPerobjectsInfo.keys()))

        if video.isOpened():
            for frames in self.getFrameBatch(video, frameList, batch):
                objectIds, images, period, probs = [], [], [], []
                for i,frame in frames:
                    for obj in framesPerobjectsInfo[i]:
                        image = frame[obj["location"][1]:obj["location"][3],obj["location"][0]:obj["location"][2]]
                        shape = image.shape
                        if shape[0]==0 or shape[1]==0:
                            continue
                        images.append(image)
                        objectIds.append(obj["objectId"])
                        period.append((obj["start"],obj["end"]))
                        probs.append(obj["prob"])
                processed+=len(objectIds)
                yield (objectIds,images,float(processed/len(list(objects.keys()))),period,probs)
        else:
            raise Exception

    def doTrackingBatch(self, video, batch):
        totalFrame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        maxIter = int(totalFrame / batch) if totalFrame % batch == 0 else int(totalFrame / batch) + 1
        for i in range(maxIter):
            self.resetObject()
            self.trackingBatch(self.readBetch(video, batch))
            yield {"type":"tracking-progress","progress":float((i+1)/maxIter),"result":self.getObjectFrames()}

    def doClassifyBatch(self, video, models, batch):
        for imageResults in self.getObjectImagesBatch(video, batch):
            result = {}
            result["objectId"] = imageResults[0]
            result["period"] = imageResults[3]
            result["probs"] = imageResults[4]
            result["images"] = imageResults[1]
            for key in models.keys():
                result[key] = models[key].predict(imageResults[1])
            yield {"type": "labeling-progress", "progress":imageResults[2], "result": result}

    def trackingBatch(self, frames):
        with torch.no_grad():
            objectsPerFrames = self.detector(frames).pandas().xyxy
            torch.cuda.empty_cache()
        objectsPerFrames = [np.array(objectsPerFrame[objectsPerFrame['class'].isin(self.filterNums)].iloc[:, :-2]) for objectsPerFrame in objectsPerFrames]
        mappingIdToObjectsPerFrames = [self.tracker.update(objectsPerFrame) for objectsPerFrame in objectsPerFrames]


        for frameCount,objects in enumerate(mappingIdToObjectsPerFrames):
            for obj in objects:
                prob = obj[-1]
                num = (self.frameCount + frameCount)
                obj = np.append(obj[:-1].astype(int), [num])
                try:
                    self.objectFrames[obj[-2]].append(obj)

                except KeyError:
                    self.objectFrames[obj[-2]] = [obj]

                try:
                    if self.objects[obj[-2]]["prob"] < prob:
                        self.objects[obj[-2]]["num"] = num
                        self.objects[obj[-2]]["prob"] = prob
                        self.objects[obj[-2]]["location"] = [obj[0], obj[1], obj[2], obj[3]]
                    self.objects[obj[-2]]["end"] = num
                except KeyError:
                    self.objects[obj[-2]] = {"num": num, "location": [obj[0], obj[1], obj[2], obj[3]], "start": num,"end": num, "prob": prob}

        self.frameCount +=len(frames)

    def excuteAnalysisBatch(self,videoPath,models,batchSize=150):
        video = cv2.VideoCapture(videoPath)
        if video.isOpened():
            for progress in self.doTrackingBatch(video, batchSize):
                yield progress

            for progress in self.doClassifyBatch(video, models, batchSize):
                yield progress
        yield {"type": "done","progress":100}


