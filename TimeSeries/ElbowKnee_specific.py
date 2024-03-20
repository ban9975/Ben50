from ElbowKnee_all_nSensors import *
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.signal import savgol_filter


def smooth(y, window_length):
    y_smooth = savgol_filter(y, window_length=window_length, polyorder=1)
    return y_smooth


# fileName = input("File name: ")
# fileName = 'band1_222_1130'
fileName = "band2_0315"
xls = pd.ExcelFile(
    os.path.join(os.getcwd(), "Excel_data/v8/Time_series", f"{fileName}.xlsx")
)
saveFolder = os.path.join(
    os.getcwd(), "Wristband_plots/versions/v8/Time_series", fileName
)
if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)
sheetName = '0123_5'
data = xls.parse(sheetName)
data = data.iloc[200:400].reset_index(drop=True)

plt.ylim(500,3000)
# ek0 = findEK(
#     data,
#     0,
#     EKGroupParameter(
#         90,
#         2,
#         EKParameter(1, 250, 10, 1),
#         EKParameter(1, 300, 5, 2),
#         EKParameter(1, 300, 10, 3),
#         EKParameter(1, 150, 4, 6),
#     ),
# )
# plot(data, 0, ek0)
# ek1 = findEK(
#     data,
#     1,
#     EKGroupParameter(
#         40,
#         1,
#         EKParameter(1, 180, 10, 0),
#         EKParameter(1, 150, 6, 0),
#         EKParameter(1, 210, 7, 0),
#         EKParameter(1, 150, 6, 0),
#     ),
# )
# plot(data, 1, ek1)
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
plot(data, 2, ek2)
plt.title(f"{fileName} {sheetName}")
plt.show()
