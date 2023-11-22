from sklearn.model_selection import train_test_split
from sklearn import metrics
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.optimizers import SGD, Adam, Adadelta, RMSprop
import keras.backend as K
import importDataRaw
from keras.utils.np_utils import to_categorical
import numpy as np
import tensorflow as tf
import random
seed=9999
np.random.seed(seed)
random.seed(seed)
tf.random.set_seed(seed)
modes=['gesture','length', 'raw data', 'first','ges+first']
mode = int(input("0: gesture, 1: length, 2: raw, 3: first: ")) # 0 for gesture, 1 for length
# mode = 0
trainFile = 'wristband/v6/adi_v3_1ADC.xlsx'
testFile = 'wristband/v6/adi_v3_1ADC_test.xlsx'
train = importDataRaw.importData(trainFile,mode)
test = importDataRaw.importData(testFile,mode)
# if mode == 0:
#     train.data.to_excel(r'data_cal/v4Plus/adi_v3_1ADC_round2_cal_ges_train.xlsx')
#     test.data.to_excel(r'data_cal/v4Plus/adi_v3_1ADC_round2_cal_ges_test.xlsx')
print(trainFile)

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=seed)
y_train=to_categorical(y_train)
y_test_c=to_categorical(y_test)
model = Sequential()
model.add(Dense(32, input_shape = (4,), activation = "relu"))
model.add(Dense(128, activation = "relu"))
model.add(Dense(64, activation = "relu"))
model.add(Dropout(0.2))
model.add(Dense(7, activation = "softmax"))
model.compile(Adam(lr = 0.0001), "categorical_crossentropy", metrics = ["accuracy"])
model.summary()
model.fit(x_train, y_train, verbose=1, epochs=300,batch_size=28,validation_data=(x_test,y_test_c))
predictions = np.argmax(model.predict(x_test), axis=1)
predictionsTest = np.argmax(model.predict(test.features), axis=1)
print('calibration with',modes[mode])
# print(predictions)
print(predictionsTest)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(test.labels, predictionsTest)

print('train: ', acc)
print('test: ', accTest)
print()