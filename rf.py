import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

xls = pd.ExcelFile('wristband_small.xlsx')
xlsTest = pd.ExcelFile('wristband_small_test.xlsx')
# nSheet = len(xls.sheet_names)
data = pd.DataFrame()
for name in xls.sheet_names:
    data = pd.concat([data, xls.parse(name, usecols=[0,3,4,5,6])], ignore_index=True)
# print(data)
dataTest = pd.DataFrame()
for name in xlsTest.sheet_names:
    dataTest = pd.concat([dataTest, xlsTest.parse(name, usecols=[0,3,4,5,6])], ignore_index=True)
# print(dataTest)
labels = data['gesture']
features = data[[0,1,2,3]]
labelsTest = dataTest['gesture']
featuresTest = dataTest[[0,1,2,3]]
"""
[0]: 0.328
[1]: 0.381
[2]: 0.381
[3]: 0.312
[0,1]: 0.513
[0,2]: 0.577
[0,3]: 0.566
[1,2]: 0.646
[1,3]: 0.661
[2,3]: 0.598
[0,1,2]: 0.709
[0,1,3]: 0.720
[0,2,3]: 0.709
[1,2,3]: 0.820
[0,1,2,3]: 0.804
"""

x_train, x_test, y_train, y_test = train_test_split(features,labels,train_size=0.7, random_state=9999)
# print(x_train)
model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=9999)
model.fit(x_train, y_train)

predictions = model.predict(x_test)
predictionsTest = model.predict(featuresTest)
print(predictionsTest)
# print(y_test)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(labelsTest, predictionsTest)
print('train: ', acc)
print('test: ', accTest)

