from pydub import AudioSegment
import os
# from scikits.talkbox.features import mfcc
from pymir import AudioFile
import math, h5py
from tqdm import tqdm
def formatAllAudio(path = 'raw_record_IUO_singing_reading_conversion'):
    for root, dirs, files in os.walk(path):
        for audioName in files:
            audioPath = os.path.join(root, audioName)
            print audioPath
            if '.doc' not in audioPath:
                # audioFormat = audioPath.split('.')[-1]
                audioFormat = audioPath[-3:]

                outPath = 'output_mono_16k/' + os.path.basename(audioPath).split('.')[0] + '.wav'
                audioContent = AudioSegment.from_file(audioPath, audioFormat)
                audioContent = audioContent.set_channels(1)
                audioContent = audioContent.set_frame_rate(16000)
                if not os.path.exists(os.path.dirname(outPath)):
                    os.makedirs(os.path.dirname(outPath))
                audioContent.export(outPath, 'wav')

    return 0

def get_mono(wav_path):
    audio = AudioSegment.from_wav(wav_path)
    audio = audio.set_channels(1)
    # print audio.frame_rate
    audio.export('sL-mono.wav','wav')

def readText(text_path = "002 btag.txt"):
    txt = open(text_path)
    songs = []
    i = 0
    for chunk in txt.readlines():
        chunk = chunk.split('\r')[0]
        song = chunk.split('\t')
        songs.append(song)
    return songs

def get_ms(str_time = "01.34.44.450"):
    timeList = str_time.split('.')
    num = len(timeList)
    for i in range(num):
        timeList[i] = int(timeList[i])
    if num == 2:
        MilliSecond = timeList[-1] + timeList[-2] * 1000
    elif num == 3:
        MilliSecond = timeList[-1] + timeList[-2] * 1000 + timeList[-3] * 60 * 1000
    elif num == 4:
        MilliSecond = timeList[-1] + timeList[-2] * 1000 + timeList[-3] * 60 * 1000\
            + timeList[-4] * 60 * 60 * 1000
    return MilliSecond

def songs_str_to_time(songs):
    num = len(songs)
    for i in range(num):
        songs[i][1] = get_ms(songs[i][1])
        songs[i][2] = get_ms(songs[i][2])
    print songs

# def get_data_chroma_setXY(output):
#     data_setX = []
#     data_setY = []
#     for root, dirs, files in os.walk("./Linkin_Park_Live_in_Texas_mp3/output_mono"):
#         for filename in files:
#             if ".wav" not in filename:
#                 continue
#             filename = os.path.join(root, filename)
#             Y_data_item = AudioFile.open(filename)
#             filename = os.path.basename(filename).split(".")[0]
#             sr = 22050
#             frames = Y_data_item.frames(1024)
#             for frame in tqdm(frames):
#                 chroma = frame.spectrum().chroma()
#                 continue_flag = False
#                 for chroma_item in chroma:
#                     if math.isnan(chroma_item) or math.isinf(chroma_item):
#                         continue_flag = True
#                         break
#                 if continue_flag:
#                     continue
#                 data_setX.append(chroma)
#                 data_setY.append(filename)
#     save_h5 = h5py.File(output + "_chroma.h5","w")
#     save_h5.create_dataset("X", data = data_setX)
#     save_h5.create_dataset("Y", data = data_setY)
#     save_h5.close()

def get_studio_chroma_setXY():
    data_setX = []
    data_setY = []

    # inputting
    while True:
        try:
            path = raw_input("studio_chroma:\n")
        except:
            break
        if ".wav" not in path:
            continue
        Y_data_item = AudioFile.open(path)
        filename = os.path.basename(path).split(".")[0]

        # frame splitting
        frames = Y_data_item.frames(1024)

        # chroma extracting
        for frame in tqdm(frames):
            chroma = frame.spectrum().chroma()
            continue_flag = False
            for mfcc_item in mfcc_data:
                if math.isnan(chroma_item) or math.isinf(chroma_item):
                    continue_flag = True
                    break
            if continue_flag:
                continue
            data_setX.append(chroma)
            data_setY.append(filename)

    # saving
    save_h5 = h5py.File("studio_songs_chroma.h5","w")
    save_h5.create_dataset("X", data = data_setX)
    save_h5.create_dataset("Y", data = data_setY)
    save_h5.close()

def get_studio_mfcc_setXY():
    data_setX = []
    data_setY = []

    # inputting
    while True:
        try:
            path = raw_input("studio_mfcc:\n")
        except:
            break
        if ".wav" not in path:
            continue
        Y_data_item = AudioFile.open(path)
        filename = os.path.basename(path).split(".")[0]

        # frame splitting
        frames = Y_data_item.frames(1024)

        # mfcc extracting
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

    # saving
    save_h5 = h5py.File("studio_songs_mfcc.h5","w")
    save_h5.create_dataset("X", data = data_setX)
    save_h5.create_dataset("Y", data = data_setY)
    save_h5.close()

def get_live_chroma_setXY():
    data_setX = []
    data_setY = []
    while True:
        try:
            path = raw_input("live_chroma:\n")
        except:
            break
        if ".wav" not in path:
            continue
        Y_data_item = AudioFile.open(path)
        filename = os.path.basename(path).split(".")[0]
        frames = Y_data_item.frames(1024)
        for frame in tqdm(frames):
            chroma = frame.spectrum().chroma()
            continue_flag = False
            for mfcc_item in mfcc_data:
                if math.isnan(chroma_item) or math.isinf(chroma_item):
                    continue_flag = True
                    break
            if continue_flag:
                continue
            data_setX.append(chroma)
            data_setY.append(filename)
    save_h5 = h5py.File("live_songs_chroma.h5","w")
    save_h5.create_dataset("X", data = data_setX)
    save_h5.create_dataset("Y", data = data_setY)
    save_h5.close()

def get_live_mfcc_setXY():
    data_setX = []
    data_setY = []
    while True:
        path = raw_input("live_mfcc:\n")
        # path = 'songs/live_songs/liveintexas.mp3'
        Y_data_item = AudioFile.open(path)
        if Y_data_item == None:
            break
        filename = os.path.basename(path).split(".")[0]
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
        save_h5 = h5py.File("live_songs_mfcc.h5","w")
        save_h5.create_dataset("X", data = data_setX)
        save_h5.create_dataset("Y", data = data_setY)
        save_h5.close()

def main():
    get_live_mfcc_setXY()

if __name__ == '__main__':
    main()