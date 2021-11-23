import sys
import os
import subprocess
from playsound import playsound
from PyQt5.QtWidgets import *
from datetime import datetime as dt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STM8 Flash GUI")
        self.setGeometry(50, 50, 600, 400)
        self.count = 0
        self.UI()

    def UI(self):
        mainLayout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Flash")
        self.tabs.addTab(self.tab2, "Misc")

        mainLayout.addWidget(self.tabs)

        tab1Form = QFormLayout()
        tab1Form.addRow(QLabel("Select Device"), QLineEdit("STM8S003K3"))
        fileView = QHBoxLayout()
        self.fileLE = QLineEdit()
        fileView.addWidget(self.fileLE)
        browseButton = QPushButton("Browse")
        browseButton.clicked.connect(self.getfile)
        fileView.addWidget(browseButton)
        tab1Form.addRow(QLabel("Select BIN File"), fileView)

        tab1Layout = QVBoxLayout()
        tab1Layout.addLayout(tab1Form)
        tab1Layout.addStretch()

        hbox = QHBoxLayout()

        self.flashButton = QPushButton("Flash")
        self.flashButton.clicked.connect(self.flashAction)
        hbox.addWidget(self.flashButton)
        self.statusLE = QLineEdit("Ready")
        hbox.addWidget(self.statusLE)
        self.countLE = QLineEdit(str(self.count))
        hbox.addWidget(QLabel("Count"))
        hbox.addWidget(self.countLE)
        tab1Layout.addLayout(hbox)

        self.tab1.setLayout(tab1Layout)

        self.setLayout(mainLayout)
        self.show()

    def flashAction(self):
        # ret = 0
        cmd = os.path.abspath("bin/stm8flash_x86_64") + \
            " -c stlinkv2 -p stm8s003k3 -w " + self.fileLE.text()
        print("Command = ", cmd)
        child = subprocess.call(cmd, shell=True)
        # streamdata = child.communicate()[0]
        print("Result = ", child)

        if (child == 0):
            self.statusLE.setText("Code Flashed at {}".format(
                dt.now().strftime("%I:%M:%S %p")))
            self.count += 1
            self.countLE.setText(str(self.count))
            playsound("media/ok.mp3")
        else:
            self.statusLE.setText("Programming Failed")
            playsound("media/error.mp3")

    def getfile(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'c:\\', "STM8 Binaries (*.bin)")
    #   print(fname)
        self.fileLE.setText(fname[0])


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
