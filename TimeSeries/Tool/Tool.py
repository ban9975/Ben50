import sys
import os
from openpyxl import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
from Constants import *
from BTController import *
from DataCollector import *
from Components import *
from CalibrationClassifier import *
from Plotter import *


class Tool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataCollector = DataCollector()
        self.calibrationClassifier = CalibrationClassifier()
        self.plotter = Plotter()
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.btWidget = QWidget()
        self.btLayout = QHBoxLayout(self.btWidget)
        self.btLabel = QLabel("COM Port:")
        self.btCombo = QComboBox()
        self.btCombo.addItems(list_all_ports())
        self.btBtn = QPushButton("Connect")
        self.btBtn.clicked.connect(self.connectBT)
        self.btLayout.addWidget(self.btLabel)
        self.btLayout.addWidget(self.btCombo)
        self.btLayout.addWidget(self.btBtn)
        self.layout.addWidget(self.btWidget)
        self.tab = QTabWidget()
        self.tab.addTab(TrainPage(self.calibrationClassifier), "Train")
        self.tab.addTab(CollectPage(self.dataCollector), "Collect")
        self.tab.addTab(PlotPage(self.plotter), "Plot")
        self.layout.addWidget(self.tab)
        self.setCentralWidget(self.widget)
        self.setFixedSize(1500, 800)
        self.show()

    def connectBT(self):
        self.dataCollector.connectBT(self.btCombo.currentText())
        self.btBtn.setDisabled(True)


class TrainPage(QWidget):
    def __init__(self, calibrationClassifier: CalibrationClassifier):
        super().__init__()
        self.calibrationClassifier = calibrationClassifier
        self.trainFile = FileSelector(
            "Train data path: ", "Select train data", config["Store_Path"]["excel_path"]
        )
        self.trainFlatFile = FileSelector(
            "Train flat file path: ",
            "Select train flat file",
            config["Store_Path"]["excel_path"],
        )
        self.testFile = FileSelector(
            "Test data path: ", "Select test data", config["Store_Path"]["excel_path"]
        )
        self.testFlatFile = FileSelector(
            "Test flat file path: ",
            "Select test flat file",
            config["Store_Path"]["excel_path"],
        )
        self.mode = QComboBox()
        self.mode.addItems(calibrationModes)
        self.trainBtn = QPushButton("Train")
        self.trainBtn.clicked.connect(self.run)
        self.trainAllBtn = QPushButton("Train all calibration modes")
        self.trainAllBtn.clicked.connect(self.trainAll)
        self.resultLabel = QLabel()
        self.resultLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultFig = QLabel()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.trainFile, 0, 0, 1, 4)
        self.layout.addWidget(self.trainFlatFile, 1, 0, 1, 4)
        self.layout.addWidget(self.testFile, 2, 0, 1, 4)
        self.layout.addWidget(self.testFlatFile, 3, 0, 1, 4)
        self.layout.addWidget(self.mode, 4, 1, 1, 1)
        self.layout.addWidget(self.trainBtn, 4, 2, 1, 1)
        self.layout.addWidget(self.trainAllBtn, 4, 3, 1, 1)
        self.layout.addWidget(self.resultLabel, 5, 0, 1, 3)
        self.layout.addWidget(self.resultFig, 5, 3, 2, 1)

    def run(self):
        self.disableBtns(True)
        self.thread = QThread()
        self.worker = TrainWorker(
            self.calibrationClassifier,
            self.trainFile.getFileName(),
            self.testFile.getFileName(),
            self.trainFlatFile.getFileName(),
            self.testFlatFile.getFileName(),
            self.mode.currentText(),
        )
        self.worker.resultSignal.connect(
            lambda result: self.resultLabel.setText(result)
        )
        self.worker.finishSignal.connect(
            lambda: self.setFig(
                QPixmap(
                    self.calibrationClassifier.confusionMatrix(
                        config["Store_Path"]["plot_path"]
                    )
                )
            )
        )
        self.worker.finishSignal.connect(lambda: self.disableBtns(False))
        self.worker.finishSignal.connect(self.worker.deleteLater)
        self.worker.finishSignal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.start()

    def trainAll(self):
        self.disableBtns(True)
        self.thread = QThread()
        self.worker = TrainWorker(
            self.calibrationClassifier,
            self.trainFile.getFileName(),
            self.testFile.getFileName(),
            self.trainFlatFile.getFileName(),
            self.testFlatFile.getFileName(),
            -1,
        )
        # self.worker.resultSignal.connect(
        #     lambda result: self.resultLabel.setText(result)
        # )
        # self.worker.finishSignal.connect(
        #     lambda: self.setFig(
        #         QPixmap(
        #             self.calibrationClassifier.confusionMatrix(
        #                 config["Store_Path"]["plot_path"]
        #             )
        #         )
        #     )
        # )
        self.worker.finishSignal.connect(lambda: self.disableBtns(False))
        self.worker.finishSignal.connect(self.worker.deleteLater)
        self.worker.finishSignal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.start()

    def disableBtns(self, state):
        self.trainBtn.setDisabled(state)
        self.trainAllBtn.setDisabled(state)

    def setFig(self, fileName: str):
        self.resultFig.setPixmap(QPixmap(fileName).scaled(400, 400, Qt.KeepAspectRatio))


