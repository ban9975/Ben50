from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import importDataRaw
mode = 1
train = importDataRaw.importData('wristband/rawT.xlsx',mode)
test = importDataRaw.importData('wristband/rawTTest.xlsx',mode)

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=9999)
# rf
model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=9999)
model.fit(x_train, y_train)

predictions = model.predict(x_test)
predictionsTest = model.predict(test.features)
print(predictionsTest)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(test.labels, predictionsTest)
print('train: ', acc)
print('test: ', accTest)