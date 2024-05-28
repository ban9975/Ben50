import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from ElbowKnee_all_nSensors import *
from Calibration import *
from Classifier import *


if __name__ == "__main__":
    nSensors = 4
    trainFileName = "band5_0315"
    testFileName = "band5_0316"
    tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
    testFile, calibrationFile = calibrationPartition(
        sheetNames, tmpFile, 0.7, 0.3, ["0123", "1032", "3120", "0213"]
    )
    trainFile, _ = loadRawDataFile(getDefaultFilePath(trainFileName))
    testFile = maxminNormalization(trainFile, testFile, calibrationFile)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
    trainFeatures = timeNormalization(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
    testFeatures = timeNormalization(testFeatures)
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
        "",
        os.path.join(
            os.getcwd(),
            "../Sensys 2024",
            f"{trainFileName}_{testFileName}.png",
        ),
    )
    print(acc, accTest)
