
import h5py, os, time
import numpy
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Activation, LSTM
from keras.models import Sequential, model_from_json
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def save_model(model, model_path='../4th_dnn.json'):
    # serialize model to JSON
    model_json = model.to_json()
    with open(model_path, "w") as json_file:
        json_file.write(model_json)
    print("Successfully saved configs to disk.\n")
    return 0


def save_model_weights(model, model_weights_path='../4th_dnn.h5'):
    # serialize weights to HDF5
    model.save_weights(model_weights_path)
    print("Successfully saved weights to disk.\n")
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return 0

def vector2matrix(verctorlist=[]):
    matrix=[]
    for vector in verctorlist:
        matrix.append(vector)
    return matrix

def load_model(model_path):
    # load json and create model
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    print("Successfully loaded configs to disk.\n")
    return loaded_model

def load_model_weights(weights_path, model):
    # load weights into  model
    model.load_weights(weights_path)
    print("Successfully loaded weights from disk.\n")
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return model

def load_train_test_data(path='studio_songs_mfcc.h5'):
    hfile = h5py.File(path, 'r')
    X = hfile['X'][:]
    Y = hfile['Y'][:]

    encoder = LabelEncoder()
    encoder.fit(Y)
    # print len(X[1])
    # print Y[:10]
    Y = encoder.transform(Y)
    # print Y[:10]
    Y = to_categorical(Y)
    # print Y[:10]
    # print len(Y[1])
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    return x_train, y_train, x_test, y_test

def load_train_test_data_for_lstm(path='studio_songs_mfcc.h5', time_step=10):
    hfile = h5py.File(path, 'r')
    X = hfile['X'][:]
    Y = hfile['Y'][:]

    finalX = []
    finalY = []
    for item in range(0, len(X) - time_step, time_step):
        temp_verctorlist = []
        temp_y = []
        temp_verctorlist.extend(X[item:item + time_step])
        temp_y.extend(Y[item:item + time_step])
        value = temp_y[0]
        append_flag = True
        # print value
        for i_y in temp_y:
            if i_y != value:
                append_flag = False
                break
        if append_flag:
            matrix = []
            for vector in temp_verctorlist:
                matrix.append(vector)
            finalX.append(matrix)
            finalY.append(value)
    nameY = set(finalY)
    encoder = LabelEncoder()
    encoder.fit(finalY)
    finalY = encoder.transform(finalY)
    temp_num = finalY[0]
    numY = [finalY[0]]
    for i in range(len(finalY)):
        if temp_num != finalY[i]:
            numY.append(finalY[i])
            temp_num = finalY[i]
    finalY = to_categorical(finalY)
    file = open("name2num.txt", 'w')
    nameY = list(nameY)
    for i in range(len(nameY)):
        file.write(str(numY[i]) + '-->' + nameY[i] + '\n')
    file.close()
    x_train, x_test, y_train, y_test = train_test_split(finalX, finalY, test_size=0.2, random_state=42)

    return x_train, y_train, x_test, y_test

def load_songs_lstm(path='SetList_mfcc.h5', time_step=10):
    hfile = h5py.File(path, 'r')
    X = hfile['X'][:]
    Y = hfile['Y'][:]
    finalX = []
    finalY = []
    for item in range(0, len(X) - time_step, time_step):
        temp_verctorlist = []
        temp_y = []
        temp_verctorlist.extend(X[item:item + time_step])
        temp_y.extend(Y[item:item + time_step])
        value = temp_y[0]
        append_flag = True
        # print value
        for i_y in temp_y:
            if i_y != value:
                append_flag = False
                break
        if append_flag:
            matrix = []
            for vector in temp_verctorlist:
                matrix.append(vector)
            finalX.append(matrix)
            finalY.append(value)
    resultX = []
    for i in range(len(finalX)):
        resultX.append(finalX[i])
    return resultX

def dnn_model():
    # param setting
    INPUT_FEATURE_DIM = 32
    CLASS_NO = 78
    EPOCH = 1000
    min_epoch = 10
    BATCHSIZE = 1024
    load_model_flag = True
    FIRST_UNITS = 1024
    SECOND_UNITS = 1024
    THIRD_UNITS = 1024
    FOURTH_UNITS = 1024

    save_model_weights_path = '4th_dnn_weights.h5'
    save_model_path = '4th_dnn_model.json'
    x_train, y_train, x_test, y_test = load_train_test_data()

    if load_model_flag and os.path.isfile(save_model_path):
        model = load_model(save_model_path)
    else:

        # build model
        model = Sequential()

        model.add(Dense(FIRST_UNITS, input_dim=INPUT_FEATURE_DIM))
        model.add(Activation('relu'))

        model.add(Dense(SECOND_UNITS))
        model.add(Activation('relu'))

        model.add(Dense(THIRD_UNITS))
        model.add(Activation('relu'))

        model.add(Dense(FOURTH_UNITS))
        model.add(Activation('relu'))

        model.add(Dense(CLASS_NO))
        model.add(Activation('softmax'))

        save_model(model, save_model_path)

    # load or build over model

    model.compile(loss='categorical_crossentropy',
     optimizer='sgd', metrics=['accuracy'])

    callbacks = EarlyStopping(monitor='val_loss',
     patience=4, min_delta=0.02, verbose=0, mode='auto')
    if os.path.isfile(save_model_weights_path):
        model = load_model_weights(save_model_weights_path, model)
    for fit in range(EPOCH):
        loss_and_metrics = model.evaluate(x_test, y_test,
                                          batch_size=BATCHSIZE)
        print loss_and_metrics
        model.fit(x_train, y_train, validation_split=0.1,
         nb_epoch=min_epoch, batch_size=BATCHSIZE,
                  callbacks=[callbacks])
        save_model_weights(model, save_model_weights_path)
    loss_and_metrics = model.evaluate(x_test, y_test,
     batch_size=BATCHSIZE)
    print loss_and_metrics
    # classes = model.predict(x_test, batch_size=BATCHSIZE)
    return 0

