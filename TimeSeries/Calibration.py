import pandas as pd
from DataPartition import *


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
        if ("12_" in sheetName or "01_" in sheetName) and "012_" not in sheetName:
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


def timeNormalization(features: list[list[float]]) -> list[list[float]]:
    for i in range(len(features)):
        r0t = features[i][len(features[i]) // 4]
        for j in range(0, len(features[i]) // 2, 2):
            features[i][j] = (features[i][j]) / r0t
        byRange = (
            features[i][len(features[i]) // 4 * 3] - features[i][len(features[i]) // 2]
        )
        b0t = features[i][len(features[i]) // 2]
        for j in range(len(features[i]) // 2, len(features[i]), 2):
            features[i][j] = (features[i][j] - b0t) / byRange
    return features


def flatNormalization(
    features: list[list[float]], flatFileName: str, nSensor: int
) -> list[list[float]]:
    flat = []
    xls = pd.ExcelFile(flatFileName)
    sheet = xls.parse(xls.sheet_names[0])
    for colName in sheet.columns:
        if colName != "gesture":
            flat.append(sum(sheet[colName]) / len(sheet[colName]))
    for i in range(len(features)):
        for j in range(nSensor):
            for k in range(j * 2 + 1, len(features[i]), 2 * nSensor):
                features[i][k] = features[i][k] / flat[j]
    return features


def greenpointNormalization(
    features: list[list[float]], nSensor: int
) -> list[list[float]]:
    for i in range(len(features)):
        for j in range(nSensor):
            green = features[i][j * 2 + 1]
            for k in range(j * 2 + 1, len(features[i]), 2 * nSensor):
                features[i][k] = features[i][k] / green
    return features


def findMaxMin(allData: list[pd.DataFrame]) -> list[tuple[float, float]]:
    maxx = [0, 0, 0]
    minn = [9999, 9999, 9999]
    for data in allData:
        tmpMax = data.max()
        tmpMin = data.min()
        for i in range(3):
            maxx[i] = max(maxx[i], tmpMax[str(i)])
            minn[i] = min(minn[i], tmpMin[str(i)])
    return list(zip(maxx, minn))


def findLinearTransform(
    maxmin1: list[tuple[float, float]], maxmin2: list[tuple[float, float]]
) -> list[tuple[float, float]]:  # find the transform to shift maxmin2 to maxmin1
    linearTransform = []
    for i in range(3):
        a = (maxmin1[i][0] - maxmin1[i][1]) / (
            maxmin2[i][0] - maxmin2[i][1]
        )  # y = ax + b
        b = (maxmin2[i][0] * maxmin1[i][1] - maxmin2[i][1] * maxmin1[i][0]) / (
            maxmin2[i][0] - maxmin2[i][1]
        )
        linearTransform.append((a, b))
    return linearTransform


def transformData(
    allData: list[pd.DataFrame], transformParameter: list[tuple[float, float]]
) -> list[pd.DataFrame]:
    for data in allData:
        for i in range(3):
            data[str(i)] = data[str(i)].map(
                lambda value: transformParameter[i][0] * value
                + transformParameter[i][1]
            )
    return allData


def maxminNormalization(
    trainFile: list[pd.DataFrame],
    testFile: list[pd.DataFrame],
    calibrationFile: list[pd.DataFrame],
) -> list[pd.DataFrame]:
    linearTransform = findLinearTransform(
        findMaxMin(trainFile), findMaxMin(calibrationFile)
    )
    testFile = transformData(testFile, linearTransform)
    return testFile
