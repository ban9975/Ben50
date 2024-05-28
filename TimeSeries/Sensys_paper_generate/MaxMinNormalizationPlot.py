import pandas as pd
import DataParser
import matplotlib.pyplot as plt
from ElbowKnee_all_nSensors import *
from Classifier import *
from DataPartition import *
from Calibration import *


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
    # plt.title(title)
    plt.show()


if __name__ == "__main__":
    trainFileName = "band2_0115"
    testFileName = "band4_0128"
    trainFile, _ = DataParser.loadRawDataFile(getDefaultFilePath(trainFileName))
    plot(trainFile[0], "Training data")
    tmpFile, sheetNames = DataParser.loadRawDataFile(getDefaultFilePath(testFileName))
    testFile, calibrationFile = calibrationPartition(
        sheetNames, tmpFile, 0.7, 0.3, ["00", "11", "22", "01", "12", "02"]
    )
    plot(testFile[0], "Original testing data")
    testFile = maxminNormalization(trainFile, testFile, calibrationFile)
    plot(testFile[0], "Transformed testing data")
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = timeNormalization(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = timeNormalization(testFeatures)

    print(len(trainFeatures), len(testFeatures))
    classifier = Classifier()
    acc, accTest = classifier.randomForest(
        trainFeatures,
        trainLabel,
        testFeatures,
        testLabel,
    )
    print(acc, accTest)