def test_lstm():
    INPUT_FEATURE_DIM = 32
    time_step = 10
    CLASS_NO = 78
    BATCHSIZE = 100
    save_model_weights_path = 'lstm_weights.h5'
    model = Sequential()
    model.add(LSTM(256, return_sequences=True, batch_input_shape=(BATCHSIZE, time_step, INPUT_FEATURE_DIM)))
    model.add(LSTM(64))
    model.add(Dense(CLASS_NO))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    if os.path.isfile(save_model_weights_path):
        model = load_model_weights(save_model_weights_path, model)
    print 'testing...'
    datasetX = load_songs_lstm(path = 'live_songs_mfcc.h5')
    datasetX = datasetX[:len(datasetX) / BATCHSIZE * BATCHSIZE]
    output = model.predict_classes(datasetX, batch_size=BATCHSIZE)
    file = open('output.txt', 'w')
    count = 0
    for i in output:
        file.write(str(i) + ' ')
        count += 1
        if count == 20:
            file.write('\n')
            count = 0
    output2 = model.predict(datasetX, batch_size=BATCHSIZE)
    file2 = open('output2.txt', 'w')
    count = 0
    for i in output2:
        file2.write(str(i) + ' ')
        count += 1
        if count == 20:
            file2.write('\n')
            count = 0
    print "\nDone!"

def lstm_model():
    # parm
    INPUT_FEATURE_DIM = 32
    time_step = 10
    CLASS_NO = 78
    EPOCH = 1000
    min_epoch = 2
    BATCHSIZE = 100
    save_model_weights_path = 'lstm_weights.h5'
    save_model_path = 'lstm_model.json'
    save_epoch_time = 'lstm_epoch.txt'
    # data
    print 'data...'
    x_train, y_train, x_test, y_test = load_train_test_data_for_lstm(time_step=time_step)
    x_train = x_train[:len(x_train)/BATCHSIZE * BATCHSIZE]
    y_train = y_train[:len(y_train) / BATCHSIZE * BATCHSIZE]
    x_test = x_test[:len(x_test) / BATCHSIZE * BATCHSIZE]
    y_test = y_test[:len(y_test) / BATCHSIZE * BATCHSIZE]
    model = Sequential()
    model.add(LSTM(256, return_sequences=True, batch_input_shape=(BATCHSIZE, time_step, INPUT_FEATURE_DIM)))
    model.add(LSTM(64))
    model.add(Dense(CLASS_NO))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    callbacks = EarlyStopping(monitor='val_loss', patience=2, min_delta=0.02, verbose=0, mode='auto')
    if os.path.isfile(save_model_weights_path):
        model = load_model_weights(save_model_weights_path, model)

    print 'testing...'
    datasetX = load_first_song_lstm()
    datasetX = datasetX[:len(x_test) / BATCHSIZE * BATCHSIZE]
    print model.predict_classes(datasetX, batch_size=BATCHSIZE)

    print 'train model ...'
    # for fit in range(EPOCH):
        # model.fit(x_train, y_train, validation_split=0.2, nb_epoch=min_epoch, batch_size=BATCHSIZE,
        #           callbacks=[callbacks])
    model.fit(x_train, y_train, nb_epoch=EPOCH, batch_size=BATCHSIZE,
              callbacks=[callbacks], validation_data=([x_test, y_test]),verbose=1)
    save_model_weights(model, save_model_weights_path)

    # epoch_time += min_epoch
    # open(save_epoch_time, "w").write(str(epoch_time))
    # print "EPOCH: " + str(epoch_time) + " times"

    save_model(model, save_model_path)
    # loss_and_metrics = model.evaluate(x_test, y_test, batch_size=BATCHSIZE)
    # print loss_and_metrics
    # classes = model.predict(x_test, batch_size=BATCHSIZE)

    return model

def main():
    # lstm_model()
    # dnn_model()
    # test_lstm()
    load_train_test_data_for_lstm()

if __name__ == '__main__':
    main()