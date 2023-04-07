from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import importDataRaw
modes=['gesture','length', 'raw data', 'first round', 'multi']
mode = int(input("0: gesture, 1: length, 2: raw, 3: first round, 4: all : ")) # 0 for gesture, 1 for length
# mode = 0
trainFile = 'wristband/v7/adi_v3_1ADC.xlsx'
testFile = 'wristband/v7/adi_v3_1ADC_test.xlsx'
train = importDataRaw.importData(trainFile,mode)
test = importDataRaw.importData(testFile,mode)
if mode == 2:
    train.data.to_excel(r'data_cal/v7/adi_v3_1ADC_cal_raw_train.xlsx')
    test.data.to_excel(r'data_cal/v7/adi_v3_1ADC_cal_raw_test.xlsx')
print(trainFile)

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=9999)
# x_train=train.features
# y_train=train.labels
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
print()
# # Visualize a tree
# estimator = model.estimators_[5]
# from sklearn.tree import export_graphviz
# # Export as dot file
# dot = export_graphviz(estimator, out_file='adi_v3_1ADC_round2_tree.dot', 
#                 feature_names = ['0','1','2','3'],
#                 class_names = ['down','up','thumb','little finger','stretch','fist','rest'],
#                 rounded = True, proportion = False, 
#                 precision = 2, filled = True)
# import pydot
# (graph,) = pydot.graph_from_dot_file('adi_v3_1ADC_round2_tree.dot')
# graph.write_png('adi_v3_1ADC_round2_tree.png')