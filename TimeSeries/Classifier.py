from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from ElbowKnee_all_nSensors import *
from itertools import product
from DataParser import *
import os


def generateFeatureIndex() -> list[str]:
    color = ["g", "r", "b", "y"]
    sensor = ["0", "1", "2"]
    type = ["t", "r"]
    index = []
    for permutation in list(product(color, sensor, type)):
        index.append(permutation[0] + permutation[1] + permutation[2])
    print(index)
    return index

def confusionMatrix(expected, actual):
    test_matrix = confusion_matrix(expected, actual)
    disp = ConfusionMatrixDisplay(test_matrix)
    disp.plot()
    plt.show()

def normalize(
    features: list[list[float]],
) -> list[list[float]]:
    for i in range(len(features)):
        for j in range(0, len(features[i])//2, 2):
            features[i][j] = (features[i][j]) / (features[i][len(features[i])//4])
        for j in range(len(features[i])//2, len(features[i]), 2):
            features[i][j] = (features[i][j] - features[i][len(features[i])//2]) / (
                features[i][len(features[i])//4*3] - features[i][len(features[i])//2]
            )
    return features

def plotFeatures(features: list[float]):
    colors = ["orange", "green", "red"]
    for i in range(0, 6, 2):
        plt.plot(
            features[i::6],
            features[i + 1 :: 6],
            colors[i // 2],
            linestyle="-",
            marker=".",
            label=f"Sensor {i//2}",
        )
    plt.legend()
    plt.show()

class Classifier:
    def randomForest(
        self, 
        trainFeatures: list[list[float]],
        trainLabel: list[int],
        testFeatures: list[list[float]],
        testLabel: list[int],
    ) -> tuple[float]:
        x_train, x_test, y_train, y_test = train_test_split(
            trainFeatures, trainLabel, train_size=0.7, random_state=9999
        )
        self.model = RandomForestClassifier(
            random_state=9999,
        )
        self.model.fit(x_train, y_train)
        expected_train = y_test
        actual_train = self.model.predict(x_test)
        expected_test = testLabel
        actual_test = self.model.predict(testFeatures)
        acc = accuracy_score(expected_train, actual_train)
        accTest = accuracy_score(expected_test, actual_test)
        confusionMatrix(expected_test, actual_test)
        # print(actual_test),
        return acc, accTest

    def predict(self, features: list[float]):
        features = normalize(features)
        return self.model.predict(features)

