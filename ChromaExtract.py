from __future__ import print_function
from __future__ import division
from pymir import AudioFile
from tqdm import tqdm
import math, h5py
def get_data_chroma_setXY(filename):
    data_setX = []
    data_setY = []
    Y_data_item = AudioFile.open(filename)
    filename = os.path.basename(filename).split(".")[0]
    sr = 22050
    frames = Y_data_item.frames(1024)
    for frame in tqdm(frames):
        chroma = frame.spectrum().chroma()
        continue_flag = False
        for chroma_item in chroma:
            if math.isnan(chroma_item) or math.isinf(chroma_item):
                continue_flag = True
                break
        if continue_flag:
            continue
        data_setX.append(chroma)
        data_setY.append(filename)
    filename = filename.split(".")[0]
    save_h5 = h5py.File(filename + "_chroma.h5","w")
    save_h5.create_dataset("X", data = data_setX)
    save_h5.create_dataset("Y", data = data_setY)
    save_h5.close()
    return 0

# get_data_chroma_setXY(raw_input("FileName:"))
get_data_chroma_setXY("Crawling.wav")
