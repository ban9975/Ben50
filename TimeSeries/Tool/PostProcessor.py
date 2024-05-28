import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import numpy as np
from DataParser import *
from ElbowKnee_all_nSensors import *
from DataPartition import *
from CalibrationClassifier import *


class PostProcessor:
    def __init__(self):
        pass

    def calculateExtractionRate(self, fileName: str) -> tuple[int]:
        def splitGroupCount(
            data: pd.DataFrame, ekLists: list[list[tuple[int, int]]]
        ) -> tuple[list[list[int]], list[int]]:
            expected = 0
            groups = []
            labelPoints = []
            for s in range(len(ekLists)):
                group = []
                expected = 0
                for i in range(len(ekLists[s])):
                    if ekLists[s][i][0] == expected:
                        if expected == 0:
                            timeStart = ekLists[s][i][1]
                        if expected == 3:
                            expected = 0
                            group.append(timeStart)
                            if s == 0:
                                labelPoints.append(ekLists[s][i - 2][1])
                        else:
                            expected = expected + 1
                    else:
                        expected = 0
                groups.append(group)

            count = 0
            for i in range(len(groups[0])):
                t1 = False
                t2 = False
                for t in range(groups[0][i] - 700, groups[0][i] + 700):
                    if t in groups[1]:
                        t1 = True
                    if t in groups[2]:
                        t2 = True
                    if t1 and t2 and data["gesture"][labelPoints[i] // 10] != -1:
                        count += 1
                        break
            return count

        def countEK(
            data: pd.DataFrame,
            nSensors: int,
            ekGroupParameters: tuple[list[EKGroupParameter], int, int],
            step: int,
        ) -> int:
            ekLists = []
            for i in range(nSensors):
                ekLists.append(findEK(data, i, ekGroupParameters[0][i]))
            for i in range(nSensors):
                ekLists[i] = removeDuplicate(ekLists[i], ekGroupParameters[1])
            if step > 0:
                ekLists = complement(ekLists, ekGroupParameters[2])
            if step > 1:
                for i in range(nSensors):
                    ekLists[i] = orderCheck(ekLists[i])
                ekLists = complement(ekLists, ekGroupParameters[2])
            count = splitGroupCount(data, ekLists)
            return count

        self.fileName = fileName
        self.result = []
        for i in range(4):
            allCount = 0
            allData, _ = loadRawDataFile(self.fileName)
            for data in allData:
                count = countEK(data, nSensors, offlineEKGroupParameters, i)
                allCount += count
            self.result.append(allCount / foldingPointGroundTruth * 100)
        return self.result

    def plotExtractionRate(self, plotPath: str) -> str:
        fig, ax = plt.subplots()
        x = [i * 2 for i in range(1, 4)]
        h = [self.result[i] for i in range(3)]
        label = ["Baseline", "Point-level majority vote", "Group-level majority vote"]
        barList = plt.bar(x, h, tick_label=label, width=1.2, color="#4A85E8")
        figName = os.path.expanduser(
            os.path.join(
                plotPath,
                f"{os.path.basename(os.path.normpath(self.fileName)).split('.')[0]}_foldingpoint.png",
            )
        )
        plt.xlabel("Procedures")
        plt.ylabel("Extraction rate (%)")
        plt.yticks(np.arange(0, 101, step=10))
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        plt.grid(axis="y")
        plt.savefig(figName, bbox_inches="tight", dpi=600)
        plt.close()
        return figName

    def beforeCalibration(
        self,
        trainFileName: str,
        testFileName: str,
        resultFile: str,
    ):
        resultFile = os.path.expanduser(resultFile)
        if not os.path.exists(resultFile):
            workbook = Workbook()
            workbook.create_sheet("Result")
            sheet = workbook.worksheets[0]
            sheet.append(["training data", "testing data", "Testing accuracy"])
            workbook.save(resultFile)
            workbook.close()
        workbook = load_workbook(resultFile)
        sheet = workbook.worksheets[0]
        sheet.append([trainFileName, testFileName])
        calibrationClassifier = CalibrationClassifier(trainFileName, testFileName)
        row = sheet.max_row
        col = 3
        result = calibrationClassifier.train("notime")
        sheet.cell(row, col, result[3])
        workbook.save(resultFile)
        col += 1
        workbook.close()

    def afterCalibration(
        self,
        trainFileName: str,
        testFileName: str,
        trainFlatFileName: str,
        testFlatFileName: str,
        resultFile: str,
    ):
        modes = ["no calibration", "flat", "greenpoint", "maxmin"]
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
        sheet.append([trainFileName, testFileName])
        calibrationClassifier = CalibrationClassifier(
            trainFileName, testFileName, trainFlatFileName, testFlatFileName
        )
        row = sheet.max_row
        col = 3
        for mode in modes:
            result = calibrationClassifier.train(mode)
            sheet.cell(row, col, result[3])
            workbook.save(resultFile)
            col += 1
        workbook.close()

    def calibrationEffort(self, trainFileName: str, testFileName: str, resultFile: str):
        efforts = [
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
            "down-up-open*1",
            "down-up-open*2",
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
                + efforts
            )
            workbook.save(resultFile)
            workbook.close()
        workbook = load_workbook(resultFile)
        sheet = workbook.worksheets[0]
        sheet.append([trainFileName, testFileName])
        calibrationClassifier = CalibrationClassifier(trainFileName, testFileName)
        row = sheet.max_row
        col = 3
        for combo in maxminSplitCombos:
            print(combo[1])
            for split in combo[0]:
                result = calibrationClassifier.train("maxmin", (split, combo[1]))
                sheet.cell(row, col, result[3])
                col += 1
                workbook.save(resultFile)
        workbook.close()
