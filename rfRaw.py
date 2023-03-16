from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import importDataRaw
modes=['gesture','length', 'raw data']
# mode = int(input("0: gesture, 1: length, 2: raw: ")) # 0 for gesture, 1 for length
mode = 0
trainFile = 'wristband/v4/1ADC/adi_old_board.xlsx'
train = importDataRaw.importData(trainFile,mode)
test = importDataRaw.importData('wristband/v4/1ADC/adi_old_board_test.xlsx',mode)
train.data.to_excel(r'data_cal/v4_old_board_train.xlsx')
test.data.to_excel(r'data_cal/v4_old_board_test.xlsx')
print(trainFile)

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=9999)
# rf
model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=9999)
model.fit(x_train, y_train)

predictions = model.predict(x_test)
predictionsTest = model.predict(test.features)
print('calibration with',modes[mode])
print(predictionsTest)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(test.labels, predictionsTest)
print('train: ', acc)
print('test: ', accTest)
print()