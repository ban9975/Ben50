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
    os.makedirs(saveFolder, exist_ok=True)
for sheetName in xls.sheet_names:
    data = xls.parse(sheetName)
    plt.figure()
    plt.ylim(500, 3200)
    plt.title(f"{fileName} {sheetName}")
    for col in data.columns:
        if col == "gesture":
            plt.plot(
                [i * 10 for i in range(len(data[col]))],
                [i * 50 + 3000 for i in data[col]],
                label="gesture",
            )
            continue
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
