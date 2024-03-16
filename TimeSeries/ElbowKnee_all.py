from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
from DataParser import *
from scipy.signal import savgol_filter
import csv


class EKParameter:
    def __init__(self, s: int, windowSize: int, overlapSize: int, threshold: int, online:int = False):
        self.s = s
        self.windowSize = windowSize
        self.overlapSize = overlapSize
        self.threshold = threshold
        self.online = online


class EKGroupParameter:
    def __init__(
        self,
        smooth: int,
        smoothPolyOrder: int,
        convexInc: EKParameter,
        concaveInc: EKParameter,
        concaveDec: EKParameter,
        convexDec: EKParameter,
    ):
        self.smooth = smooth
        self.smoothPolyOrder = smoothPolyOrder
        self.convexInc = convexInc
        self.concaveInc = concaveInc
        self.concaveDec = concaveDec
        self.convexDec = convexDec


def importEKFile(fileName: str) -> tuple[list[list[float]], list[int]]:
    csvFile = pd.read_csv(fileName).values.tolist()
    allFeatures = []
    allLabel = []
    for row in csvFile:
        if len(row) != 25:
            continue
        features = [
            *row[1:3],
            *row[9:11],
            *row[17:19],
            *row[3:5],
            *row[11:13],
            *row[19:21],
            *row[5:7],
            *row[13:15],
            *row[21:23],
            *row[7:9],
            *row[15:17],
            *row[23:25],
        ]
        allFeatures.append(features)
        allLabel.append(gestureDict[row[0]])
    return allFeatures, allLabel


def loadEKFolder(folderPath: str) -> tuple[list[list[float]], list[int]]:
    allFeatures = []
    allLabel = []
    for fileName in os.listdir(folderPath):
        if fileName.endswith(".csv"):
            features, label = importEKFile(os.path.join(folderPath, fileName))
            allFeatures += features
            allLabel += label
    return allFeatures, allLabel


def exportEKFile(fileName: str, outputPath: str):
    if not os.path.exists(
        os.path.join(os.getcwd(), "Excel_data/v8/Time_series", outputPath)
    ):
        os.mkdir(os.path.join(os.getcwd(), "Excel_data/v8/Time_series", outputPath))
    xls = pd.ExcelFile(
        os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
    )
    for sheetName in xls.sheet_names:
        with open(
            os.path.join(
                os.getcwd(),
                "Excel_data/v8/Time_series",
                outputPath,
                f"{fileName}_{sheetName}.csv",
            ),
            "a",
            newline="",
        ) as csvfile:
            writer = csv.writer(csvfile)
            allData = loadRawDataFile(fileName, [sheetName])
            allFeatures, allLabel = fullEKProcessing(allData)
            for i in range(len(allFeatures)):
                row = [allLabel[i]] + allFeatures[i]
                writer.writerow(row)


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
            online=parameters.convexInc.online
        )
        if parameters.convexDec.online==True and len(kneedle.all_knees)==1 or parameters.convexDec.online==False and kneedle.knee != None:
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
            online=parameters.concaveInc.online
        )
        if parameters.convexDec.online==True and len(kneedle.all_knees)==1 or parameters.convexDec.online==False and kneedle.knee != None:
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
            online=parameters.concaveDec.online
        )
        if parameters.convexDec.online==True and len(kneedle.all_knees)==1 or parameters.convexDec.online==False and kneedle.knee != None:
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
            online=parameters.convexDec.online
        )
        if parameters.convexDec.online==True and len(kneedle.all_knees)==1 or parameters.convexDec.online==False and kneedle.knee != None:
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
    duplicateRange = duplicateRange * 10  # change unit from grid to millisecond
    popList = []
    for ek in ekList:
        if any(
            (ek[0], point) in ekList
            for point in range(ek[1] - duplicateRange, ek[1], 10)
        ):
            popList.append(ek)
    for ek in popList:
        ekList.remove(ek)
    return ekList


