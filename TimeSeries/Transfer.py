import pandas as pd
import DataParser
import matplotlib.pyplot as plt
from ElbowKnee_all import *
from Classifier import *


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


def plot(data: pd.DataFrame):
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
    plt.show()


if __name__ == "__main__":
    trainFile = DataParser.loadRawDataFile("band2_0115")
    testFile = DataParser.loadRawDataFile("band4_0127")
    linearTransform = findLinearTransform(findMaxMin(trainFile), findMaxMin(testFile))
    testFile = transformData(testFile, linearTransform)
    trainFeatures, trainLabel = fullEKProcessing(trainFile)
    trainFeatures = normalize(trainFeatures)
    print(len(trainFeatures))
    testFeatures, testLabel = fullEKProcessing(testFile)
    testFeatures = normalize(testFeatures)
    acc, accTest = randomForest(trainFeatures, trainLabel, testFeatures, testLabel)
    print(acc, accTest)
