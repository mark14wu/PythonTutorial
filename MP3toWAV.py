import os
from tqdm import tqdm
from pydub import AudioSegment
def importAudio_MP3(path = raw_input("please input path:\n")):
    # songs = AudioSegment.empty()
    i = 0
    for root, dirs, files in os.walk(path):
        singer = root.split("/")[-1]
        NameList = open(singer + "_Songs.txt", "w")
        for audioName in tqdm(files):
            audioPath = os.path.join(root, audioName)
            if ".mp3" not in audioPath:
                continue
            audioName = audioName.split(".")[0]
            NewName = audioName.split(" - ")[1]
            # NewName = NewName.split("(")[0]
            NewName = NewName + "_mono" + ".wav"
            # print NewName
            Newroot = os.path.join(root, "output_mono")
            if not os.path.exists(Newroot):
                os.mkdir(Newroot)
            audioNewPath = os.path.join(Newroot, NewName)
            NameList.write(audioNewPath)
            NameList.write("\n")
            if os.path.exists(audioNewPath):
                continue
            audio = AudioSegment.from_mp3(audioPath)
            audio = audio.set_channels(1)
            # audio = audio.set_frame_rate(16000)
            audio.export(audioNewPath, "wav")
        NameList.close()

importAudio_MP3()