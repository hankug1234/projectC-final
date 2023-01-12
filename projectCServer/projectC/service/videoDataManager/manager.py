import base64

from flask import send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
import time
import hashlib
import cv2

class VideoDataManager:

    def __init__(self,clientDB=None):
        self.clientDB = clientDB
        self.videoDao = self.clientDB.getVideoDao()
        self.ALLOWED_EXTENSIONS = []

    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS

    def deleteFile(self,videoId):
        video = self.videoDao.select(videoId)[0]
        BASE_DIR = os.path.dirname(video.videoDirectory)
        if os.path.isfile(video.videoDirectory):
            os.remove(video.videoDirectory)
        fileList = os.listdir(BASE_DIR)
        if len(fileList) == 0:
            os.rmdir(BASE_DIR)
        self.videoDao.delete(videoId)
        return True

    def fileSaver(self,request):
        clientId = self.clientDB.getClientId()
        BASE_DIR = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-4] + ["userVideos"])
        clientVideosDirectory = os.path.join(BASE_DIR,clientId)
        if not os.path.exists(clientVideosDirectory):
            os.makedirs(clientVideosDirectory)

        try:
            sha1 = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()
        except Exception:
            sha1 = hashlib.sha1(str(time.time())).hexdigest()

        secure_name = sha1+secure_filename(request.files['file'].filename)
        savePath = os.path.join(clientVideosDirectory,secure_name)
        videoDao = self.videoDao

        f = request.files['file']
        f.save(savePath)
        video = cv2.VideoCapture(savePath)
        fps, f_count,width,height = video.get(cv2.CAP_PROP_FPS), video.get(cv2.CAP_PROP_FRAME_COUNT),video.get(cv2.CAP_PROP_FRAME_WIDTH),video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ret,image = video.read()
        if ret:
            image = base64.b64encode(cv2.imencode('.jpg',cv2.resize(image, dsize=(100,100), interpolation=cv2.INTER_AREA))[1])
        else:
            image = "none"
        videoDao.insert([self.clientDB.Video(width=width,height=height,fps = fps,totalFrame=f_count,videoName=request.files['file'].filename, videoDirectory=savePath, clientId=clientId,state=0,image=image)])
        video.release()
        return redirect(request.referrer)

    def fileSender(self,videoId):
        videoDao = self.videoDao
        video = videoDao.select(videoId)[0]
        path = video.videoDirectory
        BASE_DIR = os.path.dirname(path)
        FILE_NAME = os.path.basename(path)
        return send_from_directory(BASE_DIR,FILE_NAME)

    def selectVideoDatas(self):
        videos = self.videoDao.selectAll()
        videoDict = {}
        for video in videos:
            videoDict[video.id] = video.asJson()
        return videoDict

    def changeState(self,videoId,state):
        video = self.videoDao.select(videoId)[0]
        video.state = state
        self.videoDao.update(video)

    def selectVideoData(self,videoId):
        video = self.videoDao.select(videoId)[0]
        info = video.asJson()
        return info

    def getVideoPath(self,videoId):
        video = self.videoDao.select(videoId)[0]
        return video.videoDirectory