class TrainWorker(QObject):
    finishSignal = pyqtSignal()
    resultSignal = pyqtSignal(str)

    def __init__(
        self,
        calibrationClassifier: CalibrationClassifier,
        trainFileName: str,
        testFileName: str,
        trainFlatFileName: str,
        testFlatFileName: str,
        mode: str,
    ):
        super().__init__()
        self.calibrationClassifier = calibrationClassifier
        self.trainFileName = trainFileName
        self.testFileName = testFileName
        self.trainFlatFileName = trainFlatFileName
        self.testFlatFileName = testFlatFileName
        self.mode = mode

    def work(self):
        if self.mode == -1:
            self.calibrationClassifier.setFile(
                self.trainFileName,
                self.testFileName,
                self.trainFlatFileName,
                self.testFlatFileName,
            )
            self.calibrationClassifier.trainAll(
                config["Store_Path"]["trainResult_path"]
            )
        else:
            self.calibrationClassifier.setFile(
                self.trainFileName,
                self.testFileName,
                self.trainFlatFileName,
                self.testFlatFileName,
            )
            result = self.calibrationClassifier.train(self.mode)
            self.resultSignal.emit(
                "Train features: {}, Test festures: {}, Train acc: {}, Test acc: {}".format(
                    *result
                )
            )
        self.finishSignal.emit()


class CollectPage(QWidget):
    def __init__(self, dataCollector: DataCollector):
        super().__init__()
        self.file = LineEdit("FileName: ")
        self.sequence = LineEdit("Sequence: ")
        self.iteration = LineEdit("Iteration: ")
        self.collectBtn = QPushButton("Collect")
        self.collectBtn.clicked.connect(self.collect)
        self.fig = QLabel()
        self.dataCollector = dataCollector
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.file, 0, 0, 1, 2)
        self.layout.addWidget(self.sequence, 1, 0, 1, 1)
        self.layout.addWidget(self.iteration, 1, 1, 1, 1)
        self.layout.addWidget(self.collectBtn, 1, 2, 1, 1)
        self.layout.addWidget(self.fig, 2, 0, 1, 1)

    def collect(self):
        self.disableBtns(True)
        fileName = os.path.join(
            config["Store_Path"]["excel_path"], self.file.getEditText()
        )
        sequence = self.sequence.getEditText()
        iteration = int(self.iteration.getEditText())
        self.thread = QThread()
        self.worker = CollectWorker(self.dataCollector, fileName, sequence, iteration)
        self.worker.gestureSignal.connect(
            lambda gesture: self.setFig(
                os.path.join(
                    basedir, config["Store_Path"]["gesture_fig_path"], f"{gesture}.png"
                )
            )
        )
        self.worker.finishSignal.connect(
            lambda: self.setFig(
                QPixmap(self.dataCollector.plotData(config["Store_Path"]["plot_path"]))
            )
        )
        self.worker.finishSignal.connect(lambda: self.disableBtns(False))
        self.worker.finishSignal.connect(self.worker.deleteLater)
        self.worker.finishSignal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.start()

    def disableBtns(self, state):
        self.collectBtn.setDisabled(state)

    def setFig(self, fileName: str):
        self.fig.setPixmap(QPixmap(fileName).scaled(400, 400, Qt.KeepAspectRatio))


