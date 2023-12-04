from kneed import KneeLocator
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import savgol_filter 
def smooth(y, window_length):
    y_smooth = savgol_filter(y,  window_length=window_length, polyorder=2)
    return y_smooth

# fileName = input("File name: ")
fileName = 'band1_222_1130'
xls = pd.ExcelFile(
    os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
)
saveFolder = os.path.join(
    os.getcwd(), "Wristband_plots/versions/v8/Time_series", fileName
)
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
for sheetName in xls.sheet_names:
    if sheetName == 'Sheet':
        continue
    data = xls.parse(sheetName)
    
    # plt.figure()
    # plt.ylim(800, 2900)
    # plt.title(f"{fileName} {sheetName}")
    for col in data.columns:
        t = [i * 10 for i in range(len(data[col]))]
        # plt.plot(smooth(data[col],30))
        # data[col] = smooth(data[col], 30)
        kneedle = KneeLocator(t, data[col], S=2000, curve="convex", direction="decreasing")
        print(kneedle.all_knees)
        kneedle.plot_knee()
        kneedle = KneeLocator(t, data[col], S=2000, curve="convex", direction="increasing")
        print(kneedle.all_knees)
        kneedle.plot_knee()
        plt.show()
        # plt.plot(
        #     [i * 10 for i in range(len(data[col]))], data[col], label=f"Sensor {col}"
        # )
    # plt.ylabel("resistance(ohm)")
    # plt.xlabel("time(ms)")
    # plt.legend(loc="upper right")
    # plt.savefig(
    #     os.path.join(
    #         saveFolder,
    #         f"{sheetName}.png",
    #     )
    # )