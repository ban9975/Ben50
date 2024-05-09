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
    ):
        self.trainFileName = ""
        self.testFileName = ""
        self.trainFlatFileName = ""
        self.testFlatFileName = ""

    def setFile(
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
        if self.mode == "maxmin":
            testFile, calibrationFile = calibrationPartition(
                sheetNames, tmpFile, 0.7, maxminSplit[0], maxminSplit[1]
            )
            testFile = maxminNormalization(trainFile, testFile, calibrationFile)
            trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
            trainFeatures = timeNormalization(trainFeatures)
            testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
            testFeatures = timeNormalization(testFeatures)
        else:
            testFile, calibrationFile = calibrationPartition(sheetNames, tmpFile, 0.7)
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

    def trainAll(self, resultFile: str):
        modes = [
            "no calibration",
            "flat",
            "greenpoint",
            "maxmin",
            "down*1",
            "down*2",
            "down*3",
            "up*1",
            "up*2",
            "up*3",
            "open*1",
            "open*2",
            "open*3",
            "down-up",
            "down-open",
            "up-open",
            "down_up_open*1",
            "down_up_open*2",
        ]
        maxminSplitCombos = [
            ([0.1, 0.2, 0.3], ["00"]),
            ([0.1, 0.2, 0.3], ["11"]),
            ([0.1, 0.2, 0.3], ["22"]),
            ([0.2], ["01"]),
            ([0.2], ["02"]),
            ([0.2], ["12"]),
            ([0.1], ["00", "11", "22"]),
            ([0.2], ["01", "02", "12"]),
        ]
        resultFile = os.path.expanduser(resultFile)
        if not os.path.exists(resultFile):
            workbook = Workbook()
            workbook.create_sheet("Result")
            sheet = workbook.worksheets[0]
            sheet.append(
                [
                    "training data",
                    "testing data",
                ]
                + modes
            )
            workbook.save(resultFile)
            workbook.close()
        workbook = load_workbook(resultFile)
        sheet = workbook.worksheets[0]
        sheet.append([self.trainFileName, self.testFileName])
        row = sheet.max_row
        col = 3
        for mode in modes[:4]:
            print(mode)
            result = self.train(mode)
            sheet.cell(row, col, result[3])
            workbook.save(resultFile)
            col += 1
        for combo in maxminSplitCombos:
            print(combo[1])
            for split in combo[0]:
                result = self.train("maxmin", (split, combo[1]))
                sheet.cell(row, col, result[3])
                col += 1
                workbook.save(resultFile)
        workbook.close()
