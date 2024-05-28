import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from sklearn.inspection import permutation_importance
from DataParser import *
from ElbowKnee_all_nSensors import *
from CalibrationCompare import *

if __name__ == "__main__":
    trainFileName = "band2_0115"

    testFileNames = ["band2_0115", "band2_0116", "band1_0126", "band4_0128"]
    testTypes = ["Same-wear", "Cross-wear", "Cross-band", "Cross-user"]
    for i, testFileName in enumerate(testFileNames):
        trainFile, sheetNames = loadRawDataFile(getDefaultFilePath(trainFileName))
        trainFile, _ = calibrationPartition(
            sheetNames,
            trainFile,
            0.6,
        )
        print(testFileName)
        tmpFile, sheetNames = loadRawDataFile(getDefaultFilePath(testFileName))
        _, tmpFile = calibrationPartition(
            sheetNames,
            tmpFile,
            0.6,
            0.4,
            ["00", "11", "22", "01", "12", "02"],
        )
        testFile, calibrationFile = calibrationPartition(
            sheetNames,
            tmpFile,
            0.5,
            0.5,
            ["00", "11", "22", "01", "12", "02"],
        )
        testFile = maxminNormalization(trainFile, testFile, calibrationFile)
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
        print(forest_importances)
        ax.set_ylabel("Mean accuracy decrease")
        ax.set_xlabel("Feature")
        fig.tight_layout()
        plt.savefig(
            os.path.join(
                os.getcwd(),
                "../Sensys 2024",
                "Feature importance",
                f"{testTypes[i]}",
                "feature_importance.png",
            ),
        )
