from ElbowKnee_all_nSensors import *
from Classifier import *
from Calibration import *
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.text import Text
from functools import partial
from DataParser import *

lastPredict = -1
lastGesture = -1
lastPredictTime = -200
lastGestureTime = -200
neutralFlag = False
# parameters for 1s gesture
ekGroupParameters = (
    [
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
    ],
    30,
    50,
)


def plotAnimate(
    data: pd.DataFrame,
    sensorNum: int,
    ekList: list[tuple[int, int]],
    dataPlots: list[Line2D],
    EKPlots: list[Line2D],
):
    col = str(sensorNum)
    dataPlots[sensorNum].set_data([i * 10 for i in range(len(data[col]))], data[col])
    if len(ekList) == 0:
        for i in range(4):
            EKPlots[sensorNum * 4 + i].set_data([], [])
    else:
        for i, ek in enumerate(ekList):
            EKPlots[sensorNum * 4 + i].set_data([ek[1]], [data[col][ek[1] // 10]])


def generator(dataLength: int):
    row = 0
    while row + 200 < dataLength:
        row += 5
        yield row


def animate(
    row: int,
    classifier: Classifier,
    realtimeData: list[pd.DataFrame],
    linearTransform: list[tuple[float, float]],
    dataPlots: list[Line2D],
    EKPlots: list[Line2D],
    result: Text,
):
    global lastGesture, lastPredictTime, neutralFlag, lastPredict, lastGestureTime
    data = [realtimeData[0].iloc[row : row + 200].reset_index(drop=True)]
    data = transformData(data, linearTransform)[0]
    features, label, ekLists = EKProcessing(data, 3, ekGroupParameters)
    for i in range(len(ekLists)):
        plotAnimate(data, i, ekLists[i], dataPlots, EKPlots)
    if features != []:
        features = timeNormalization(features)
        r = classifier.predict(features)
        ges = gestureReverseDict[r[0]]
        if row - lastGestureTime < 225:
            ges = f"{gestureReverseDict[lastGesture]}_{gestureReverseDict[r[0]]}"
        lastPredictTime = row
        lastPredict = r[0]
        result.set_text(f"expected: {gestureReverseDict[label[0]]} / actual: {ges}")
        neutralFlag = False
    elif (not neutralFlag) and row - lastPredictTime > 100:
        lastGesture = lastPredict
        lastGestureTime = lastPredictTime
        neutralFlag = True
    else:
        result.set_text("neutral")
    return tuple(dataPlots) + tuple(EKPlots), result


if __name__ == "__main__":
    classifier = Classifier()
    trainFileName = "band2_0323"
    testFileName = "band1_0323"
    trainFile, _ = loadRawDataFile(getDefaultFilePath(trainFileName))
    trainMaxMin = findMaxMin(trainFile)
    # tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
    # testFile, calibrationFile = calibrationPartition(
    #     sheetNames, tmpFile, 0.7, 0.3, ["00", "11", "22", "01", "12", "02"]
    # )
    # testFile = maxminNormalization(trainFile, testFile, calibrationFile)
    # trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    # trainFeatures = timeNormalization(trainFeatures)
    # testFeatures, testLabel = fullFileProcessing(testFile, 3)
    # testFeatures = timeNormalization(testFeatures)
    # print(len(trainFeatures), len(testFeatures))
    # acc, accTest = classifier.randomForest(
    #     trainFeatures, trainLabel, testFeatures, testLabel
    # )
    # print(acc, accTest)
    # classifier.saveModel(f"{trainFileName}_{testFileName}.joblib")
    classifier.loadModel(f"{trainFileName}_{testFileName}.joblib")
    # realtimeFileName = "band2_0322"
    # realtimeSheetName = "01_51"
    realtimeFileName = "band2_0323_rep"
    realtimeSheetName = "012_3"
    realtimeTmpFile, realtimeSheetNames = loadRawDataFile(
        getDefaultFilePath(realtimeFileName), [realtimeSheetName]
    )

    # realtimeTestFile, realtimeCalibrationFile = calibrationPartition(
    #     realtimeSheetNames,
    #     realtimeTmpFile,
    #     0.7,
    #     0.3,
    #     ["00", "11", "22", "01", "12", "02"],
    # )
    realtimeTestFile, realtimeCalibrationFile = calibrationPartition(
        realtimeSheetNames,
        realtimeTmpFile,
        0.67,
        0.33,
        ["012"],
    )
    realtimeMaxMin = findMaxMin(realtimeCalibrationFile)
    realtimeLinearTransform = findLinearTransform(trainMaxMin, realtimeMaxMin)
    print(trainMaxMin, realtimeMaxMin, realtimeLinearTransform)
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 2000), ylim=(500, 3500))
    dataPlots = []
    EKPlots = []
    for i in range(3):
        dataPlots.append(ax.plot([], [], linestyle="-")[0])
        EKPlots.append(ax.plot([], [], "go")[0])
        EKPlots.append(ax.plot([], [], "ro")[0])
        EKPlots.append(ax.plot([], [], "bo")[0])
        EKPlots.append(ax.plot([], [], "yo")[0])
    result = ax.text(50, 3200, "")
    anim = FuncAnimation(
        fig,
        partial(
            animate,
            classifier=classifier,
            realtimeData=realtimeTestFile,
            linearTransform=realtimeLinearTransform,
            dataPlots=dataPlots,
            EKPlots=EKPlots,
            result=result,
        ),
        # frames=partial(generator, len(realtimeTestFile[0])),
        # frames=partial(generator, 1400),
        frames=partial(generator, 1700),
        interval=50,
        repeat=False,
    )
    plt.show()
    anim.save(f"realtime_{realtimeFileName}_{realtimeSheetName}.gif", writer="pillow")
