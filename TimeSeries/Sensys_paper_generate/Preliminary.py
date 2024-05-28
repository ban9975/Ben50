import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DataParser import *
from Classifier import *
from ElbowKnee_all_nSensors import *
from Calibration import *

if __name__ == "__main__":
    trainFileName = "band2_0115"
    trainFile, sheetNames = loadRawDataFile(getDefaultFilePath(trainFileName))
    trainFile, _ = calibrationPartition(
        sheetNames,
        trainFile,
        0.6,
    )
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = [[f[7], f[9], f[11]] for f in trainFeatures]
    print("train: ", trainFileName, len(trainFeatures))
    testFileNames = ["band2_0115", "band2_0126", "band1_0126", "band4_0128"]
    for testFileName in testFileNames:
        tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
        _, tmpFile = calibrationPartition(
            sheetNames,
            tmpFile,
            0.6,
            0.4,
            ["00", "11", "22", "01", "12", "02"],
        )
        testFile, _ = calibrationPartition(
            sheetNames,
            tmpFile,
            0.5,
        )
        testFeatures, testLabel = fullFileProcessing(testFile, 3)
        testFeatures = [[f[7], f[9], f[11]] for f in testFeatures]
        classifier = Classifier()
        acc, accTest = classifier.randomForest(
            trainFeatures,
            trainLabel,
            testFeatures,
            testLabel,
        )
        print("test: ", testFileName, len(testFeatures))
        print(acc, accTest)
