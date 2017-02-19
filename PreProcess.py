from pydub import AudioSegment
import os
# 16KHz mono .wav

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

formatAllAudio()