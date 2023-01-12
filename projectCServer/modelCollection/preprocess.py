from torchvision import transforms
from torch.autograd import Variable
import torch
from PIL import Image
import cv2

def pmgPreprocess(frames):
    transform = transforms.Compose([
        transforms.Resize((550, 550)),
        transforms.CenterCrop(448),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    frames = [Image.fromarray(frame) for frame in frames]
    frames = torch.stack([transform(frame) for frame in frames], 0)
    if torch.cuda.is_available():
        frames = frames.to("cuda")
    frames = Variable(frames, volatile=True)

    return frames

def mobileNetPreprocess(frames):
    frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
    frames = [cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_AREA)/255 for frame in frames]
    return frames