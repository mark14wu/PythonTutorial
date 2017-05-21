from pydub import AudioSegment
import os
def importAudio_MP3(path="Linkin_Park_Live_in_Texas_mp3"):
    # songs = AudioSegment.empty()
    i = 0
    for root, dirs, files in os.walk(path):
        for audioName in files:
            audioPath = os.path.join(root, audioName)
            if ".mp3" not in audioPath:
                continue
            audioName = audioName.split(".")[0]
            NewName = audioName.split(" - ")[1]
            NewName = NewName.split("(")[0]
            NewName = NewName[:-1] + ".wav"
            print NewName
            Newroot = os.path.join(root, "output_mono")
            if not os.path.exists(Newroot):
                os.mkdir(Newroot)
            audioNewPath = os.path.join(Newroot, NewName)
            audio = AudioSegment.from_mp3(audioPath)
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(16000)
            audio.export(audioNewPath, "wav")

        # songs.export(os.path.join(root,"live.wav"), format="wav")

importAudio_MP3()