import pandas as pd
import DataParser
import matplotlib.pyplot as plt
from ElbowKnee_all_nSensors import *
from Classifier import *
from DataPartition import *


def findMaxMin(allData: list[pd.DataFrame]) -> list[tuple[float, float]]:
    maxx = [0, 0, 0]
    minn = [9999, 9999, 9999]
    for data in allData:
        tmpMax = data.max()
        tmpMin = data.min()
        for i in range(3):
            maxx[i] = max(maxx[i], tmpMax[str(i)])
            minn[i] = min(minn[i], tmpMin[str(i)])
    return list(zip(maxx, minn))


def findLinearTransform(
    maxmin1: list[tuple[float, float]], maxmin2: list[tuple[float, float]]
) -> list[tuple[float, float]]:  # find the transform to shift maxmin2 to maxmin1
    linearTransform = []
    for i in range(3):
        a = (maxmin1[i][0] - maxmin1[i][1]) / (
            maxmin2[i][0] - maxmin2[i][1]
        )  # y = ax + b
        b = (maxmin2[i][0] * maxmin1[i][1] - maxmin2[i][1] * maxmin1[i][0]) / (
            maxmin2[i][0] - maxmin2[i][1]
        )
        linearTransform.append((a, b))
    return linearTransform


def transformData(
    allData: list[pd.DataFrame], transformParameter: list[tuple[float, float]]
) -> list[pd.DataFrame]:
    for data in allData:
        for i in range(3):
            data[str(i)] = data[str(i)].map(
                lambda value: transformParameter[i][0] * value
                + transformParameter[i][1]
            )
    return allData


def plot(data: pd.DataFrame, title: str = ""):
    plt.figure()
    plt.ylim(500, 3200)
    for col in data.columns:
        if col == "gesture":
            plt.plot(
                [i * 10 for i in range(len(data[col]))],
                [i * 50 + 3000 for i in data[col]],
                label="gesture",
            )
            continue
        plt.plot(
            [i * 10 for i in range(len(data[col]))], data[col], label=f"Sensor {col}"
        )
    plt.ylabel("resistance(ohm)")
    plt.xlabel("time(ms)")
    plt.legend(loc="upper right")
    plt.title(title)
    plt.show()


def transfer(
    trainFile: list[pd.DataFrame],
    testFile: list[pd.DataFrame],
    calibrationFile: list[pd.DataFrame],
) -> list[pd.DataFrame]:
    linearTransform = findLinearTransform(
        findMaxMin(trainFile), findMaxMin(calibrationFile)
    )
    testFile = transformData(testFile, linearTransform)
    return testFile


if __name__ == "__main__":
    trainFileName = "band2_0115"
    testFileName = "band2_0126"
    trainFile, _ = DataParser.loadRawDataFile(trainFileName)
    plot(trainFile[0], "Training data")
    tmpFile, sheetNames = DataParser.loadRawDataFile(testFileName)
    testFile = []
    calibrationFile = []
    for i, sheet in enumerate(tmpFile):
        if "12" in sheetNames[i]:
            test, calibration = dataPartition(sheet, 0.7)
        else:
            calibration, test = dataPartition(sheet, 0.3)
        testFile.append(test)
        calibrationFile.append(calibration)
    plot(testFile[0], "Original testing data")
    testFile = transfer(trainFile, tmpFile, tmpFile)
    plot(testFile[0], "Transformed testing data")
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = normalize(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = normalize(testFeatures)

    print(len(trainFeatures), len(testFeatures))
    classifier = Classifier()
    acc, accTest = classifier.randomForest(
        trainFeatures,
        trainLabel,
        testFeatures,
        testLabel,
        # f"{trainFileName}_{testFileName}_4_gestures",
    )
    print(acc, accTest)