def complement(
    ek0: list[tuple[int, int]],
    ek1: list[tuple[int, int]],
    ek2: list[tuple[int, int]],
    sensorRange: int,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
    sensorRange = sensorRange * 10  # change unit from grid to millisecond
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

def orderCheck(ek: list[tuple[int, int]])->list[tuple[int, int]]:
    expected = 0
    i = 0
    duplicate = []
    removed = False
    while True:
        try:
            if ek[i][0] == expected:
                removed = False
                if duplicate!=[]:
                    duplicate.append(ek[i-1])
                    ek.pop(i-1)
                    ek.insert(i-1, (duplicate[0][0], int(sum([d[1]/10 for d in duplicate])//len(duplicate))*10))
                    duplicate = []
                if expected == 3:
                    expected = 0
                else:
                    expected +=1
            elif i>0 and ek[i][0] == ek[i-1][0] and not removed:
                duplicate.append(ek[i])
                ek.pop(i)
                i-=1
            else:
                removed = True
                duplicate = []
                popIdx = i-expected
                for j in range(expected + int(ek[i][0]!=0)):
                    ek.pop(popIdx)
                i-=expected+1
                expected = 0
            i+=1
        except:
            break
    while True:
        try:
            if ek[-1][0] != 3:
                ek.pop(-1)
            else:
                break
        except:
            break        
    return ek

def splitGroup(
    data: pd.DataFrame,
    ek0: list[tuple[int, int]],
    ek1: list[tuple[int, int]],
    ek2: list[tuple[int, int]],
) -> tuple[list[list[int]], list[int]]:
    features = []
    label = []
    pending = []
    for i in range(len(ek0)):
        if ek0[i][0] == 3:
            timeStart = ek0[i-3][1]
            pending = []
            for j in range(3, -1, -1):
                pending+=[
                ek0[i-j][1] - timeStart,
                data["0"][ek0[i-j][1] // 10],
                ek1[i-j][1] - timeStart,
                data["1"][ek1[i-j][1] // 10],
                ek2[i-j][1] - timeStart,
                data["2"][ek2[i-j][1] // 10],
                ]
            features.append(pending)
            label.append(data["gesture"][(features[-1][6] + timeStart) // 10])
    return features, label


def plot(data: pd.DataFrame, sensorNum: int, ekList: list[tuple[int, int]]):
    color = ["go", "ro", "bo", "yo"]
    col = str(sensorNum)
    plt.plot([i * 10 for i in range(len(data[col]))], data[col])
    for ek in ekList:
        plt.plot(ek[1], data[col][ek[1] // 10], color[ek[0]])


def plotAverage(allFeatures: list[list[float]], allLabel: list[int]):
    colors = ["blue", "green", "red", "orange"]
    lineStyle = ["-", "--", ":"]
    label = ["down", "up", "open", "little"]
    avg = [[0 for i in range(24)] for j in range(4)]
    for i in range(len(allFeatures)):
        avg[allLabel[i]] = [avg[allLabel[i]][j] + allFeatures[i][j] for j in range(24)]

    for i in range(4):
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


def fullEKProcessing(data: pd.DataFrame) -> tuple[list[float], int]:
    ek0 = findEK(
        data,
        0,
        EKGroupParameter(
            35,
            1,
            EKParameter(1, 50, 5, 1),
            EKParameter(1, 80, 5, 2),
            EKParameter(1, 40, 5, 2),
            EKParameter(2, 30, 3, 1, True),
        ),
    )
    ek1 = findEK(
        data,
        1,
        EKGroupParameter(
            20,
            1,
            EKParameter(1, 40, 5, 1),
            EKParameter(1, 50, 3, 3),
            EKParameter(1, 50, 3, 2, True),
            EKParameter(1, 20, 3, 1, True),
        ),
    )
    ek2 = findEK(
        data,
        2,
        EKGroupParameter(
            20,
            1,
            EKParameter(1, 40, 5, 1),
            EKParameter(1, 50, 3, 3),
            EKParameter(1, 30, 3, 1, True),
            EKParameter(1, 20, 2, 2, True),
        ),
    )
    # plot(data, 0, ek0)
    # plot(data, 1, ek1)
    # plot(data, 2, ek2)
    ek0 = removeDuplicate(ek0, 30)
    ek1 = removeDuplicate(ek1, 30)
    ek2 = removeDuplicate(ek2, 30)
    # plot(data, 0, ek0)
    # plot(data, 1, ek1)
    # plot(data, 2, ek2)
    ek0, ek1, ek2 = complement(ek0, ek1, ek2, 50)
    # plot(data, 0, ek0)
    # plot(data, 1, ek1)
    # plot(data, 2, ek2)
    ek0 = orderCheck(ek0)
    ek1 = orderCheck(ek1)
    ek2 = orderCheck(ek2)
    ek0, ek1, ek2 = complement(ek0, ek1, ek2, 50)
    features, label = splitGroup(data, ek0, ek1, ek2)
    return features, label

def fullFileProcessing(allData=list[pd.DataFrame]) -> tuple[list[list[float]], list[int]]:
    allFeatures = []
    allLabel = []
    for data in allData:
        features, label = fullEKProcessing(data)
        allFeatures += features
        allLabel += label
    return allFeatures, allLabel

if __name__ == "__main__":
    allData, _ = loadRawDataFile("band2_0115")
    allFeatures, allLabel = fullFileProcessing(allData)
    plotAverage(allFeatures, allLabel)
    print(len(allFeatures), len(allLabel))
