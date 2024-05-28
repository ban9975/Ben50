import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DataParser import *
from Classifier import *
from ElbowKnee_all_nSensors import fullFileProcessing
from DataPartition import *
from CalibrationCompare import *

if __name__ == "__main__":
    trainFileName = "band2_0115"
    testFileNames = ["band2_0115", "band2_0116", "band1_0126", "band4_0128"]
    for testFileName in testFileNames:
        trainFile, sheetNames = loadRawDataFile(getDefaultFilePath(trainFileName))
        trainFile, _ = calibrationPartition(
            sheetNames,
            trainFile,
            0.6,
        )
        print(testFileName)
        tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
        _, tmpFile = calibrationPartition(
            sheetNames,
            tmpFile,
            0.6,
            0.4,
            ["00", "11", "22", "01", "12", "02"],
        )
        testFile, calibrationFile = calibrationPartition(
            sheetNames,
            tmpFile,
            0.5,
            0.5,
            ["00", "11", "22", "01", "12", "02"],
        )
        testFile = maxminNormalization(trainFile, testFile, calibrationFile)
        trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
        trainFeatures = normalize(trainFeatures)
        testFeatures, testLabel = fullFileProcessing(testFile, 3)
        testFeatures = normalize(testFeatures)
        print(len(trainFeatures), len(testFeatures))
        parts = [
            ("all", 0, 24),
            ("green_red", 0, 12),
            ("red_blue", 6, 18),
            ("blue_yellow", 12, 24),
            ("green", 0, 6),
            ("red", 6, 12),
            ("blue", 12, 18),
            ("yellow", 18, 24),
        ]
        for part in parts:
            newTrainFeatures = []
            newTestFeatures = []
            for i in range(len(trainFeatures)):
                newTrainFeatures.append(trainFeatures[i][part[1] : part[2]])
            for i in range(len(testFeatures)):
                newTestFeatures.append(testFeatures[i][part[1] : part[2]])
            classifier = Classifier()
            acc, accTest = classifier.randomForest(
                newTrainFeatures,
                trainLabel,
                newTestFeatures,
                testLabel,
            )
            print(part[0], acc, accTest)
        parts = [("only_time", 0), ("only_resistance", 1)]
        for part in parts:
            newTrainFeatures = []
            newTestFeatures = []
            for i in range(len(trainFeatures)):
                newTrainFeatures.append(trainFeatures[i][part[1] :: 2])
            for i in range(len(testFeatures)):
                newTestFeatures.append(testFeatures[i][part[1] :: 2])
            classifier = Classifier()
            acc, accTest = classifier.randomForest(
                newTrainFeatures,
                trainLabel,
                newTestFeatures,
                testLabel,
            )
            print(part[0], acc, accTest)
