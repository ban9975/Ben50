import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV
import numpy as np

xls = pd.ExcelFile('wristband_small_random.xlsx')
xlsTest = pd.ExcelFile('wristband_small_test.xlsx')
nSheet = len(xls.sheet_names)
data = pd.DataFrame()
# i=0
# while i < nSheet:
#     rest = xls.parse(i,usecols=[0,3,4,5,6])
#     avg = [0,0,0,0]
#     for j in range(rest.shape[0]):
#         for k in range(4):
#             avg[k]+=rest[k][j]
#     for k in range(4):
#         avg[k]/=rest.shape[0]
#     # print(avg)
#     while i%7!=6:
#         i+=1
#         tmp=xls.parse(i, usecols=[0,3,4,5,6])
#         for j in range(tmp.shape[0]):
#             for k in range(4):
#                 tmp[k][j]/=avg[k]
#         data = pd.concat([data, tmp], ignore_index=True)
#     for j in range(rest.shape[0]):
#         for k in range(4):
#             rest[k][j]/=avg[k]
#     data = pd.concat([data, rest], ignore_index=True)
#     i+=1

i=0
while i < nSheet:
    rest = xls.parse(i,usecols=[0,3,4,5,6])
    avg = [0,0,0,0]
    for j in range(rest.shape[0]):
        for k in range(4):
            avg[k]+=rest[k][j]
    for k in range(4):
        avg[k]/=rest.shape[0]
    # print(avg)
    i+=1
    tmp=xls.parse(i, usecols=[0,3,4,5,6])
    for j in range(tmp.shape[0]):
        for k in range(4):
            tmp[k][j]/=avg[k]
    data = pd.concat([data, tmp], ignore_index=True)
    i+=1
# print(data)

dataTest = pd.DataFrame()
rest = xlsTest.parse(0,usecols=[0,3,4,5,6])
avg = [0,0,0,0]
for j in range(rest.shape[0]):
    for k in range(4):
        avg[k]+=rest[k][j]
for k in range(4):
    avg[k]/=rest.shape[0]
tmp=xlsTest.parse(1, usecols=[0,3,4,5,6])
for j in range(tmp.shape[0]):
    for k in range(4):
        tmp[k][j]/=avg[k]
dataTest = tmp
# print(dataTest)
labels = data['gesture']
features = data[[0,1,2,3]]
labelsTest = dataTest['gesture']
featuresTest = dataTest[[0,1,2,3]]

x_train, x_test, y_train, y_test = train_test_split(features,labels,train_size=0.7, random_state=9999)
# print(x_train)
model = RandomForestClassifier(random_state=9999)
# model.fit(x_train, y_train)
n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators, 'max_features': max_features,
               'max_depth': max_depth, 'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf, 'bootstrap': bootstrap}
random_grid
rf_random = RandomizedSearchCV(estimator = model, param_distributions=random_grid,
                              n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)

rf_random.fit(x_train,y_train)
print(rf_random.best_params_)

# predictions = model.predict(x_test)
# predictionsTest = model.predict(featuresTest)
# acc = metrics.accuracy_score(y_test, predictions)
# accTest = metrics.accuracy_score(labelsTest, predictionsTest)
# print('train: ', acc)
# print('test: ', accTest)


# # Visualize a tree
# estimator = model.estimators_[5]
# from sklearn.tree import export_graphviz
# # Export as dot file
# dot = export_graphviz(estimator, out_file='tree.dot', 
#                 feature_names = ['0','1','2','3'],
#                 class_names = ['down','up','thumb','little finger','stretch','fist','rest'],
#                 rounded = True, proportion = False, 
#                 precision = 2, filled = True)
