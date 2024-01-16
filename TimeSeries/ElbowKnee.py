from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import savgol_filter


def smooth(y, window_length):
    y_smooth = savgol_filter(y, window_length=window_length, polyorder=2)
    return y_smooth


# fileName = input("File name: ")
# fileName = 'band1_222_1130'
fileName = "band2_1226"
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
    col = "0"
    t = [i * 10 for i in range(len(data[col]))]
    data[col] = smooth(data[col], 70)
    plt.plot(t, data[col])
    concaveDec = {}
    convexDec = {}
    concaveInc = {}
    convexInc = {}
    for i in range(0, len(data[col]) - 300, 5):
        kneedle = KneeLocator(
            t[i : i + 300],
            data[col][i : i + 300],
            S=1,
            curve="concave",
            direction="increasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in concaveInc:
                concaveInc[kneedle.knee] += 1
            else:
                concaveInc[kneedle.knee] = 1
    for i in range(0, len(data[col]) - 300, 10):
        kneedle = KneeLocator(
            t[i : i + 300],
            data[col][i : i + 300],
            S=1,
            curve="convex",
            direction="increasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in convexInc:
                convexInc[kneedle.knee] += 1
            else:
                convexInc[kneedle.knee] = 1
    for i in range(0, len(data[col]) - 300, 10):
        kneedle = KneeLocator(
            t[i : i + 300],
            data[col][i : i + 300],
            S=1,
            curve="concave",
            direction="decreasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in concaveDec:
                concaveDec[kneedle.knee] += 1
            else:
                concaveDec[kneedle.knee] = 1
    for i in range(0, len(data[col]) - 220, 5):
        kneedle = KneeLocator(
            t[i : i + 220],
            data[col][i : i + 220],
            S=1,
            curve="convex",
            direction="decreasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in convexDec:
                convexDec[kneedle.knee] += 1
            else:
                convexDec[kneedle.knee] = 1
    for c in concaveInc:
        if concaveInc[c] > 2:
            plt.vlines(c, 1000, 3000, colors=["r"])
    for c in convexInc:
        if convexInc[c] > 1:
            plt.vlines(c, 1000, 3000, colors=["g"])
    for c in concaveDec:
        if concaveDec[c] > 3:
            plt.vlines(c, 1000, 3000, colors=["b"])
    for c in convexDec:
        if convexDec[c] > 4:
            plt.vlines(c, 1000, 3000, colors=["y"])
    plt.show()
