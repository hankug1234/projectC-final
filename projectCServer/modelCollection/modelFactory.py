import torch
import tensorflow as tf
import sys
import os
import json
from modelCollection import postprocess
from modelCollection import preprocess

class TensorModel:
    def __init__(self,modelDirectory=None,modelName=None):
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                tf.config.experimental.set_virtual_device_configuration(gpus[0],[tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                print(e)

        self.modelDirectory = modelDirectory
        self.modelName = modelName
        self.model = None

    def loadModel(self):
        sys.path.insert(0, self.modelDirectory)
        self.model = tf.keras.models.load_model(os.path.sep.join([self.modelDirectory,self.modelName]))

    def setModelName(self,modelName):
        self.modelName = modelName

    def setModelDirectory(self,directory):
        self.modelDirectory = directory

    def getModel(self):
        if self.model == None:
            self.loadModel()
        return self.model


class TorchModel:
    def __init__(self,modelDirectory=None,modelName=None):
        self.modelDirectory = modelDirectory
        self.modelName = modelName
        self.model = None

    def loadModel(self):
        sys.path.insert(0, self.modelDirectory)
        self.model = torch.load(os.path.sep.join([self.modelDirectory,self.modelName]))
        self.model.eval()
        if torch.cuda.is_available():
            device = torch.device("cuda")
            self.model.to(device)

    def setModelName(self,modelName):
        self.modelName = modelName

    def setModelDirectory(self,directory):
        self.modelDirectory = directory

    def getModel(self):
        if self.model == None:
            self.loadModel()
        return self.model

class ModelForVideo:
    def __init__(self,modelDirectory,modelName,preprocess=lambda x:x,postProcess=lambda x,y:[]):
        self.model = TensorModel(modelDirectory,modelName).getModel() if "h5" in modelName else TorchModel(modelDirectory,modelName).getModel()
        self.preprocess = preprocess
        self.postProcess = postProcess

    def predict(self,frames):
        return self.postProcess(self.model, self.preprocess(frames))

class DetectorFactory:
    def __init__(self):
        configPath = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2] + ["config", "appConfig.json"])
        modelPath = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
        with open(configPath, "r") as file:
            config = json.load(file)
            config = config["detector"]
            self.detector = TorchModel(os.path.sep.join([modelPath, config["name"]]),config["model"]).getModel()
            self.filterNums = config["filterNums"]

    def getDetector(self):
        return self.detector

    def getFilterNums(self):
        return self.filterNums

class ClassifyModelsFactory:
    def __init__(self,name):
        configPath = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2] + ["config", "appConfig.json"])
        modelPath = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
        with open(configPath, "r") as file:
            config = json.load(file)
            config = config[name]
            self.classifyModels = {key:ModelForVideo(os.path.sep.join([modelPath,config[key]["name"]]),config[key]["model"],getattr(preprocess,config[key]["pre"])
                                                     ,getattr(postprocess,config[key]["post"])) for key in config.keys()}
            self.labels = {key:config[key]["label"] for key in config.keys()}

    def getClassifyModels(self):
        return self.classifyModels

    def getLabels(self):
        return self.labels


