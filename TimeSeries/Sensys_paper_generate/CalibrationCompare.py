import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from ElbowKnee_all_nSensors import *
from Calibration import *
from Classifier import *


if __name__ == "__main__":
    nSensors = 3
    trainFileName = "band2_0115"
    trainFlatName = "band2_flat"
    testFiles = [
        ("band2_0126", "band2_flat"),
        ("band1_0126", "band1_flat"),
        ("band4_0128", "band4_flat"),
    ]
    modes = ["no", "flat", "greenpoint"]
    for mode in modes:
        print(mode)
        for tf in testFiles:
            testFileName = tf[0]
            testFlatName = tf[1]
            tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
            testFile, calibrationFile = calibrationPartition(sheetNames, tmpFile, 0.7)
            trainFile, _ = loadRawDataFile(getDefaultFilePath(trainFileName))
            trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
            trainFeatures = timeNormalization(trainFeatures)
            testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
            testFeatures = timeNormalization(testFeatures)
            if mode == "flat":
                trainFeatures = flatNormalization(
                    trainFeatures, getDefaultFilePath(trainFlatName), nSensors
                )
                testFeatures = flatNormalization(
                    testFeatures, getDefaultFilePath(testFlatName), nSensors
                )
            elif mode == "greenpoint":
                trainFeatures = greenpointNormalization(trainFeatures, nSensors)
                testFeatures = greenpointNormalization(testFeatures, nSensors)
            print(
                f"{trainFileName}({len(trainFeatures)})",
                f"{testFileName}({len(testFeatures)})",
            )
            classifier = Classifier()
            acc, accTest = classifier.randomForest(
                trainFeatures,
                trainLabel,
                testFeatures,
                testLabel,
            )
            classifier.confusionMatrix(
                classifier.expected_test,
                classifier.actual_test,
                f"{testFileName}_{mode}",
                os.path.join(
                    os.getcwd(),
                    "../Sensys 2024",
                    f"{testFileName}_{mode}.png",
                ),
            )
            print(acc, accTest)
    print("maxmin")
    calibrationCombos = [
        ([0.1, 0.2, 0.3], ["00"]),
        ([0.1, 0.2, 0.3], ["11"]),
        ([0.1, 0.2, 0.3], ["22"]),
        ([0.2], ["01"]),
        ([0.2], ["02"]),
        ([0.2], ["12"]),
        ([0.1], ["00", "11", "22"]),
        ([0.2], ["01", "02", "12"]),
        ([0.3], ["00", "11", "22", "01", "12", "02"]),
    ]
    for combo in calibrationCombos:
        for split in combo[0]:
            print(split, combo[1])
            for tf in testFiles:
                trainFile, _ = loadRawDataFile(getDefaultFilePath(trainFileName))
                testFileName = tf[0]
                tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
                testFile, calibrationFile = calibrationPartition(
                    sheetNames, tmpFile, 0.7, split, combo[1]
                )
                testFile = maxminNormalization(trainFile, testFile, calibrationFile)
                trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
                trainFeatures = timeNormalization(trainFeatures)
                testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
                testFeatures = timeNormalization(testFeatures)
                print(
                    f"{trainFileName}({len(trainFeatures)})",
                    f"{testFileName}({len(testFeatures)})",
                )
                classifier = Classifier()
                acc, accTest = classifier.randomForest(
                    trainFeatures,
                    trainLabel,
                    testFeatures,
                    testLabel,
                )
                classifier.confusionMatrix(
                    classifier.expected_test,
                    classifier.actual_test,
                    f"{testFileName}_maxmin_{split*100}%_{'_'.join(combo[1])}",
                    os.path.join(
                        os.getcwd(),
                        "../Sensys 2024",
                        f"{testFileName}_maxmin_{split*100}%_{'_'.join(combo[1])}.png",
                    ),
                )
                print(acc, accTest)
