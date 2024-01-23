from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import savgol_filter

def smooth(y, window_length):
    y_smooth = savgol_filter(y, window_length=window_length, polyorder=1)
    return y_smooth

# fileName = input("File name: ")
# fileName = 'band1_222_1130'
fileName = "band2_0115"
xls = pd.ExcelFile(
    os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
)
saveFolder = os.path.join(
    os.getcwd(), "Wristband_plots/versions/v8/Time_series", fileName
)
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
row = len(xls.sheet_names) // 3
column = len(xls.sheet_names) // row
idx = 0

for sheetName in xls.sheet_names:
    idx += 1
    plt.subplot(row, column, idx)
    if sheetName == "Sheet":
        continue
    data = xls.parse(sheetName)
    col = "1"
    t = [i * 10 for i in range(len(data[col]))]
    plt.ylim(750,1500)
    plt.plot(t, data[col])
    data[col] = smooth(data[col], 40)
    concaveDec = {}
    convexDec = {}
    concaveInc = {}
    convexInc = {}
    for i in range(0, len(data[col]) - 180, 10):
        kneedle = KneeLocator(
            t[i : i + 180],
            data[col][i : i + 180],
            S=1,
            curve="convex",
            direction="increasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in convexInc:
                convexInc[kneedle.knee] += 1
            else:
                convexInc[kneedle.knee] = 1
    for i in range(0, len(data[col]) - 150, 6):
        kneedle = KneeLocator(
            t[i : i + 150],
            data[col][i : i + 150],
            S=1,
            curve="concave",
            direction="increasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in concaveInc:
                concaveInc[kneedle.knee] += 1
            else:
                concaveInc[kneedle.knee] = 1
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
    for i in range(0, len(data[col]) - 180, 6):
        kneedle = KneeLocator(
            t[i : i + 180],
            data[col][i : i + 180],
            S=1,
            curve="convex",
            direction="decreasing",
        )
        if kneedle.knee != None:
            if kneedle.knee in convexDec:
                convexDec[kneedle.knee] += 1
            else:
                convexDec[kneedle.knee] = 1
    for c in convexInc:
        if convexInc[c] > 1:
            plt.vlines(c, 750, 1500, colors=["g"])
            print(0, c)
    for c in concaveInc:
        if concaveInc[c] > 2:
            plt.vlines(c, 750, 1500, colors=["r"])
            print(1, c)
    for c in concaveDec:
        if concaveDec[c] > 2:
            plt.vlines(c, 750, 1500, colors=["b"])
            print(2, c)
    for c in convexDec:
        if convexDec[c] > 2:
            plt.vlines(c, 750, 1500, colors=["y"])
            print(3, c)
    plt.title(sheetName)
plt.tight_layout(pad=1.1)
plt.show()
