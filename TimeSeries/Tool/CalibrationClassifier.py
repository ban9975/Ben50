import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from openpyxl import *
from Calibration import *
from Classifier import *
from Constants import *


class CalibrationClassifier:
    def __init__(
        self,
        trainFileName: str,
        testFileName: str,
        trainFlatFileName: str = "",
        testFlatFileName: str = "",
    ):
        self.trainFileName = trainFileName
        self.testFileName = testFileName
        self.trainFlatFileName = trainFlatFileName
        self.testFlatFileName = testFlatFileName

    def train(
        self,
        mode: str,
        maxminSplit: tuple[float, list[str]] = (
            0.3,
            ["00", "11", "22", "01", "12", "02"],
        ),
    ) -> tuple[int, int, float, float]:
        self.mode = mode
        tmpFile, sheetNames = loadRawDataFile(self.testFileName)
        trainFile, _ = loadRawDataFile(self.trainFileName)
        if self.mode == "notime":
            testFile, _ = calibrationPartition(sheetNames, tmpFile, 0.7)
            trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
            testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
        elif self.mode == "preliminary":
            testFile, _ = calibrationPartition(sheetNames, tmpFile, 0.7)
            trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
            trainFeatures = [[f[7], f[9], f[11]] for f in trainFeatures]
            testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
            testFeatures = [[f[7], f[9], f[11]] for f in testFeatures]
        elif self.mode == "maxmin":
            testFile, calibrationFile = calibrationPartition(
                sheetNames, tmpFile, 0.7, maxminSplit[0], maxminSplit[1]
            )
            testFile = maxminNormalization(trainFile, testFile, calibrationFile)
            trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
            trainFeatures = timeNormalization(trainFeatures)
            testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
            testFeatures = timeNormalization(testFeatures)
        else:
            testFile, _ = calibrationPartition(sheetNames, tmpFile, 0.7)
            trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
            trainFeatures = timeNormalization(trainFeatures)
            testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
            testFeatures = timeNormalization(testFeatures)
            if self.mode == "flat":
                trainFeatures = flatNormalization(
                    trainFeatures, self.trainFlatFileName, nSensors
                )
                testFeatures = flatNormalization(
                    testFeatures, self.testFlatFileName, nSensors
                )
            elif self.mode == "greenpoint":
                trainFeatures = greenpointNormalization(trainFeatures, nSensors)
                testFeatures = greenpointNormalization(testFeatures, nSensors)

        self.classifier = Classifier()
        acc, accTest = self.classifier.randomForest(
            trainFeatures,
            trainLabel,
            testFeatures,
            testLabel,
        )
        return len(trainFeatures), len(testFeatures), acc, accTest

    def confusionMatrix(self, plotPath: str):
        path = os.path.expanduser(
            os.path.join(
                plotPath,
                f"{os.path.basename(os.path.normpath(self.trainFileName)).split('.')[0]}_{os.path.basename(os.path.normpath(self.testFileName)).split('.')[0]}_{self.mode}.png",
            )
        )
        self.classifier.confusionMatrix(
            self.classifier.expected_test,
            self.classifier.actual_test,
            f"{os.path.basename(os.path.normpath(self.trainFileName)).split('.')[0]}_{os.path.basename(os.path.normpath(self.testFileName)).split('.')[0]}_{self.mode}",
            path,
        )
        return path
