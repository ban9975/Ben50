from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from datetime import datetime
import importDataRaw
import joblib
from BTController import bt
import matplotlib.pyplot as plt
import os

modes = ["gesture", "length", "raw data", "first round", "avg", "norm"]
nSensor = 3
caliCnt = 15
# gestures = ["down", "up", "paper", "rock", "thumb", "little finger", "rest"]
# gestures = ["down", "up", "paper", "rock"]
gestures = ["down", "up", "open", "close"]


class Rf:
    def prepareData(self, trainFile, testFile, mode):
        self.mode = mode
        self.train = importDataRaw.importData(trainFile, mode)
        self.test = importDataRaw.importData(testFile, mode)

    def runRf(self):
        x_train, x_test, y_train, y_test = train_test_split(
            self.train.features, self.train.labels, train_size=0.7, random_state=9999
        )
        self.model = RandomForestClassifier(
            n_estimators=944,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features="sqrt",
            max_depth=20,
            bootstrap=True,
            random_state=9999,
        )
        self.model.fit(x_train, y_train)
        self.expected_train = y_test
        self.actual_train = self.model.predict(x_test)
        self.expected_test = self.test.labels
        self.actual_test = self.model.predict(self.test.features)
        acc = accuracy_score(self.expected_train, self.actual_train)
        accTest = accuracy_score(self.expected_test, self.actual_test)
        result = f"train: {acc}\ntest: {accTest} \n{self.actual_test}"
        return result

    def saveModel(self, path):
        joblib.dump(self.model, f'{path.split(".")[0]}_{modes[self.mode]}.joblib')
    
    def confusionMatrix(self, path):
        train_matrix = confusion_matrix(self.expected_train, self.actual_train)
        disp = ConfusionMatrixDisplay(train_matrix)
        disp.plot()
        plt.title(f'{os.path.split(path)[1]} {modes[self.mode]}_train')
        plt.savefig(f'{path}_{modes[self.mode]}_cm_train.png')
        test_matrix = confusion_matrix(self.expected_test, self.actual_test)
        disp = ConfusionMatrixDisplay(test_matrix)
        disp.plot()
        plt.title(f'{os.path.split(path)[1]} {modes[self.mode]}_test')
        plt.savefig(f'{path}_{modes[self.mode]}_cm_test.png')        
        

    def predictSetup(self, path):
        self.model = joblib.load(path)
        self.cali = [0 for i in range(nSensor)]
    
    def _readData(self):
        data = [[] for j in range(nSensor)]
        for j in range(20):
            for k in range(nSensor):
                btIn = float(bt.read())
                while btIn == 0:
                    print(0)
                    btIn = float(bt.read())
                data[k].append(btIn)
        return data   

    def calibration(self):
        bt.write("1")
        data = self._readData()
        avg = [sum(data[k]) for k in range(nSensor)]
        for k in range(nSensor):
            avg[k] = 1000 * avg[k] / 20 * 3 / (5000 - avg[k] / 20 * 3)
            self.cali[k] += avg[k] / caliCnt
        return f"{avg}"

    def collect(self, worksheet, row, start):
        bt.write("1")
        worksheet.cell(row=row, column=2, value=str(datetime.now()-start))
        data = self._readData()
        avg = [sum(data[k]) for k in range(nSensor)]
        for k in range(nSensor):
            avg[k] = 1000 * avg[k] / 20 * 3 / (5000 - avg[k] / 20 * 3)
            for j in range(20):
                worksheet.cell(row=row, column=k*20+j+4, value=round(1000 * data[k][j] * 3 / (5000 - data[k][j] * 3), 2))
        worksheet.cell(row=row, column=3, value=str(datetime.now()-start))
        return f"{avg}"

    def predict(self):
        bt.write("1")
        data = self._readData()
        avg = [sum(data[k]) for k in range(nSensor)]
        for k in range(nSensor):
            avg[k] = 1000 * avg[k] / 20 * 3 / (5000 - avg[k] / 20 * 3)
        result = self.model.predict([[a - c for a, c in zip(avg, self.cali)]])[0]
        return gestures[result], f"{avg}"
