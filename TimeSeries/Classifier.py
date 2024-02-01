from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from ElbowKnee_all import *
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


def normalize(
    features: list[list[float]], mode: str = "no", flat: list[float] = []
) -> list[list[float]]:
    for i in range(len(features)):
        for j in range(0, 12, 2):
            features[i][j] = (features[i][j]) / (features[i][10])
        for j in range(12, 24, 2):
            features[i][j] = (features[i][j] - features[i][12]) / (
                features[i][22] - features[i][12]
            )
        if mode == "no":
            continue
        if mode == "flat":
            for j in range(3):
                for k in range(j * 2 + 1, len(features[i]), 6):
                    features[i][k] = features[i][k] / flat[j]
        elif mode == "greenpoint":
            for j in range(3):
                green = features[i][j * 2 + 1]
                for k in range(j * 2 + 1, len(features[i]), 6):
                    features[i][k] = features[i][k] / green
    return features


def calculateFlat(fileName: str) -> list[float]:
    flat = []
    xls = pd.ExcelFile(
        os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
    )
    sheet = xls.parse(xls.sheet_names[0])
    for colName in sheet.columns:
        if colName != "gesture":
            flat.append(sum(sheet[colName]) / len(sheet[colName]))
    return flat


def randomForest(
    trainFeatures: list[list[float]],
    trainLabel: list[int],
    testFeatures: list[list[float]],
    testLabel: list[int],
) -> tuple[float]:
    x_train, x_test, y_train, y_test = train_test_split(
        trainFeatures, trainLabel, train_size=0.7, random_state=9999
    )
    model = RandomForestClassifier(
        random_state=9999,
    )
    model.fit(x_train, y_train)
    expected_train = y_test
    actual_train = model.predict(x_test)
    expected_test = testLabel
    actual_test = model.predict(testFeatures)
    acc = accuracy_score(expected_train, actual_train)
    accTest = accuracy_score(expected_test, actual_test)
    print(len(actual_test))
    confusionMatrix(expected_test, actual_test)
    print(actual_test)
    return acc, accTest


def confusionMatrix(expected, actual):
    test_matrix = confusion_matrix(expected, actual)
    disp = ConfusionMatrixDisplay(test_matrix)
    disp.plot()
    plt.show()


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


if __name__ == "__main__":
    trainFeatures = []
    trainLabel = []
    testFeatures = []
    testLabel = []
    trainFile = [("band2_0115", "band2_flat")]
    testFile = [("band1_0126", "band1_flat")]
    # trainFeatures, trainLabel = loadEKFolder(os.path.join(os.getcwd(), "Excel_data/v8/Time_series/rick/0127"))
    # trainFeatures = normalize(trainFeatures, 'greenpoint', calculateFlat('band4_flat'))
    for f in trainFile:
        allData = loadRawDataFile(f[0])
        features, label = fullEKProcessing(allData)
        features = normalize(features, "flat", calculateFlat(f[1]))
        trainFeatures += features
        trainLabel += label
    print(len(trainFeatures))
    for f in testFile:
        allData = loadRawDataFile(f[0])
        features, label = fullEKProcessing(allData)
        features = normalize(features, "flat", calculateFlat(f[1]))
        testFeatures += features
        testLabel += label
    # testFeatures, testLabel = loadEKFolder(os.path.join(os.getcwd(), "Excel_data/v8/Time_series/rick/0127"))
    # testFeatures = normalize(testFeatures, 'greenpoint', calculateFlat('band4_flat'))
    acc, accTest = randomForest(trainFeatures, trainLabel, testFeatures, testLabel)
    print(acc, accTest)
