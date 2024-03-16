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
data = data.iloc[2000:5000].reset_index(drop=True)

plt.ylim(500,3000)
# ek0 = findEK(
#     data,
#     0,
#     EKGroupParameter(
#         35,
#         1,
#         EKParameter(1, 50, 5, 1),
#         EKParameter(1, 80, 5, 2),
#         EKParameter(1, 40, 5, 2),
#         EKParameter(2, 30, 3, 1, True),
#     ),
# )
# plot(data, 0, ek0)
ek1 = findEK(
    data,
    1,
    EKGroupParameter(
        50,
        1,
        EKParameter(1, 40, 3, 2),
        EKParameter(1, 50, 3, 2),
        EKParameter(1, 60, 3, 3, False),
        EKParameter(1, 50, 3, 4, False),
    ),
)
plot(data, 1, ek1)
# ek2 = findEK(
#     data,
#     2,
#     EKGroupParameter(
#         20,
#         1,
#         EKParameter(1, 40, 5, 1),
#         EKParameter(1, 50, 3, 3),
#         EKParameter(1, 30, 3, 1, True),
#         EKParameter(1, 20, 2, 2, True),
#     ),
# )
# plot(data, 2, ek2)
plt.title(sheetName)
plt.show()
