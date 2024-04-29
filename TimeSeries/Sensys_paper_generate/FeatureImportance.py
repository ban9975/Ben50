import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from sklearn.inspection import permutation_importance
from DataParser import *
from Transfer import *
from ElbowKnee_all_nSensors import *
from Sensys_paper_generate.Calibration import *

if __name__ == "__main__":
    trainFileName = "band2_0115"
    trainFile, _ = loadRawDataFile(trainFileName)
    # testFileName = "band2_0126"
    # testFile, _ = loadRawDataFile(testFileName)
    trainFile, testFile = fullFileDataPartition(trainFile, 0.6)
    # testFile = transfer(trainFile, testFile, calibrationFile)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = normalize(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = normalize(testFeatures)
    print(len(trainFeatures), len(testFeatures))
    classifier = Classifier()
    acc, accTest = classifier.randomForest(
        trainFeatures,
        trainLabel,
        testFeatures,
        testLabel,
    )
    print(acc, accTest)
    # importances = classifier.model.feature_importances_
    # forest_importances = pd.Series(importances, index=generateFeatureIndex())
    # forest_importances.plot.bar()
    # plt.show()
    result = permutation_importance(
        classifier.model,
        testFeatures,
        testLabel,
        n_repeats=10,
        random_state=42,
    )
    forest_importances = pd.Series(
        result.importances_mean, index=generateFeatureIndex()
    )
    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importances using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.show()
