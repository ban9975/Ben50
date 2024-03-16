from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
from DataParser import *
from scipy.signal import savgol_filter
from copy import deepcopy


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
    ekLists: list[list[tuple[int, int]]],
    sensorRange: int,
) -> list[list[tuple[int, int]]]:
    sensorRange = sensorRange * 10  # change unit from grid to millisecond
    if len(ekLists)<2:
        return
    ekListsCopy = deepcopy(ekLists)
    for j, ekList in enumerate(ekListsCopy):      
        while len(ekList)>0:
            inEkTime = []
            inEkIdx = []
            inEkRemain = [n for n in range(len(ekListsCopy))]
            inEkRemain.remove(j)
            for point in range(ekList[0][1] - sensorRange, ekList[0][1] + sensorRange, 10):
                for k in range(len(ekListsCopy)):
                    if j==k:
                        continue
                    if (ekList[0][0], point) in ekListsCopy[k] and k in inEkRemain:
                        inEkTime.append(point//10)
                        inEkRemain.remove(k)
                        inEkIdx.append(k)
            if len(inEkRemain)>=(len(ekListsCopy)+1)//2:
                for k in range(len(inEkIdx)):
                    ekListsCopy[inEkIdx[k]].remove((ekList[0][0], inEkTime[k]*10))
                    ekLists[inEkIdx[k]].remove((ekList[0][0], inEkTime[k]*10))
                ekLists[j].remove(ekList[0])
                ekListsCopy[j].remove(ekList[0])
            else:
                inEkTime.append(ekList[0][1]//10)
                inEkIdx.append(j)
                for k in inEkRemain:
                    ekLists[k].append((ekList[0][0], int(sum(inEkTime)//len(inEkTime) * 10)))
                for k in range(len(inEkIdx)):
                    ekListsCopy[inEkIdx[k]].remove((ekList[0][0], inEkTime[k]*10))                
    for ekList in ekLists:
        ekList.sort(key=lambda x: x[1])
    return ekLists

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
    ekLists: list[list[tuple[int, int]]]
) -> tuple[list[list[int]], list[int]]:
    features = []
    label = []
    pending = []
    for i in range(0, len(ekLists[0]), 4):
        timeStart = ekLists[0][i][1]
        pending = []
        for j in range(4):
            for k in range(len(ekLists)):
                pending +=[ekLists[k][i+j][1] - timeStart, data[str(k)][ekLists[k][i+j][1] // 10]]
        features.append(pending)
        label.append(data["gesture"][(features[-1][len(ekLists)*2] + timeStart) // 10])
    return features, label


def plot(data: pd.DataFrame, sensorNum: int, ekList: list[tuple[int, int]]):
    color = ["go", "ro", "bo", "yo"]
    col = str(sensorNum)
    plt.plot([i * 10 for i in range(len(data[col]))], data[col])
    for ek in ekList:
        plt.plot(ek[1], data[col][ek[1] // 10], color[ek[0]])

def EKProcessing(data: pd.DataFrame, nSensors: int, ekGroupParameters: tuple[list[EKGroupParameter], int, int]) -> tuple[list[float], int]:
    ekLists = []
    for i in range(nSensors):
        ekLists.append(findEK(data, i, ekGroupParameters[0][i]))
    for i in range(nSensors):
        ekLists[i] = removeDuplicate(ekLists[i], ekGroupParameters[1])

    ekLists = complement(ekLists, ekGroupParameters[2])
    for i in range(nSensors):
        ekLists[i] = orderCheck(ekLists[i])
    ekLists = complement(ekLists, ekGroupParameters[2])
    # for i in range(len(ekLists)):
    #     plot(data, i, ekLists[i])
    # plt.show()
    features, label = splitGroup(data, ekLists)
    return features, label, ekLists

def fullFileProcessing(allData:list[pd.DataFrame], nSensors: int) -> tuple[list[list[float]], list[int]]:
    allFeatures = []
    allLabel = []
    ekGroupParameters = ([
        EKGroupParameter(
            90,
            2,
            EKParameter(1, 250, 10, 1),
            EKParameter(1, 300, 5, 2),
            EKParameter(1, 300, 10, 3),
            EKParameter(1, 150, 4, 6),
        ),
        EKGroupParameter(
            40,
            1,
            EKParameter(1, 180, 10, 1),
            EKParameter(1, 150, 6, 2),
            EKParameter(1, 210, 7, 2),
            EKParameter(1, 150, 6, 2),
        ),
        EKGroupParameter(
            40,
            1,
            EKParameter(1, 180, 9, 1),
            EKParameter(1, 150, 6, 2),
            EKParameter(1, 140, 7, 2),
            EKParameter(1, 180, 5, 3),
        ),
        EKGroupParameter(
            40,
            1,
            EKParameter(1, 180, 10, 1),
            EKParameter(1, 150, 6, 2),
            EKParameter(1, 210, 7, 2),
            EKParameter(1, 150, 6, 2),
        ),
    ], 70, 70)
    for data in allData:
        features, label, _ = EKProcessing(data, nSensors, ekGroupParameters)
        allFeatures += features
        allLabel += label
    return allFeatures, allLabel

if __name__ == "__main__":
    allData, _ = loadRawDataFile("band2_0315")
    allFeatures, allLabel = fullFileProcessing(allData, 3)
    print(len(allFeatures), len(allLabel))
