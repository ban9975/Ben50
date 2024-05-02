from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from ElbowKnee_all_nSensors import *
from itertools import product
from DataParser import *
import joblib


def generateFeatureIndex() -> list[str]:
    color = ["g", "r", "b", "y"]
    sensor = ["0", "1", "2"]
    type = ["t", "r"]
    index = []
    for permutation in list(product(color, sensor, type)):
        index.append(permutation[0] + permutation[1] + permutation[2])
    return index


def normalize(
    features: list[list[float]],
) -> list[list[float]]:
    for i in range(len(features)):
        r0t = features[i][len(features[i]) // 4]
        for j in range(0, len(features[i]) // 2, 2):
            features[i][j] = (features[i][j]) / r0t
        byRange = (
            features[i][len(features[i]) // 4 * 3] - features[i][len(features[i]) // 2]
        )
        b0t = features[i][len(features[i]) // 2]
        for j in range(len(features[i]) // 2, len(features[i]), 2):
            features[i][j] = (features[i][j] - b0t) / byRange
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
        self.expected_train = y_test
        self.actual_train = self.model.predict(x_test)
        self.expected_test = testLabel
        self.actual_test = self.model.predict(testFeatures)
        acc = accuracy_score(self.expected_train, self.actual_train)
        accTest = accuracy_score(self.expected_test, self.actual_test)
        return acc, accTest

    def predict(self, features: list[float]):
        features = normalize(features)
        return self.model.predict(features)

    def saveModel(self, path: str):
        joblib.dump(self.model, os.path.join(os.getcwd(), "Model", path))

    def loadModel(self, path: str):
        self.model = joblib.load(os.path.join(os.getcwd(), "Model", path))

    def confusionMatrix(self, expected, actual, title="", path=""):
        test_matrix = confusion_matrix(expected, actual)
        disp = ConfusionMatrixDisplay(test_matrix)
        disp.plot()
        plt.title(title)
        if path != "":
            plt.savefig(path)
            plt.close()
        else:
            plt.show()
