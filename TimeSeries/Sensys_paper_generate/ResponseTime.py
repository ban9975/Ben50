import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from ElbowKnee_all_nSensors import *

fileName = input("File name: ")
saveFolder = os.path.join(os.getcwd(), "../Sensys 2024")

sheetNames = ["00_5", "11_5", "22_5"]
colors = [
    "#a4c2f4",
    "#6d9eeb",
    "#3c78d8",
    "#ea9999",
    "#e06666",
    "#cc0000",
    "#b6d7a8",
    "#93c47d",
    "#6aa84f",
]
label = ["down", "up", "open", "little"]
file, _ = loadRawDataFile(getDefaultFilePath(fileName), sheetNames)
features, label, ekLists = EKProcessing(file[0], 3, offlineEKGroupParameters)
file[0] = file[0].drop(["gesture"], axis=1)
for j in range(3):
    plt.plot(
        [
            i * 10
            for i in range(
                len(
                    file[0][
                        (ekLists[0][0][1] - 200) // 10 : (ekLists[0][3][1] + 200) // 10
                    ]
                )
            )
        ],
        file[0][(ekLists[0][0][1] - 200) // 10 : (ekLists[0][3][1] + 200) // 10][
            str(j)
        ],
        label=f"down_{j}",
        color=colors[j],
    )
features, label, ekLists = EKProcessing(file[1], 3, offlineEKGroupParameters)
file[1] = file[1].drop(["gesture"], axis=1)
for j in range(3):
    plt.plot(
        [
            i * 10
            for i in range(
                len(
                    file[1][
                        (ekLists[0][0][1] - 200) // 10 : (ekLists[0][3][1] + 200) // 10
                    ]
                )
            )
        ],
        file[1][(ekLists[0][0][1] - 200) // 10 : (ekLists[0][3][1] + 200) // 10][
            str(j)
        ],
        label=f"up_{j}",
        color=colors[3 + j],
    )
features, label, ekLists = EKProcessing(file[2], 3, offlineEKGroupParameters)
file[2] = file[2].drop(["gesture"], axis=1)
for j in range(3):
    plt.plot(
        [
            i * 10
            for i in range(
                len(
                    file[2][
                        (ekLists[0][0][1] - 200) // 10 : (ekLists[0][3][1] + 200) // 10
                    ]
                )
            )
        ],
        file[2][(ekLists[0][0][1] - 200) // 10 : (ekLists[0][3][1] + 200) // 10][
            str(j)
        ],
        label=f"open_{j}",
        color=colors[6 + j],
    )
# plt.title("Response time")
plt.ylabel("resistance(ohm)")
plt.xlabel("time(ms)")
# plt.legend(loc="upper right")
plt.legend(loc="upper center", ncol=3, fancybox=True)
plt.ylim(500, 3200)
plt.savefig(
    os.path.join(
        saveFolder,
        f"{fileName}_response_time.png",
    )
)
plt.show()
