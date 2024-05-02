import sys
import os
from openpyxl import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
from Constants import *
from BTController import *
from DataCollector import DataCollector
from Components import *
from CalibrationClassifier import *


class Tool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataCollector = DataCollector()
        self.calibrationClassifier = CalibrationClassifier()
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
        self.layout.addWidget(self.tab)
        self.setCentralWidget(self.widget)
        self.setFixedSize(1500, 750)
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
        self.runBtn = QPushButton("Run")
        self.runBtn.clicked.connect(self.run)
        self.resultLabel = QLabel()
        self.resultLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultFig = QLabel()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.trainFile, 0, 0, 1, 4)
        self.layout.addWidget(self.trainFlatFile, 1, 0, 1, 4)
        self.layout.addWidget(self.testFile, 2, 0, 1, 4)
        self.layout.addWidget(self.testFlatFile, 3, 0, 1, 4)
        self.layout.addWidget(self.mode, 4, 1, 1, 1)
        self.layout.addWidget(self.runBtn, 4, 2, 1, 1)
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

    def disableBtns(self, state):
        self.runBtn.setDisabled(state)

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
                os.path.join(config["Store_Path"]["gesture_fig_path"], f"{gesture}.png")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(13)
    app.setFont(font)
    MainWindow = Tool()
    sys.exit(app.exec_())
