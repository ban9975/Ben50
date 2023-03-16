from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import importDataRaw
modes=['gesture','length']
mode = int(input("0: gesture, 1: length: ")) # 0 for gesture, 1 for length
train = importDataRaw.importData('wristband/v4/adi_raw.xlsx',mode)
test = importDataRaw.importData('wristband/v4/adi_raw_test.xlsx',mode)

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=9999)
# rf
model = RandomForestClassifier(n_estimators=944, min_samples_split=2,min_samples_leaf=1,max_features='sqrt',max_depth=20, bootstrap=True,random_state=9999)
model.fit(x_train, y_train)

predictions = model.predict(x_test)
predictionsTest = model.predict(test.features)
print('calibration with',modes[mode])
print(predictionsTest)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(test.labels, predictionsTest)
print('train: ', acc)
print('test: ', accTest)