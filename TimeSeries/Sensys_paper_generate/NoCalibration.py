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
    testFileNames = ["band2_0115", "band2_0126", "band1_0126", "band4_0128"]
    for testFileName in testFileNames:
        tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
        testFile, _ = calibrationPartition(sheetNames, tmpFile, 0.7)
        trainFile, _ = loadRawDataFile(getDefaultFilePath(trainFileName))
        trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
        testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
        classifier = Classifier()
        acc, accTest = classifier.randomForest(
            trainFeatures,
            trainLabel,
            testFeatures,
            testLabel,
        )
        print(testFileName, acc, accTest)
