from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

import importData

train = importData.importData('wristband/v3/small_adi_len.xlsx')
test = importData.importData('wristband/v3/small_adi_len_test.xlsx')

# train.res2len()
# test.res2len()

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=9999)
# rf
model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=9999)
# knn
# model = KNeighborsClassifier()
# naive bayes
# model = GaussianNB()
# svm
# model = SVC()
model.fit(x_train, y_train)

predictions = model.predict(x_test)
predictionsTest = model.predict(test.features)
print(predictionsTest)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(test.labels, predictionsTest)
print('train: ', acc)
print('test: ', accTest)