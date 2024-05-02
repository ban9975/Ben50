from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constants import *


class FileSelector(QWidget):
    def __init__(self, labelText: str, buttonText: str, defaultPath: str):
        super().__init__()
        self.defaultPath = defaultPath
        self.label = QLabel(labelText)
        self.fileNameLabel = QLabel("")
        self.btn = QPushButton(buttonText)
        self.fileName = ""
        self.btn.clicked.connect(lambda: self.selectFile())
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.fileNameLabel)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    def selectFile(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(os.path.expanduser(self.defaultPath))
        print(dialog.directory().absolutePath())
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            self.fileName = dialog.selectedFiles()[0]
            self.fileNameLabel.setText(self.fileName)

    def getFileName(self) -> str:
        return self.fileName


class LineEdit(QWidget):
    def __init__(self, labelText: str, placeholder: str = ""):
        super().__init__()
        self.label = QLabel(labelText)
        self.lineEdit = QLineEdit(placeholder)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.setLayout(self.layout)

    def getEditText(self):
        return self.lineEdit.text()
