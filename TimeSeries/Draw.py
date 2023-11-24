import matplotlib.pyplot as plt
import pandas as pd
import os

fileName = input("File name: ")
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
    plt.figure()
    plt.ylim(800, 2900)
    plt.title(f"{fileName} {sheetName}")
    for col in data.columns:
        plt.plot(
            [i * 10 for i in range(len(data[col]))], data[col], label=f"Sensor {col}"
        )
    plt.ylabel("resistance(ohm)")
    plt.xlabel("time(ms)")
    plt.legend(loc="upper right")
    plt.savefig(
        os.path.join(
            saveFolder,
            f"{sheetName}.png",
        )
    )
