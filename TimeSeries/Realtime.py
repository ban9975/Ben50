from ElbowKnee_all_nSensors import *
from Classifier import *
from Transfer import *
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.text import Text
from functools import partial

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
        EKParameter(1, 60, 3, 3),
        EKParameter(1, 50, 3, 4),
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
def plotAnimate(data: pd.DataFrame, sensorNum: int, ekList: list[tuple[int, int]], dataPlots: list[Line2D], EKPlots: list[Line2D]):
    col = str(sensorNum)
    dataPlots[sensorNum].set_data([i * 10 for i in range(len(data[col]))], data[col])
    if len(ekList)==0:
        for i in range(4):
            EKPlots[sensorNum*4+i].set_data([], [])
    else:
        for i, ek in enumerate(ekList):
            EKPlots[sensorNum*4+i].set_data([ek[1]], [data[col][ek[1] // 10]])
def generator(dataLength: int):
    row = 0
    while row+200 < dataLength:
        row+=5
        yield row
def animate(row: int, realtimeData: list[pd.DataFrame], linearTransform: list[tuple[float, float]], dataPlots: list[Line2D], EKPlots: list[Line2D], result: Text):
    data = [realtimeData[0].iloc[row:row+200].reset_index(drop=True)]
    data = transformData(data, linearTransform)[0]
    features, label, ekLists = EKProcessing(data, 3, ekGroupParameters)
    for i in range(len(ekLists)):
        plotAnimate(data, i, ekLists[i], dataPlots, EKPlots)
    if features!=[]:
        r = classifier.predict(features)
        result.set_text(f"expected: {str(label)} / actual: {str(r)}")
    else:
        result.set_text("neutral")
    return tuple(dataPlots)+tuple(EKPlots), result

if __name__ == "__main__":
    classifier = Classifier()
    trainFile, _ = DataParser.loadRawDataFile("band2_0315")
    testFile, _ = DataParser.loadRawDataFile("band1_0315")
    trainMaxMin = findMaxMin(trainFile)
    testLinearTransform = findLinearTransform(trainMaxMin, findMaxMin(testFile))
    testFile = transformData(testFile, testLinearTransform)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = normalize(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = normalize(testFeatures)    
    print(len(trainFeatures), len(testFeatures))
    acc, accTest = classifier.randomForest(trainFeatures, trainLabel, testFeatures, testLabel)
    print(acc, accTest)
    realtimeData, _ = loadRawDataFile("band2_0316", ["0123_5"])
    realtimeMaxMin = findMaxMin(realtimeData)
    realtimeLinearTransform = findLinearTransform(trainMaxMin, realtimeMaxMin)
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
    plt.title("band2_0316_0123_5")
    anim = FuncAnimation(fig, partial(animate, realtimeData = realtimeData, linearTransform = realtimeLinearTransform, dataPlots = dataPlots, EKPlots = EKPlots, result = result), frames=partial(generator, len(realtimeData[0])), interval = 50, repeat=False)
    plt.show()
    anim.save('realtime_band2_0316.gif', writer='pillow')