class CollectWorker(QObject):
    gestureSignal = pyqtSignal(str)
    finishSignal = pyqtSignal()
    resultSignal = pyqtSignal(str)

    def __init__(
        self, dataCollector: DataCollector, fileName: str, sequence: str, iteration: str
    ):
        super().__init__()
        self.dataCollector = dataCollector
        self.stop = False
        self.fileName = fileName
        self.sequence = sequence
        self.iteration = iteration

    def work(self):
        gestureList = []
        for i in range(self.iteration):
            gestureList += [int(s) for s in self.sequence]
        section = 1
        ges = -1
        gesIdx = 0
        self.gestureSignal.emit("neutral")
        stop = self.dataCollector.startCollect(
            self.fileName, self.sequence, self.iteration
        )
        start = time.time()
        while not stop:
            if time.time() - start > 2:
                if section % 2 == 1 and section < len(gestureList) * 2:
                    ges = gestureList[gesIdx]
                    gesIdx += 1
                    self.gestureSignal.emit(gestures[ges])
                elif section % 2 == 0 or section >= len(gestureList) * 2:
                    ges = -1
                    self.gestureSignal.emit("neutral")
                section += 1
                start = time.time()
            stop = self.dataCollector.collectData(ges)
        self.dataCollector.stopCollect()
        self.finishSignal.emit()


class PlotPage(QWidget):
    def __init__(self, plotter: Plotter):
        super().__init__()
        self.plotter = plotter
        self.layout = QVBoxLayout()
        self.tab = QTabWidget()
        self.tab.addTab(FeatureImportancePage(self.plotter), "Feature importance")
        self.tab.addTab(SelectedFeaturePage(self.plotter), "Selected Feature")
        self.tab.addTab(FoldingPointPage(self.plotter), "Folding Point Improvement")
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)


class FeatureImportancePage(QWidget):
    def __init__(self, plotter: Plotter):
        super().__init__()
        self.plotter = plotter
        self.file = FileSelector(
            "File: ", "Select file", config["Store_Path"]["excel_path"]
        )
        self.plotBtn = QPushButton("Plot")
        self.plotBtn.clicked.connect(self.plot)
        self.resultLabel = QLabel()
        self.resultLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultFig = QLabel()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.file, 0, 0, 1, 4)
        self.layout.addWidget(self.plotBtn, 1, 3, 1, 1)
        self.layout.addWidget(self.resultLabel, 2, 0, 1, 2)
        self.layout.addWidget(self.resultFig, 2, 2, 2, 1)
        self.setLayout(self.layout)

    def plot(self):
        self.disableBtns(True)
        self.thread = QThread()
        self.worker = PlotterWorker(
            self.plotter, self.file.getFileName(), "FeatureImportance"
        )
        self.worker.resultSignal.connect(
            lambda result: self.resultLabel.setText(result)
        )
        self.worker.finishSignal.connect(
            lambda: self.setFig(
                QPixmap(
                    self.plotter.plotFeatureImportance(
                        config["Store_Path"]["plot_path"]
                    )
                )
            )
        )
        self.worker.finishSignal.connect(lambda: self.disableBtns(False))
        self.worker.finishSignal.connect(self.worker.deleteLater)
        self.worker.finishSignal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.start()

    def disableBtns(self, state):
        self.plotBtn.setDisabled(state)

    def setFig(self, fileName: str):
        self.resultFig.setPixmap(QPixmap(fileName).scaled(400, 400, Qt.KeepAspectRatio))


