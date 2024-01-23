from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import savgol_filter


class EKParameter:
    def __init__(self, s: int, windowSize: int, overlapSize: int, threshold: int):
        self.s = s
        self.windowSize = windowSize
        self.overlapSize = overlapSize
        self.threshold = threshold


class EKGroupParameter:
    def __init__(
        self,
        smooth: int,
        smoothPolyOrder: int,
        convexInc: EKParameter,
        concaveInc: EKParameter,
        concaveDec: EKParameter,
        convexDec: EKParameter,
    ) -> list[tuple[int, int]]:
        self.smooth = smooth
        self.smoothPolyOrder = smoothPolyOrder
        self.convexInc = convexInc
        self.concaveInc = concaveInc
        self.concaveDec = concaveDec
        self.convexDec = convexDec


def smooth(y, window_length, polyorder):
    y_smooth = savgol_filter(y, window_length=window_length, polyorder=polyorder)
    return y_smooth


def findEK(data: pd.DataFrame, sensorNum: int, parameters: EKGroupParameter):
    col = str(sensorNum)
    t = [i * 10 for i in range(len(data[col]))]
    data[col] = smooth(data[col], parameters.smooth, parameters.smoothPolyOrder)
    convexInc = {}
    concaveInc = {}
    concaveDec = {}
    convexDec = {}
    for i in range(
        0,
        len(data[col]) - parameters.convexInc.windowSize,
        parameters.convexInc.overlapSize,
    ):
        kneedle = KneeLocator(
            t[i : i + parameters.convexInc.windowSize],
            data[col][i : i + parameters.convexInc.windowSize],
            S=parameters.convexInc.s,
            curve="convex",
            direction="increasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in convexInc:
                convexInc[kneedle.knee] += 1
            else:
                convexInc[kneedle.knee] = 1
    for i in range(
        0,
        len(data[col]) - parameters.concaveInc.windowSize,
        parameters.concaveInc.overlapSize,
    ):
        kneedle = KneeLocator(
            t[i : i + parameters.concaveInc.windowSize],
            data[col][i : i + parameters.concaveInc.windowSize],
            S=parameters.concaveInc.s,
            curve="concave",
            direction="increasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in concaveInc:
                concaveInc[kneedle.knee] += 1
            else:
                concaveInc[kneedle.knee] = 1
    for i in range(
        0,
        len(data[col]) - parameters.concaveDec.windowSize,
        parameters.concaveDec.overlapSize,
    ):
        kneedle = KneeLocator(
            t[i : i + parameters.concaveDec.windowSize],
            data[col][i : i + parameters.concaveDec.windowSize],
            S=parameters.concaveDec.s,
            curve="concave",
            direction="decreasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in concaveDec:
                concaveDec[kneedle.knee] += 1
            else:
                concaveDec[kneedle.knee] = 1
    for i in range(
        0,
        len(data[col]) - parameters.convexDec.windowSize,
        parameters.convexDec.overlapSize,
    ):
        kneedle = KneeLocator(
            t[i : i + parameters.convexDec.windowSize],
            data[col][i : i + parameters.convexDec.windowSize],
            S=parameters.convexDec.s,
            curve="convex",
            direction="decreasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in convexDec:
                convexDec[kneedle.knee] += 1
            else:
                convexDec[kneedle.knee] = 1
    result = []
    for c in convexInc:
        if convexInc[c] > parameters.convexInc.threshold:
            result.append((0, c))
    for c in concaveInc:
        if concaveInc[c] > parameters.concaveInc.threshold:
            result.append((1, c))
    for c in concaveDec:
        if concaveDec[c] > parameters.concaveDec.threshold:
            result.append((2, c))
    for c in convexDec:
        if convexDec[c] > parameters.convexDec.threshold:
            result.append((3, c))
    result.sort(key=lambda x: x[1])
    return result


def removeDuplicate(
    ekList: list[tuple[int, int]], duplicateRange: int
) -> list[tuple[int, int]]:
    popList = []
    for ek in ekList:
        if any(
            (ek[0], point) in ekList for point in range(ek[1] - duplicateRange, ek[1], 10)
        ):
            popList.append(ek)
    for ek in popList:
        ekList.remove(ek)
    return ekList


def postprocess(
    ek0: list[tuple[int, int]],
    ek1: list[tuple[int, int]],
    ek2: list[tuple[int, int]],
    duplicateRange: int,
    sensorRange: int,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
    duplicateRange = duplicateRange * 10  # change unit from grid to millisecond
    sensorRange = sensorRange * 10  # change unit from grid to millisecond
    ek0 = removeDuplicate(ek0, duplicateRange)
    ek1 = removeDuplicate(ek1, duplicateRange)
    ek2 = removeDuplicate(ek2, duplicateRange)
    ekCount = len(ek0)
    i = 0
    while i < ekCount:
        inEk1 = []
        inEk2 = []
        for point in range(ek0[i][1] - sensorRange, ek0[i][1] + sensorRange, 10):
            if (ek0[i][0], point) in ek1:
                inEk1.append((ek0[i][0], point))
            if (ek0[i][0], point) in ek2:
                inEk2.append((ek0[i][0], point))
        if len(inEk1) == 0 and len(inEk2) == 0:
            ek0.pop(i)
            ekCount = ekCount - 1
            i = i - 1
        elif len(inEk1) > 0 and len(inEk2) == 0:
            ek2.append((ek0[i][0], int((ek0[i][1] / 10 + inEk1[0][1] / 10) // 2 * 10)))
        elif len(inEk2) > 0 and len(inEk1) == 0:
            ek1.append((ek0[i][0], int((ek0[i][1] / 10 + inEk2[0][1] / 10) // 2 * 10)))
        i = i + 1
    ekCount = len(ek1)
    i = 0
    while i < ekCount:
        inEk0 = []
        inEk2 = []
        for point in range(ek1[i][1] - sensorRange, ek1[i][1] + sensorRange, 10):
            if (ek1[i][0], point) in ek0:
                inEk0.append((ek1[i][0], point))
            if (ek1[i][0], point) in ek2:
                inEk2.append((ek1[i][0], point))
        if len(inEk0) == 0 and len(inEk2) == 0:
            ek1.pop(i)
            ekCount = ekCount - 1
            i = i - 1
        elif len(inEk0) > 0 and len(inEk2) == 0:
            ek2.append((ek1[i][0], int((ek1[i][1] / 10 + inEk0[0][1] / 10) // 2 * 10)))
        elif len(inEk2) > 0 and len(inEk0) == 0:
            ek0.append((ek1[i][0], int((ek1[i][1] / 10 + inEk2[0][1] / 10) // 2 * 10)))
        i = i + 1
    ekCount = len(ek2)
    i = 0
    while i < ekCount:
        inEk0 = []
        inEk1 = []
        for point in range(ek2[i][1] - sensorRange, ek2[i][1] + sensorRange, 10):
            if (ek2[i][0], point) in ek0:
                inEk0.append((ek2[i][0], point))
            if (ek2[i][0], point) in ek1:
                inEk1.append((ek2[i][0], point))
        if len(inEk0) == 0 and len(inEk1) == 0:
            ek2.pop(i)
            ekCount = ekCount - 1
            i = i - 1
        elif len(inEk0) > 0 and len(inEk1) == 0:
            ek2.append((ek2[i][0], int((ek2[i][1] / 10 + inEk0[0][1] / 10) // 2 * 10)))
        elif len(inEk1) > 0 and len(inEk0) == 0:
            ek0.append((ek2[i][0], int((ek2[i][1] / 10 + inEk1[0][1] / 10) // 2 * 10)))
        i = i + 1
    ek0.sort(key=lambda x: x[1])
    ek1.sort(key=lambda x: x[1])
    ek2.sort(key=lambda x: x[1])
    return ek0, ek1, ek2


def splitGroup(
    data: pd.DataFrame,
    ek0: list[tuple[int, int]],
    ek1: list[tuple[int, int]],
    ek2: list[tuple[int, int]],
) -> tuple[list[list[int]], list[int]]:
    expected = 0
    features = []
    label = []
    pending = []
    for i in range(len(ek0)):
        if ek0[i][0] == expected and ek1[i][0] == expected and ek2[i][0] == expected:
            if expected == 0:
                timeStart = ek0[i][1]
            pending += [
                ek0[i][1]-timeStart,
                data["0"][ek0[i][1]//10],
                ek1[i][1]-timeStart,
                data["1"][ek1[i][1]//10],
                ek2[i][1]-timeStart,
                data["2"][ek2[i][1]//10],
            ]
            if expected == 3:
                features.append(pending[1:])
                label.append(data['gesture'][(features[-1][5] + timeStart)//10])
                pending = []
                expected = 0
            else:
                expected = expected + 1
        else:
            pending = []
            expected = 0
    return features, label

def loadFile(fileName: str, sheetName: list[str] = []) -> list[pd.DataFrame]:
    data = []
    xls = pd.ExcelFile(
        os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
    )
    if sheetName == []:
        sheetName = xls.sheet_names
    for name in sheetName:
        data.append(xls.parse(name))
    return data


def plot(data: pd.DataFrame, sensorNum: int, ekList: list[tuple[int, int]]):
    color = ["go", "ro", "bo", "yo"]
    col = str(sensorNum)
    plt.plot([i * 10 for i in range(len(data[col]))], data[col])
    for ek in ekList:
        plt.plot(ek[1], data[col][ek[1] // 10], color[ek[0]])


if __name__ == "__main__":
    allData = loadFile('band2_0116')
    allFeatures = []
    allLabel = []
    for data in allData:
        ek0 = findEK(
            data,
            0,
            EKGroupParameter(
                90,
                2,
                EKParameter(1, 250, 10, 1),
                EKParameter(1, 300, 5, 2),
                EKParameter(1, 300, 10, 3),
                EKParameter(1, 150, 4, 6),
            ),
        )
        ek1 = findEK(
            data,
            1,
            EKGroupParameter(
                40,
                1,
                EKParameter(1, 180, 10, 1),
                EKParameter(1, 150, 6, 2),
                EKParameter(1, 210, 7, 2),
                EKParameter(1, 150, 6, 2),
            ),
        )
        ek2 = findEK(
            data,
            2,
            EKGroupParameter(
                40,
                1,
                EKParameter(1, 180, 9, 1),
                EKParameter(1, 150, 6, 2),
                EKParameter(1, 140, 7, 2),
                EKParameter(1, 180, 5, 3),
            ),
        )
        ek0, ek1, ek2 = postprocess(ek0, ek1, ek2, 70, 70)
        features, label = splitGroup(data, ek0, ek1, ek2)
        allFeatures+=features
        allLabel+=label
    print(len(allFeatures))