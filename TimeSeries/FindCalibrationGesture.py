import DataParser
import sys
import matplotlib.pyplot as plt
import pandas as pd
def findMaxMinGesture(fileName: str)->list[int]:
    file, sheetName = DataParser.loadRawDataFile(fileName)
    allMaxxGesture = []
    allMinnGesture = []
    for s in range(len(file)):
        maxx = [0, 0, 0]
        maxxGesture = [0, 0, 0]
        maxxTime = [0, 0, 0]
        minn = [sys.maxsize, sys.maxsize, sys.maxsize]
        minnGesture = [0, 0, 0]
        minnTime = [0, 0, 0]        
        sheet = file[s]
        for i in range(3):
            col = str(i)
            for row in range(len(sheet[col])):
                if sheet[col][row]>maxx[i]:
                    maxx[i] = sheet[col][row]
                    maxxGesture[i] = sheet['gesture'][row-50 if row>50 else row]
                    maxxTime[i] = row*10
                if sheet[col][row]<minn[i]:
                    minn[i] = sheet[col][row]
                    minnGesture[i] = sheet['gesture'][row-50 if row>50 else row]
                    minnTime[i] = row*10
        # plot(fileName, sheetName[s], sheet, maxxTime, minnTime)
        # print(maxx, maxxGesture, maxxTime)
        # print(minn, minnGesture, minnTime)
        allMaxxGesture+=maxxGesture
        allMinnGesture+=minnGesture
    return allMaxxGesture + allMinnGesture
def plot(fileName: str, sheetName: str, data: pd.DataFrame, maxxTime: list[float], minnTime: list[float]):
    plt.figure()
    plt.ylim(500, 3500)
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
    for sensorMax in maxxTime:
        plt.vlines(sensorMax, 500, 3500, colors=["lime"])
    for sensorMin in minnTime:
        plt.vlines(sensorMin, 500, 3500, colors=["salmon"])    
    plt.ylabel("resistance(ohm)")
    plt.xlabel("time(ms)")
    plt.legend(loc="lower right")
    plt.show()

if __name__ == "__main__":
    fileNames = ["band1_0310", "band1_0311", "band2_0310", "band2_0311"]
    gestureSet = set()
    for file in fileNames:
        gesture = findMaxMinGesture(file)
        for g in gesture:
            gestureSet.add(g)
    print(gestureSet)
