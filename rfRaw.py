from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import importDataRaw
modes=['gesture','length', 'raw data']
<<<<<<< HEAD
# mode = int(input("0: gesture, 1: length, 2: raw: ")) # 0 for gesture, 1 for length
mode = 0
trainFile = 'wristband/v4Plus/adi_v2_1ADC.xlsx'
train = importDataRaw.importData(trainFile,mode)
test = importDataRaw.importData('wristband/v4Plus/adi_v2_1ADC_test.xlsx',mode)
train.data.to_excel(r'data_cal/v4Plus_v2_1ADC_train.xlsx')
test.data.to_excel(r'data_cal/v4Plus_v2_1ADC_test.xlsx')
=======
mode = int(input("0: gesture, 1: length, 2: raw: ")) # 0 for gesture, 1 for length
# mode = 0
trainFile = 'wristband/v4Plus/adi_v2_1ADC_sticky_real.xlsx'
train = importDataRaw.importData(trainFile,mode)
test = importDataRaw.importData('wristband/v4Plus/adi_v2_1ADC_sticky_real_test.xlsx',mode)
if mode == 0:   
    train.data.to_excel(r'data_cal/adi_v2_1ADC_sticky_real_caltrain.xlsx')
    test.data.to_excel(r'data_cal/adi_v2_1ADC_sticky_real_caltest.xlsx')
>>>>>>> 0511199968399dfcfd7e4f7825d084b2acd92c5f
print(trainFile)

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
print()