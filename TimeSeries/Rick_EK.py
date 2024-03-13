from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import savgol_filter


def smooth(y, window_length):
    y_smooth = savgol_filter(y, window_length=window_length, polyorder=1)
    return y_smooth

def data_edit(sensors):
    maxDataLen = max(len(sensors[0]), len(sensors[1]), len(sensors[2]))
    for i in range(3):
        while len(sensors[i]) < maxDataLen:
            sensors[i].append(0)
    i = 0
    while True:
        try:
            distance01 = sensors[0][i] - sensors[1][i]
            distance12 = sensors[1][i] - sensors[2][i]
            distance20 = sensors[2][i] - sensors[0][i]
            if abs(distance01) > 600 and abs(distance12) > 600 and abs(distance20) > 600:
                if sensors[0][i] == min(sensors[0][i], sensors[1][i], sensors[2][i]):
                    del sensors[0][i]
                elif sensors[1][i] == min(sensors[0][i], sensors[1][i], sensors[2][i]):
                    del sensors[1][i]
                else:
                    del sensors[2][i]
            elif abs(distance01) > 600 and abs(distance20) > 600:
                if distance01 < 0:
                    del sensors[0][i]
                else:
                    sensors[0].insert(i, (sensors[1][i] +sensors[2][i]) // 2)
                    i += 1
            elif abs(distance01) > 600 and abs(distance12) > 600:
                if distance12 < 0:
                    del sensors[1][i]
                else:
                    sensors[1].insert(i, (sensors[0][i] +sensors[2][i]) // 2)
                    i += 1
            elif abs(distance12) > 600 and abs(distance20) > 600:
                if distance20 < 0:
                    del sensors[2][i]
                else:
                    sensors[2].insert(i, (sensors[0][i] +sensors[1][i]) // 2)
                    i += 1
            else:
                i += 1
        except:
            break
    for i in range(3):
         length = len(sensors[i])
         j = 0
         while j < length:
            if (sensors[i][j] == 0):
                del sensors[i][j]
                length -= 1
            else:
                j += 1
    minDataLen = min(len(sensors[0]), len(sensors[1]), len(sensors[2]))
    for i in range(3):
        sensors[i] = sensors[i][0:minDataLen]

def data_check(foldingPoint1TimeSet, foldingPoint2TimeSet, foldingPoint3TimeSet, foldingPoint4TimeSet):
    for i in range(3):
        startPoint = foldingPoint1TimeSet[i][0]
        while foldingPoint2TimeSet[i][0] < startPoint:
            del foldingPoint2TimeSet[i][0]
        while foldingPoint3TimeSet[i][0] < startPoint:
            del foldingPoint3TimeSet[i][0]
        while foldingPoint4TimeSet[i][0] < startPoint:
            del foldingPoint4TimeSet[i][0]
        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0
        while True:
            try:
                if (foldingPoint1TimeSet[i][f1] <= foldingPoint2TimeSet[i][f2]):
                    if (foldingPoint2TimeSet[i][f2] - foldingPoint1TimeSet[i][f1] < 1500):
                        f1 += 1
                    else:
                        del foldingPoint1TimeSet[i][f1]
                        continue
                else:
                    del foldingPoint2TimeSet[i][f2]
                    continue
                if (foldingPoint2TimeSet[i][f2] <= foldingPoint3TimeSet[i][f3]):
                    if (foldingPoint3TimeSet[i][f3] - foldingPoint2TimeSet[i][f2] < 2500):
                        f2 += 1
                    else:
                        f1 -= 1
                        del foldingPoint1TimeSet[i][f1]
                        del foldingPoint2TimeSet[i][f2]
                        continue
                else:
                    f1 -= 1
                    del foldingPoint3TimeSet[i][f3]
                    continue
                if (foldingPoint3TimeSet[i][f3] <= foldingPoint4TimeSet[i][f4]):
                    if (foldingPoint4TimeSet[i][f4] - foldingPoint3TimeSet[i][f3] < 1500):
                        f3 += 1
                    else: 
                        f1 -= 1
                        f2 -= 1
                        del foldingPoint1TimeSet[i][f1]
                        del foldingPoint2TimeSet[i][f2]
                        del foldingPoint3TimeSet[i][f3]
                        continue
                else:
                    f1 -= 1
                    f2 -= 1
                    del foldingPoint4TimeSet[i][f4]
                    continue
                if (foldingPoint4TimeSet[i][f4] <= foldingPoint1TimeSet[i][f1]):
                    f4 += 1
                else:
                    f1 -= 1
                    f2 -= 1
                    f3 -= 1
                    del foldingPoint1TimeSet[i][f1 + 1]
                    continue
            except:
                break
    
    
    for i in range(3):
        length = min(len(foldingPoint1TimeSet[i]), len(foldingPoint2TimeSet[i]), len(foldingPoint3TimeSet[i]), len(foldingPoint4TimeSet[i]))
        foldingPoint1TimeSet[i] =  foldingPoint1TimeSet[i][0:length]
        foldingPoint2TimeSet[i] =  foldingPoint2TimeSet[i][0:length]
        foldingPoint3TimeSet[i] =  foldingPoint3TimeSet[i][0:length]
        foldingPoint4TimeSet[i] =  foldingPoint4TimeSet[i][0:length]
    

#fileName = 'band1_222_1130'
fileName = "127-o-o"
xls = pd.ExcelFile(
    os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
)
saveFolder = os.path.join(
    os.getcwd(), "Wristband_plots/versions/v8/Time_series", fileName
)
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
for sheetName in xls.sheet_names:
    if sheetName == "Sheet":
        continue
    data = xls.parse(sheetName)
    cols = ["0", "1", "2"]
    #cols = ["0"]
    foldingPoint1TimeSet = []
    foldingPoint2TimeSet = []
    foldingPoint3TimeSet = []
    foldingPoint4TimeSet = []
    foldingPoint1ResistSet = []
    foldingPoint2ResistSet = []
    foldingPoint3ResistSet = []
    foldingPoint4ResistSet = []

    for col in cols: 
        t = [i * 10 for i in range(len(data[col]))]
        data[col] = smooth(data[col], 40)
        plt.plot(t, data[col])
        concaveDec = {}
        convexDec = {}
        concaveInc = {}
        convexInc = {}
        for i in range(0, len(data[col]) - 180, 10):
            kneedle = KneeLocator(
                t[i : i + 180],
                data[col][i : i + 180],
                S=1,
                curve="concave",
                direction="increasing",
            )
            if kneedle.knee != None:
                if kneedle.knee in concaveInc:
                    concaveInc[kneedle.knee] += 1
                else:
                    concaveInc[kneedle.knee] = 1
        for i in range(0, len(data[col]) - 150, 6):
            kneedle = KneeLocator(
                t[i : i + 150],
                data[col][i : i + 150],
                S=1,
                curve="convex",
                direction="increasing",
            )
            if kneedle.knee != None:
                if kneedle.knee in convexInc:
                    convexInc[kneedle.knee] += 1
                else:
                    convexInc[kneedle.knee] = 1
        for i in range(0, len(data[col]) - 210, 7):
            kneedle = KneeLocator(
                t[i : i + 210],
                data[col][i : i + 210],
                S=1,
                curve="concave",
                direction="decreasing",
            )
            if kneedle.knee != None:
                if kneedle.knee in concaveDec:
                    concaveDec[kneedle.knee] += 1
                else:
                    concaveDec[kneedle.knee] = 1
        for i in range(0, len(data[col]) - 150, 6):
            kneedle = KneeLocator(
                t[i : i + 150],
                data[col][i : i + 150],
                S=1,
                curve="convex",
                direction="decreasing",
            )
            if kneedle.knee != None:
                if kneedle.knee in convexDec:
                    convexDec[kneedle.knee] += 1
                else:
                    convexDec[kneedle.knee] = 1

        foldingPoint1Time = []
        foldingPoint2Time = []
        foldingPoint3Time = []
        foldingPoint4Time = []
        temp = -1
        for point in convexInc:
            if convexInc[point] > 2 and point - temp > 750:
                temp = point
                foldingPoint1Time.append(point)
        temp = -1
        for point in concaveInc:
            if concaveInc[point] > 1 and point - temp > 750:
                temp = point
                foldingPoint2Time.append(point)
        temp = -1
        for point in concaveDec:
            if concaveDec[point] > 2 and point - temp > 750:
                temp = point
                foldingPoint3Time.append(point)
        temp = -1
        for point in convexDec:
            if convexDec[point] > 2 and point - temp > 750:
                temp = point
                foldingPoint4Time.append(point)

        foldingPoint1TimeSet.append(foldingPoint1Time)
        foldingPoint2TimeSet.append(foldingPoint2Time)
        foldingPoint3TimeSet.append(foldingPoint3Time)
        foldingPoint4TimeSet.append(foldingPoint4Time)
        #plt.vlines(foldingPoint1Time, 1000, 3000, color = "g")
        #plt.vlines(foldingPoint2s, 1000, 3000, color = "r")
        #plt.vlines(foldingPoint3s, 1000, 3000, color = "b")
        #plt.vlines(foldingPoint4s, 1000, 3000, color = "y")
    
    data_edit(foldingPoint1TimeSet)
    data_edit(foldingPoint2TimeSet)
    data_edit(foldingPoint3TimeSet)
    data_edit(foldingPoint4TimeSet)
    data_check(foldingPoint1TimeSet, foldingPoint2TimeSet, foldingPoint3TimeSet, foldingPoint4TimeSet)    
    data_edit(foldingPoint1TimeSet)
    data_edit(foldingPoint2TimeSet)
    data_edit(foldingPoint3TimeSet)
    data_edit(foldingPoint4TimeSet)
    
    
    for col in cols:
        foldingPoint1Resist = []
        foldingPoint2Resist = []
        foldingPoint3Resist = []
        foldingPoint4Resist = []
        for time in foldingPoint1TimeSet[int(col)]:
            foldingPoint1Resist.append(data[col][time // 10])
        for time in foldingPoint2TimeSet[int(col)]:
            foldingPoint2Resist.append(data[col][time // 10])
        for time in foldingPoint3TimeSet[int(col)]:
            foldingPoint3Resist.append(data[col][time // 10])
        for time in foldingPoint4TimeSet[int(col)]:
            foldingPoint4Resist.append(data[col][time // 10])
        plt.plot(foldingPoint1TimeSet[int(col)], foldingPoint1Resist, "o", color = "g")
        plt.plot(foldingPoint2TimeSet[int(col)], foldingPoint2Resist, "o", color = "r")
        plt.plot(foldingPoint3TimeSet[int(col)], foldingPoint3Resist, "o", color = "b")
        plt.plot(foldingPoint4TimeSet[int(col)], foldingPoint4Resist, "o", color = "y")
        foldingPoint1ResistSet.append(foldingPoint1Resist)
        foldingPoint2ResistSet.append(foldingPoint2Resist)
        foldingPoint3ResistSet.append(foldingPoint3Resist)
        foldingPoint4ResistSet.append(foldingPoint4Resist)
    plt.show()

    # data output
    dataset = []
    for i in range(len(foldingPoint1TimeSet[0])):
        current = [data["gesture"][foldingPoint2TimeSet[0][i] // 10]]
        for j in range(3):
            current.extend([foldingPoint1TimeSet[j][i] - foldingPoint1TimeSet[0][i], foldingPoint1ResistSet[j][i],\
                            foldingPoint2TimeSet[j][i] - foldingPoint1TimeSet[0][i], foldingPoint2ResistSet[j][i],\
                            foldingPoint3TimeSet[j][i] - foldingPoint1TimeSet[0][i], foldingPoint3ResistSet[j][i],\
                            foldingPoint4TimeSet[j][i] - foldingPoint1TimeSet[0][i], foldingPoint4ResistSet[j][i]])
        dataset.append(current)
    df = pd.DataFrame(dataset)
    df.to_csv("./trainData/" + fileName + "-" + sheetName + ".csv", index = False)