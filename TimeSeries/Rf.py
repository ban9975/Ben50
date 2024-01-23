from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from ElbowKnee_all import *


def runRf(trainFeatures: list[list[int]], trainLabel: list[int], testFeatures: list[list[int]], testLabel: list[int])->tuple[float]:
    x_train, x_test, y_train, y_test = train_test_split(
        trainFeatures, trainLabel, train_size=0.7, random_state=9999
    )
    model = RandomForestClassifier(
        random_state=9999,
    )
    model.fit(x_train, y_train)
    expected_train = y_test
    actual_train = model.predict(x_test)
    expected_test = testLabel
    actual_test = model.predict(testFeatures)
    acc = accuracy_score(expected_train, actual_train)
    accTest = accuracy_score(expected_test, actual_test)
    confusionMatrix(expected_test, actual_test)
    print(actual_test)
    return acc, accTest

def confusionMatrix(expected, actual):
    test_matrix = confusion_matrix(expected, actual)
    disp = ConfusionMatrixDisplay(test_matrix)
    disp.plot()
    plt.show()


if __name__ == "__main__":
    trainData = loadFile("band2_0115")
    trainFeatures = []
    trainLabel = []
    for data in trainData:
        ek0 = findEK(
            data,
            0,
            EKGroupParameter(
                90,
                2,
                EKParameter(1, 250, 10, 1),
                EKParameter(1, 300, 5, 2),
                EKParameter(1, 300, 10, 3),
                EKParameter(1, 150, 4, 6),
            ),
        )
        ek1 = findEK(
            data,
            1,
            EKGroupParameter(
                40,
                1,
                EKParameter(1, 180, 10, 1),
                EKParameter(1, 150, 6, 2),
                EKParameter(1, 210, 7, 2),
                EKParameter(1, 150, 6, 2),
            ),
        )
        ek2 = findEK(
            data,
            2,
            EKGroupParameter(
                40,
                1,
                EKParameter(1, 180, 9, 1),
                EKParameter(1, 150, 6, 2),
                EKParameter(1, 140, 7, 2),
                EKParameter(1, 180, 5, 3),
            ),
        )
        ek0, ek1, ek2 = postprocess(ek0, ek1, ek2, 70, 70)
        features, label = splitGroup(data, ek0, ek1, ek2)
        trainFeatures += features
        trainLabel += label

    testData = loadFile("band2_0116")
    testFeatures = []
    testLabel = []
    for data in testData:
        ek0 = findEK(
            data,
            0,
            EKGroupParameter(
                90,
                2,
                EKParameter(1, 250, 10, 1),
                EKParameter(1, 300, 5, 2),
                EKParameter(1, 300, 10, 3),
                EKParameter(1, 150, 4, 6),
            ),
        )
        ek1 = findEK(
            data,
            1,
            EKGroupParameter(
                40,
                1,
                EKParameter(1, 180, 10, 1),
                EKParameter(1, 150, 6, 2),
                EKParameter(1, 210, 7, 2),
                EKParameter(1, 150, 6, 2),
            ),
        )
        ek2 = findEK(
            data,
            2,
            EKGroupParameter(
                40,
                1,
                EKParameter(1, 180, 9, 1),
                EKParameter(1, 150, 6, 2),
                EKParameter(1, 140, 7, 2),
                EKParameter(1, 180, 5, 3),
            ),
        )
        ek0, ek1, ek2 = postprocess(ek0, ek1, ek2, 70, 70)
        features, label = splitGroup(data, ek0, ek1, ek2)
        testFeatures += features
        testLabel += label
    acc, accTest = runRf(trainFeatures, trainLabel, testFeatures, testLabel)
    print(acc, accTest)
