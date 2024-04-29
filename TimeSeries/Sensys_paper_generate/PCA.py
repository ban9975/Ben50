import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DataParser import *
from Transfer import *
from ElbowKnee_all_nSensors import *
from Sensys_paper_generate.Calibration import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    trainFileName = "band2_0115"
    trainFile, _ = loadRawDataFile(trainFileName)
    testFileName = "band4_0127"
    testFile, _ = loadRawDataFile(testFileName)
    testFile = transfer(trainFile, testFile)
    trainFeatures, trainLabel = fullFileProcessing(trainFile, 3)
    trainFeatures = normalize(trainFeatures)
    testFeatures, testLabel = fullFileProcessing(testFile, 3)
    testFeatures = normalize(testFeatures)
    trainFeatures = StandardScaler().fit_transform(trainFeatures)
    testFeatures = StandardScaler().fit_transform(testFeatures)
    n_components_list = [3, 8, 12]
    for n_components in n_components_list:
        pca = PCA(n_components=n_components)
        pca.fit(trainFeatures)
        classifier = Classifier()
        acc, accTest = classifier.randomForest(
            pca.transform(trainFeatures),
            trainLabel,
            pca.transform(testFeatures),
            testLabel,
            f"{testFileName}_{n_components}components",
        )
        print(n_components, acc, accTest)
    # principalComponents = pca.transform(testFeatures)
    # principalDf = pd.DataFrame(
    #     data=principalComponents,
    #     columns=["principal component 1", "principal component 2"],
    # )
    # finalDf = pd.concat([principalDf, pd.DataFrame({"label": trainLabel})], axis=1)
    # fig = plt.figure(figsize=(8, 8))
    # ax = fig.add_subplot(1, 1, 1)
    # ax.set_xlabel("Principal Component 1", fontsize=15)
    # ax.set_ylabel("Principal Component 2", fontsize=15)
    # ax.set_title("2 component PCA", fontsize=20)

    # targets = [0, 1, 2]
    # colors = ["r", "g", "b"]
    # for target, color in zip(targets, colors):
    #     indicesToKeep = finalDf["label"] == target
    #     ax.scatter(
    #         finalDf.loc[indicesToKeep, "principal component 1"],
    #         finalDf.loc[indicesToKeep, "principal component 2"],
    #         c=color,
    #         s=50,
    #     )
    # ax.legend(["down", "up", "open"], loc="upper right")
    # ax.grid()
    # plt.show()
