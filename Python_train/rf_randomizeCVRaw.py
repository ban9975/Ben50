from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV
import numpy as np

import importDataRaw
modes=['gesture','length']
mode = int(input("0: gesture, 1: length: ")) # 0 for gesture, 1 for length
train = importDataRaw.importData('wristband/v4/adi_raw.xlsx',mode)
test = importDataRaw.importData('wristband/v4/adi_raw_test.xlsx',mode)

x_train, x_test, y_train, y_test = train_test_split(train.features,train.labels,train_size=0.7, random_state=9999)
# print(x_train)
model = RandomForestClassifier(random_state=9999)
# model.fit(x_train, y_train)
n_estimators = [int(x) for x in np.linspace(start=100, stop=2000, num=10)]
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