# final-projectC
projectC is video analysis application using artificial neural network. use this application you can easily search car type and color that you want to search in videos
projectC neural models is located anther repository in https://github.com/hankug1234/models
if you test this application must download models and locate each models in

projectCServer/modelCollection/pmg/ -> carType.pth
projectCServer/modelCollection/tensorflowModels/ -> color.h5
projectCServer/modelCollection/yolo/ -> yolov5l.pth

cartype.pth is pmgnet that was achived sota for stanford car type benchmark and it is pre trained our own 6 car type dataset ["bus","compact","sedan","suv","truck","van"]
color.h5 was pre trained by mobile net and it can classify 7 car color ["black", "blue", "green","red","silver","white","yellow"]
yolo5l.pth is pre trained yolov5 model

if you see more detail aboud our project please check issues and download .mp4 .pdf file
