import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DataParser import *
from Transfer import *
from ElbowKnee_all_nSensors import *

if __name__ == "__main__":
    trainFileName = "band2_0115"
    trainFile, _ = loadRawDataFile(trainFileName)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = [[f[7], f[9], f[11]] for f in trainFeatures]
    print("train: ", trainFileName, len(trainFeatures))
    testFileNames = ["band2_0126", "band1_0126", "band4_0127"]
    for testFileName in testFileNames:
        testFile, _ = loadRawDataFile(testFileName)
        testFeatures, testLabel = fullFileProcessing(testFile, 3)
        testFeatures = [[f[7], f[9], f[11]] for f in testFeatures]
        print(testFeatures)
        classifier = Classifier()
        acc, accTest = classifier.randomForest(
            trainFeatures,
            trainLabel,
            testFeatures,
            testLabel,
            f"{testFileName}_preliminary",
        )
        print("test: ", testFileName, len(testFeatures))
        print(acc, accTest)
