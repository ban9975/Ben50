import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from sklearn.inspection import permutation_importance
import numpy as np
from DataParser import *
from ElbowKnee_all_nSensors import *
from DataPartition import *
from CalibrationClassifier import *


class Plotter:
    def __init__(self):
        pass

    def calculateFeatureImportance(self, fileName) -> tuple[int, int, float, float]:
        print(fileName)
        self.fileName = fileName
        file, _ = loadRawDataFile(self.fileName)
        trainFile, testFile = fullFileDataPartition(file, 0.6)
        trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
        trainFeatures = normalize(trainFeatures)
        testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
        testFeatures = normalize(testFeatures)
        classifier = Classifier()
        acc, accTest = classifier.randomForest(
            trainFeatures,
            trainLabel,
            testFeatures,
            testLabel,
        )
        self.result = permutation_importance(
            classifier.model,
            testFeatures,
            testLabel,
            n_repeats=10,
            random_state=42,
        )
        self.forest_importances = pd.Series(
            self.result.importances_mean, index=generateFeatureIndex()
        )
        return len(trainFeatures), len(testFeatures), acc, accTest

    def plotFeatureImportance(self, plotPath: str) -> str:
        fig, ax = plt.subplots()
        self.forest_importances.plot.bar(yerr=self.result.importances_std, ax=ax)
        ax.set_title("Feature importances using permutation on full model")
        ax.set_ylabel("Mean accuracy decrease")
        fig.tight_layout()
        figName = os.path.expanduser(
            os.path.join(
                plotPath,
                f"{os.path.basename(os.path.normpath(self.fileName)).split('.')[0]}_feature_importance.png",
            )
        )
        plt.savefig(figName, bbox_inches="tight")
        plt.close()
        return figName

    def calculateSelectedFeatures(
        self, fileName: str
    ) -> tuple[int, int, list[tuple[str, float, float]]]:
        self.fileName = fileName
        file, _ = loadRawDataFile(self.fileName)
        trainFile, testFile = fullFileDataPartition(file, 0.6)
        trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
        trainFeatures = normalize(trainFeatures)
        testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
        testFeatures = normalize(testFeatures)
        self.result = []
        parts = [
            ("4 points", 0, 24),
            ("green", 0, 6),
            ("red", 6, 12),
            ("blue", 12, 18),
            ("yellow", 18, 24),
            ("green_red", 0, 12),
            ("red_blue", 6, 18),
            ("blue_yellow", 12, 24),
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
            self.result.append((part[0], acc, accTest))
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
            self.result.append((part[0], acc, accTest))
        return len(trainFeatures), len(testFeatures), self.result

    def plotSelectedFeatures(self, plotPath: str) -> str:
        fig, ax = plt.subplots()
        x = [i for i in range(1, 9)]
        h = [result[2] for result in self.result[:8]]
        label = [result[0] for result in self.result[:8]]
        barList = plt.bar(x, h, tick_label=label, width=0.75)
        barList[0].set_color("g")
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")
        foldingpointFigName = os.path.expanduser(
            os.path.join(
                plotPath,
                f"{os.path.basename(os.path.normpath(self.fileName)).split('.')[0]}_selected_foldingpoint.png",
            )
        )
        plt.title("Selected Features -- Folding points")
        plt.xlabel("Selected features")
        plt.ylabel("Testing accuracy")
        plt.yticks(np.arange(0, 1, step=0.1))
        ax.set_axisbelow(True)
        plt.grid(axis="y")
        plt.savefig(foldingpointFigName, bbox_inches="tight")
        plt.close()
        fig, ax = plt.subplots()
        x = [1, 2, 3]
        h = [self.result[0][2], self.result[8][2], self.result[9][2]]
        label = [self.result[0][0], self.result[8][0], self.result[9][0]]
        barList = plt.bar(x, h, tick_label=label, width=0.75)
        barList[0].set_color("g")
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")
        plt.title("Selected Features -- Resistance v.s. Timestamp")
        plt.xlabel("Selected features")
        plt.ylabel("Testing accuracy")
        plt.yticks(np.arange(0, 1.01, step=0.1))
        ax.set_axisbelow(True)
        plt.grid(axis="y")
        timeresistanceFigName = os.path.expanduser(
            os.path.join(
                plotPath,
                f"{os.path.basename(os.path.normpath(self.fileName)).split('.')[0]}_selected_timeresistance.png",
            )
        )
        plt.savefig(timeresistanceFigName, bbox_inches="tight")
        plt.close()

        return foldingpointFigName, timeresistanceFigName

    def calculateFoldingPoint(self, fileName: str) -> tuple[int]:
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
            self.result.append(allCount)
        return self.result

    def plotFoldingPoint(self, plotPath: str) -> str:
        fig, ax = plt.subplots()
        x = [i for i in range(1, 4)]
        h = [self.result[i] / foldingPointGroundTruth * 100 for i in range(3)]
        label = ["Baseline", "Point-level majority vote", "Group-level majority vote"]
        barList = plt.bar(x, h, tick_label=label, width=0.75)
        barList[0].set_color("g")
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha="right")
        figName = os.path.expanduser(
            os.path.join(
                plotPath,
                f"{os.path.basename(os.path.normpath(self.fileName)).split('.')[0]}_foldingpoint.png",
            )
        )
        plt.title("Folding point algorithm improvement")
        plt.xlabel("Procedures")
        plt.ylabel("Extraction rate (%)")
        plt.yticks(np.arange(0, 101, step=10))
        ax.set_axisbelow(True)
        plt.grid(axis="y")
        plt.savefig(figName, bbox_inches="tight")
        plt.close()
        return figName
