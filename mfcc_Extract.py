# from scikits.talkbox.features import mfcc
from pymir import AudioFile
import math, h5py
from tqdm import tqdm
def get_data_chroma_setXY(filename):
    data_setX = []
    data_setY = []
    Y_data_item = AudioFile.open(filename)
    filename = os
    frames = Y_data_item.frames(1024)
    for frame in tqdm(frames):
        mfcc_data = frame.spectrum().mfcc2()
        continue_flag = False
        for mfcc_item in mfcc_data:
            if math.isnan(mfcc_item) or math.isinf(mfcc_item):
                continue_flag = True
                break
        if continue_flag:
            continue
        data_setX.append(mfcc_data)
        data_setY.append(filename)
    filename = filename.split(".")[0]
    save_h5 = h5py.File(filename + "_mfcc.h5","w")
    save_h5.create_dataset("X", data = data_setX)
    save_h5.create_dataset("Y", data = data_setY)
    save_h5.close()
    return 0

get_data_chroma_setXY("Crawling.wav")
