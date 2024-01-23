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
sheetName = '00_51'
data = xls.parse(sheetName)
col = "1"
t = [i * 10 for i in range(len(data[col]))]
plt.plot(t, data[col])
data[col] = smooth(data[col], 40)
plt.ylim(500,1200)
concaveInc = {}
for i in range(0, len(data[col]) - 200, 5):
    kneedle = KneeLocator(
        t[i : i + 200],
        data[col][i : i + 200],
        S=1,
        curve="concave",
        direction="increasing",
    )
    if kneedle.knee != None:
        if kneedle.knee in concaveInc:
            concaveInc[kneedle.knee] += 1
        else:
            concaveInc[kneedle.knee] = 1
for c in concaveInc:
    if concaveInc[c] > 2:
        plt.vlines(c, 500, 1200, colors=["r"])
plt.title(sheetName)
plt.show()
