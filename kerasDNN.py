
import h5py, os
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Activation
from keras.models import Sequential, model_from_json
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def save_model(model, model_path='../dnn.json'):
    # serialize model to JSON
    model_json = model.to_json()
    with open(model_path, "w") as json_file:
        json_file.write(model_json)
    print("Successfully saved configs to disk.\n")
    return 0


def save_model_weights(model, model_weights_path='../dnn.h5'):
    # serialize weights to HDF5
    model.save_weights(model_weights_path)
    print("Successfully saved weights to disk.\n")
    return 0


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
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    return x_train, y_train, x_test, y_test


def main():
    # param setting
    INPUT_FEATURE_DIM = 32
    CLASS_NO = 78
    EPOCH = 1000
    min_epoch = 2
    BATCHSIZE = 1024
    load_model_flag = True
    FIRST_UNITS = 1024
    SECOND_UNITS = 1024
    THIRD_UNITS = 1024

    save_model_weights_path = 'dnn_weights.h5'
    save_model_path = 'dnn_model.json'
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
        model.fit(x_train, y_train, validation_split=0.2,
         nb_epoch=min_epoch, batch_size=BATCHSIZE,
                  callbacks=[callbacks])
        save_model_weights(model, save_model_weights_path)
    loss_and_metrics = model.evaluate(x_test, y_test,
     batch_size=BATCHSIZE)
    print loss_and_metrics
    # classes = model.predict(x_test, batch_size=BATCHSIZE)
    return 0


if __name__ == '__main__':
    # load_train_test_data()
    main()