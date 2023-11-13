import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

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
# print(predictionsTest)
# print(y_test)
acc = metrics.accuracy_score(y_test, predictions)
accTest = metrics.accuracy_score(labelsTest, predictionsTest)
print('train: ', acc)
print('test: ', accTest)


# Visualize a tree
estimator = model.estimators_[5]
from sklearn.tree import export_graphviz
# Export as dot file
dot = export_graphviz(estimator, out_file='tree.dot', 
                feature_names = ['0','1','2','3'],
                class_names = ['down','up','thumb','little finger','stretch','fist','rest'],
                rounded = True, proportion = False, 
                precision = 2, filled = True)

# import graphviz
# graph = graphviz.Source(dot, format='png')
# graph.render('tree')

# # Convert to png using system command (requires Graphviz)
# from subprocess import call
# call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'], shell=True)

# import pydot
# (graph,) = pydot.graph_from_dot_file('tree.dot')
# graph.write_png('tree.png')