class SelectedFeaturePage(QWidget):
    def __init__(self, plotter: Plotter):
        super().__init__()
        self.plotter = plotter
        self.file = FileSelector(
            "File: ", "Select file", config["Store_Path"]["excel_path"]
        )
        self.plotBtn = QPushButton("Plot")
        self.plotBtn.clicked.connect(self.plot)
        self.resultLabel = QLabel()
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultFig1 = QLabel()
        self.resultFig2 = QLabel()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.file, 0, 0, 1, 4)
        self.layout.addWidget(self.plotBtn, 1, 3, 1, 1)
        self.layout.addWidget(self.resultLabel, 2, 0, 1, 2)
        self.layout.addWidget(self.resultFig1, 3, 0, 2, 1)
        self.layout.addWidget(self.resultFig2, 3, 1, 2, 1)
        self.setLayout(self.layout)

    def plot(self):
        self.disableBtns(True)
        self.thread = QThread()
        self.worker = PlotterWorker(
            self.plotter, self.file.getFileName(), "SelectedFeature"
        )
        self.worker.resultSignal.connect(
            lambda result: self.resultLabel.setText(result)
        )
        self.worker.finishSignal.connect(self.setFig)
        self.worker.finishSignal.connect(lambda: self.disableBtns(False))
        self.worker.finishSignal.connect(self.worker.deleteLater)
        self.worker.finishSignal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.start()

    def disableBtns(self, state):
        self.plotBtn.setDisabled(state)

    def setFig(self):
        figPath = self.plotter.plotSelectedFeatures(config["Store_Path"]["plot_path"])
        self.resultFig1.setPixmap(
            QPixmap(figPath[0]).scaled(400, 400, Qt.KeepAspectRatio)
        )
        self.resultFig2.setPixmap(
            QPixmap(figPath[1]).scaled(400, 400, Qt.KeepAspectRatio)
        )


class FoldingPointPage(QWidget):
    def __init__(self, plotter: Plotter):
        super().__init__()
        self.plotter = plotter
        self.file = FileSelector(
            "File: ", "Select file", config["Store_Path"]["excel_path"]
        )
        self.plotBtn = QPushButton("Plot")
        self.plotBtn.clicked.connect(self.plot)
        self.resultLabel = QLabel()
        self.resultLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultFig = QLabel()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.file, 0, 0, 1, 4)
        self.layout.addWidget(self.plotBtn, 1, 3, 1, 1)
        self.layout.addWidget(self.resultLabel, 2, 0, 1, 2)
        self.layout.addWidget(self.resultFig, 2, 2, 2, 1)
        self.setLayout(self.layout)

    def plot(self):
        self.disableBtns(True)
        self.thread = QThread()
        self.worker = PlotterWorker(
            self.plotter, self.file.getFileName(), "FoldingPoint"
        )
        self.worker.resultSignal.connect(
            lambda result: self.resultLabel.setText(result)
        )
        self.worker.finishSignal.connect(
            lambda: self.setFig(
                QPixmap(
                    self.plotter.plotFoldingPoint(config["Store_Path"]["plot_path"])
                )
            )
        )
        self.worker.finishSignal.connect(lambda: self.disableBtns(False))
        self.worker.finishSignal.connect(self.worker.deleteLater)
        self.worker.finishSignal.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.start()

    def disableBtns(self, state):
        self.plotBtn.setDisabled(state)

    def setFig(self, fileName: str):
        self.resultFig.setPixmap(QPixmap(fileName).scaled(400, 400, Qt.KeepAspectRatio))


class PlotterWorker(QObject):
    finishSignal = pyqtSignal()
    resultSignal = pyqtSignal(str)

    def __init__(self, plotter: Plotter, fileName: list[str], mode: str):
        super().__init__()
        self.plotter = plotter
        self.fileName = fileName
        self.mode = mode

    def work(self):
        if self.mode == "FeatureImportance":
            result = self.plotter.calculateFeatureImportance(self.fileName)
            self.resultSignal.emit(
                "Train features: {}, Test festures: {}, Train acc: {}, Test acc: {}".format(
                    *result
                )
            )
        elif self.mode == "SelectedFeature":
            result = self.plotter.calculateSelectedFeatures(self.fileName)
            self.resultSignal.emit(
                "Train features: {}, Test festures: {}\nTest acc: {}".format(*result)
            )
        elif self.mode == "FoldingPoint":
            result = self.plotter.calculateFoldingPoint(self.fileName)
            self.resultSignal.emit(
                "BaseLine: {}, Point-level majority vote: {}, Group-level majority vote: {}".format(
                    *result
                )
            )
        elif self.mode == "Calibration":
            result = self.plotter.calculcateCalibration(*self.fileName)
            self.resultSignal.emit(
                "Cross-wear: {}, Cross-band: {}, Cross-user: {}".format(*result)
            )
        self.finishSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(13)
    app.setFont(font)
    MainWindow = Tool()
    sys.exit(app.exec_())
