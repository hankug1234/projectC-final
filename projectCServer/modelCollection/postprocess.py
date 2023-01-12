import numpy as np
import torch
import tensorflow as tf
import gc

def pmgPostprocess(model, datas):
    with torch.no_grad():
        output_1, output_2, output_3, output_concat = model(datas)
        gc.collect()
        torch.cuda.empty_cache()
    _, predicts = torch.max(output_concat.data, 1)
    return predicts

def mobileNetPostprocess(model, datas):
    try:
        with tf.device('/device:GPU:0'):
            predicts = model.predict(np.array(datas))
            predicts = [np.argmax(predict) for predict in predicts]
    except Exception:
        predicts = model.predict(np.array(datas))
        predicts = [np.argmax(predict) for predict in predicts]
    return predicts



