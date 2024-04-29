import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DataParser import *
from Transfer import plot, normalize, Classifier
from ElbowKnee_all_nSensors import fullFileProcessing
from DataPartition import *

if __name__ == "__main__":
    trainFileName = "band2_0126"
    trainFile, _ = loadRawDataFile(trainFileName)
    trainFile, testFile = fullFileDataPartition(trainFile, 0.6)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = normalize(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = normalize(testFeatures)
    print(len(trainFeatures), len(testFeatures))
    parts = [
        ("all", 0, 24),
        ("green_red", 0, 12),
        ("red_blue", 6, 18),
        ("blue_yellow", 18, 24),
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
            f"{trainFileName}_{part[0]}",
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
            f"{trainFileName}_{part[0]}",
        )
        print(part[0], acc, accTest)
