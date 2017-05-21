import warnings
import json
import os
from tqdm import tqdm
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer

from pydub import AudioSegment

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

def split_concert_to_time_series_files(concert_path, temp_directory_name):
    print "importing concert files..."
    song = AudioSegment.from_file(concert_path, concert_path.split('.')[-1])
    dur_song = song.duration_seconds * 1000
    frame_length = 5 * 1000 # each frame is 5 seconds
    part = int(dur_song / frame_length)

    song_name = os.path.basename(concert_path).split()[0]
    directory_name = temp_directory_name + song_name
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    print "framing..."
    for i in tqdm(range(part)):
        part_song = song[i * frame_length : (i+1) * frame_length]
        part_name = directory_name + '/' + str(i) + '.wav'
        if os.path.isfile(part_name):
            continue
        part_song.export(part_name, 'wav')

    return directory_name

def recognize_each_concert_part(concert_parts_dir, djv):
    print "recognizing..."
    part_name_list = {}
    for root, dirs, files in os.walk(concert_parts_dir):
        for audioName in tqdm(files):
            audioPath = os.path.join(root, audioName)
            part_NO = os.path.basename(audioPath).split('.')[0]
            part_predict_name = djv.recognize(FileRecognizer, audioPath)
            try:
                part_name_list[str(part_NO)] = part_predict_name['song_name']
            except:
                continue
    return part_name_list

def change_dic_2_list(dic):
    list_dic = []
    num_list = []
    max = 0
    for item in dic:
        num_list.append(int(item))
    num_list.sort()
    print num_list
    for i in num_list:
        list_dic.append(dic[str(i)])
    return list_dic

def combine_redundant(name_list):
    final_list = []
    count = -1
    for item in name_list:
        if count == -1:
            final_list.append(item)
            count += 1

        elif not final_list[count] == item:
            final_list.append(item)
            count += 1

    return final_list

if __name__ == '__main__':
    temp_directory_name = 'temp_concert_parts/'
    djv = Dejavu(config)
    # Fingerprint all the mp3's in the directory we give it
    djv.fingerprint_directory("/Users/tom55wu/Desktop/python/PythonTutorial/songs/studio_songs/linkin_park", [".mp3"])
    directory_name = split_concert_to_time_series_files("./songs/live_songs/setList.mp4", temp_directory_name)
    dictionary = recognize_each_concert_part(directory_name, djv)
    dic_list = change_dic_2_list(dictionary)
    temp_file = open('tempresult.txt', 'w')
    for item in dic_list:
        temp_file.write(str(item) + '\n')
    temp_file.close()
    result_list = combine_redundant(dic_list)
    file = open('result.txt', 'w')
    for item in result_list:
        file.write(str(item) + '\n')
    file.close()
