import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from ElbowKnee_all_nSensors import *
from DataPartition import *
from Transfer import *


def plotAverage(allFeatures: list[list[float]], allLabel: list[int]):
    colors = ["blue", "green", "red"]
    lineStyle = ["-", "--", ":"]
    label = ["down", "up", "open"]
    avg = [[0 for i in range(24)] for j in range(3)]
    for i in range(len(allFeatures)):
        avg[allLabel[i]] = [avg[allLabel[i]][j] + allFeatures[i][j] for j in range(24)]

    for i in range(3):
        avg[i] = [avg[i][j] / allLabel.count(i) for j in range(len(avg[i]))]
        for j in range(0, 6, 2):
            plt.plot(
                avg[i][j::6],
                avg[i][j + 1 :: 6],
                colors[i],
                linestyle=lineStyle[j // 2],
                marker=".",
                label=label[i] + str(j // 2),
            )
    plt.legend(fontsize="7")
    plt.show()


def plotDistribution(allFeatures: list[list[float]], allLabel: list[int]):
    labelList = ["down", "up", "open"]
    pointColorList = ["lightgreen", "mistyrose", "lightblue", "moccasin"]
    avgColorList = ["b-o", "g-o", "r-o"]
    for ges in range(3):  # 3 gestures
        plt.subplot(1, len(labelList), ges + 1, title=labelList[ges])
        for sen in range(3):  # 3 sensors
            timeSum = [0 for i in range(4)]
            valueSum = [0 for i in range(4)]
            pointCount = 0
            for i, features in enumerate(allFeatures):
                if allLabel[i] == ges:
                    pointCount += 1
                    for k in range(4):  # 4 folding points
                        plt.plot(
                            float(features[k * 6 + sen * 2]),
                            float(features[k * 6 + sen * 2 + 1]),
                            ".",
                            color=pointColorList[k],
                        )
                        timeSum[k] += float(features[k * 6 + sen * 2])
                        valueSum[k] += float(features[k * 6 + sen * 2 + 1])
            timeAvg = [time / pointCount for time in timeSum]
            valueAvg = [value / pointCount for value in valueSum]
            plt.plot(timeAvg, valueAvg, avgColorList[ges])
    plt.show()


def normalize(
    features: list[list[float]], mode: str = "no", flat: list[float] = []
) -> list[list[float]]:
    for i in range(len(features)):
        # time normalization
        r0t = features[i][len(features[i]) // 4]
        for j in range(0, len(features[i]) // 2, 2):
            features[i][j] = (features[i][j]) / r0t
        byRange = (
            features[i][len(features[i]) // 4 * 3] - features[i][len(features[i]) // 2]
        )
        b0t = features[i][len(features[i]) // 2]
        for j in range(len(features[i]) // 2, len(features[i]), 2):
            features[i][j] = (features[i][j] - b0t) / byRange
        # resistance normalization
        if mode == "flat":
            for j in range(3):
                for k in range(j * 2 + 1, len(features[i]), 6):
                    features[i][k] = features[i][k] / flat[j]
        elif mode == "greenpoint":
            for j in range(3):
                green = features[i][j * 2 + 1]
                for k in range(j * 2 + 1, len(features[i]), 6):
                    features[i][k] = features[i][k] / green
    return features


def calculateFlat(fileName: str) -> list[float]:
    flat = []
    xls = pd.ExcelFile(
        os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
    )
    sheet = xls.parse(xls.sheet_names[0])
    for colName in sheet.columns:
        if colName != "gesture":
            flat.append(sum(sheet[colName]) / len(sheet[colName]))
    return flat


def plotFeatures(features: list[float]):
    colors = ["orange", "green", "red"]
    for i in range(0, 6, 2):
        plt.plot(
            features[i::6],
            features[i + 1 :: 6],
            colors[i // 2],
            linestyle="-",
            marker=".",
            label=f"Sensor {i//2}",
        )
    plt.legend()
    plt.show()


def calibrationPartition(
    sheetNames: list[str],
    fullData: list[pd.DataFrame],
    testSplit: float,
    calibrationSplit: float = 0,
    calibrationSheetNames: list[str] = [],
) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    calibrationFile = []
    testFile = []
    for i, sheetName in enumerate(sheetNames):
        test = pd.DataFrame()
        calibration = pd.DataFrame()
        if "12" in sheetName or "01" in sheetName:
            test, calibration = dataPartition(fullData[i], testSplit)
        else:
            calibration, test = dataPartition(fullData[i], 1 - testSplit)

        testFile.append(test)
        for calibrationSheetName in calibrationSheetNames:
            if calibrationSheetName in sheetName:
                calibration, _ = dataPartition(
                    calibration, calibrationSplit / (1 - testSplit)
                )
                calibrationFile.append(calibration)
                break
    return testFile, calibrationFile


if __name__ == "__main__":
    nSensors = 3
    trainFileName = "band2_0115"
    trainFlatName = "band2_flat"
    testFiles = [
        ("band2_0126", "band2_flat"),
        ("band1_0126", "band1_flat"),
        ("band4_0128", "band4_flat"),
    ]
    modes = ["no", "flat", "greenpoint"]
    # for mode in modes:
    #     print(mode)
    #     for tf in testFiles:
    #         testFileName = tf[0]
    #         testFlatName = tf[1]
    #         tmpFile, sheetNames = loadRawDataFile(testFileName)
    #         testFile, calibrationFile = calibrationPartition(sheetNames, tmpFile, 0.7)
    #         trainFile, _ = loadRawDataFile(trainFileName)
    #         trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
    #         trainFeatures = normalize(trainFeatures, mode, calculateFlat(trainFlatName))
    #         testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
    #         testFeatures = normalize(testFeatures, mode, calculateFlat(testFlatName))
    #         print(
    #             f"{trainFileName}({len(trainFeatures)})",
    #             f"{testFileName}({len(testFeatures)})",
    #         )
    #         classifier = Classifier()
    #         acc, accTest = classifier.randomForest(
    #             trainFeatures,
    #             trainLabel,
    #             testFeatures,
    #             testLabel,
    #             f"{testFileName}_{mode}",
    #         )
    #         print(acc, accTest)
    print("maxmin")
    calibrationCombos = [
        ([0.1, 0.2, 0.3], ["00"]),
        ([0.1, 0.2, 0.3], ["11"]),
        ([0.1, 0.2, 0.3], ["22"]),
        ([0.2], ["01"]),
        ([0.2], ["02"]),
        ([0.2], ["12"]),
        ([0.1], ["00", "11", "22"]),
        ([0.2], ["01", "02", "12"]),
        ([0.3], ["00", "11", "22", "01", "12", "02"]),
    ]
    for combo in calibrationCombos:
        for split in combo[0]:
            print(split, combo[1])
            for tf in testFiles:
                trainFile, _ = loadRawDataFile(trainFileName)
                testFileName = tf[0]
                testFlatName = tf[1]
                tmpFile, sheetNames = loadRawDataFile(testFileName)
                testFile, calibrationFile = calibrationPartition(
                    sheetNames, tmpFile, 0.7, split, combo[1]
                )
                testFile = transfer(trainFile, testFile, calibrationFile)
                trainFeatures, trainLabel = fullFileProcessing(trainFile, nSensors)
                trainFeatures = normalize(
                    trainFeatures, "maxmin", calculateFlat(trainFlatName)
                )
                testFeatures, testLabel = fullFileProcessing(testFile, nSensors)
                testFeatures = normalize(
                    testFeatures, "maxmin", calculateFlat(testFlatName)
                )
                print(
                    f"{trainFileName}({len(trainFeatures)})",
                    f"{testFileName}({len(testFeatures)})",
                )
                classifier = Classifier()
                acc, accTest = classifier.randomForest(
                    trainFeatures,
                    trainLabel,
                    testFeatures,
                    testLabel,
                    f"{testFileName}_maxmin_{split*100}%_{'_'.join(combo[1])}",
                )
                print(acc, accTest)
