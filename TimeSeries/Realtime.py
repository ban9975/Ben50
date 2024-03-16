from ElbowKnee_all_nSensors import *
from Classifier import *
from Transfer import *
from matplotlib.animation import FuncAnimation

classifier = Classifier()
fig = plt.figure()
ax = plt.axes(xlim=(0, 2000), ylim=(500, 3200))
dataPlots = []
EKPlots = []
for i in range(3):
    dataPlots.append(ax.plot([], [],linestyle='-')[0])
    EKPlots.append(ax.plot([], [], "go")[0])
    EKPlots.append(ax.plot([], [], "ro")[0])
    EKPlots.append(ax.plot([], [], "bo")[0])
    EKPlots.append(ax.plot([], [], "yo")[0])
result = ax.text(50, 3000, "")
allData, _ = loadRawDataFile("band2_0316", ["0123_5"])
row = 0
# parameters for 1s gesture
ekGroupParameters = ([
    EKGroupParameter(
        35,
        2,
        EKParameter(1, 50, 5, 1),
        EKParameter(1, 80, 5, 2),
        EKParameter(1, 40, 5, 2),
        EKParameter(2, 30, 3, 1, True),
    ),
    EKGroupParameter(
        40,
        2,
        EKParameter(1, 40, 3, 2),
        EKParameter(1, 50, 3, 2),
        EKParameter(1, 60, 3, 3, False),
        EKParameter(1, 50, 3, 4, False),
    ),
    EKGroupParameter(
        20,
        1,
        EKParameter(1, 40, 5, 1),
        EKParameter(1, 50, 3, 3),
        EKParameter(1, 30, 3, 1, True),
        EKParameter(1, 20, 2, 2, True),
    ),
], 30, 50)
def plotAnimate(data: pd.DataFrame, sensorNum: int, ekList: list[tuple[int, int]]):
    col = str(sensorNum)
    dataPlots[sensorNum].set_data([i * 10 for i in range(len(data[col]))], data[col])
    if len(ekList)==0:
        for i in range(4):
            EKPlots[sensorNum*4+i].set_data([], [])
    else:
        for i, ek in enumerate(ekList):
            EKPlots[sensorNum*4+i].set_data([ek[1]], [data[col][ek[1] // 10]])
def generator():
    global row
    row = 0
    while row+200 < len(allData[0]):
        row+=5
        yield row
def animate(row):
    data = allData[0].iloc[row:row+200].reset_index(drop=True)
    features, label, ekLists = EKProcessing(data, 3, ekGroupParameters)
    for i in range(len(ekLists)):
        plotAnimate(data, i, ekLists[i])
    if features!=[]:
        r = classifier.predict(features)
        result.set_text(f"expected: {str(label)} / actual: {str(r)}")
    else:
        result.set_text("neutral")
    return tuple(dataPlots)+tuple(EKPlots), result

if __name__ == "__main__":
    trainFile, _ = DataParser.loadRawDataFile("band2_0315")
    testFile, _ = DataParser.loadRawDataFile("band1_0315")
    linearTransform = findLinearTransform(findMaxMin(trainFile), findMaxMin(testFile))
    testFile = transformData(testFile, linearTransform)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = normalize(trainFeatures)
    print(len(trainFeatures))
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = normalize(testFeatures)
    acc, accTest = classifier.randomForest(trainFeatures, trainLabel, testFeatures, testLabel)
    plt.title("band2_0316_0123_5")
    anim = FuncAnimation(fig, animate, frames=generator, interval = 50, repeat=False)
    plt.show()
    anim.save('realtime_band2_0316.gif', writer='pillow')

