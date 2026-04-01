import time

import PyQt6 as qt
import PyQt6.QtWidgets as widget
import PyQt6.QtGui as gui
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QFileDialog

"""
Required functionality
- Load data (button, upload file)
- Preprocess data (button, process)
- Calculate PAT and PTT (2 buttons, both have an output field)
- Derive BP (button, derive bp)
- Export processed data and analysis summary (button, export file)
"""

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.

class MainWindow(widget.QMainWindow):
    def __init__(self):
        widget.QMainWindow.__init__(self)

        # Required vars
        self.filepath = ""
        self.pat = ""
        self.ptt = ""
        self.bp = ""

        # Initial window setup
        self.setWindowTitle("HeartBP")
        # self.showFullScreen()
        self.setFixedSize(800, 600)

        # Visual structure objects
        outer_hbox = widget.QHBoxLayout()
        outer_vbox1 = widget.QVBoxLayout()
        outer_vbox2 = widget.QVBoxLayout()
        inner_hbox1 = widget.QHBoxLayout()
        inner_hbox2 = widget.QHBoxLayout()
        inner_hbox3 = widget.QHBoxLayout()

        # Structure layout
        outer_hbox.addLayout(outer_vbox1)
        outer_hbox.addLayout(outer_vbox2)

        # Object definition
        load_data = widget.QPushButton("Load data")
        preprocess_data = widget.QPushButton("Preprocess data")
        calculate_pat = widget.QPushButton("Calculate PAT")
        calculate_ptt = widget.QPushButton("Calculate PTT")
        derive_BP = widget.QPushButton("Derive BP")
        export_data = widget.QPushButton("Export data")
        preprocess_state = widget.QLabel("Preprocessed data")
        pat_value = widget.QLabel("PAT value: ")
        ptt_value = widget.QLabel("PTT value: ")
        bp_value = widget.QLabel("BP value: ")
        processing_img = widget.QLabel(self)

        # Button function assignment
        load_data.clicked.connect(self.loadData)
        preprocess_data.clicked.connect(self.preprocessData)
        calculate_pat.clicked.connect(self.calculatePAT)
        calculate_ptt.clicked.connect(self.calculatePTT)
        derive_BP.clicked.connect(self.deriveBP)
        export_data.clicked.connect(self.exportData)

        # Object place in layout
        outer_vbox1.addStretch()
        outer_vbox1.addWidget(processing_img)
        outer_vbox1.addWidget(load_data)
        outer_vbox1.addStretch()
        outer_vbox2.addWidget(preprocess_data)
        outer_vbox2.addWidget(preprocess_state)
        outer_vbox2.addLayout(inner_hbox1)
        inner_hbox1.addWidget(calculate_pat)
        inner_hbox1.addWidget(calculate_ptt)
        outer_vbox2.addLayout(inner_hbox2)
        inner_hbox2.addWidget(pat_value)
        inner_hbox2.addWidget(ptt_value)
        outer_vbox2.addLayout(inner_hbox3)
        inner_hbox3.addWidget(derive_BP)
        inner_hbox3.addWidget(bp_value)
        outer_vbox2.addWidget(export_data)

        central_widget = widget.QWidget()
        central_widget.setLayout(outer_hbox)
        self.setCentralWidget(central_widget)

    def loadData(self):
        filepath, _ = widget.QFileDialog.getOpenFileName(self,"Select .npy file","","NumPy files (*.npy)")

    def preprocessData(self):
        print("Preprocessing Data...")

    def calculatePAT(self):
        print("Calculating PAT...")

    def calculatePTT(self):
        print("Calculating PTT...")

    def deriveBP(self):
        print("Deriving BP...")

    def exportData(self):
        print("Exporting data...")

app = widget.QApplication(sys.argv)
app.setApplicationName("HeartBP")
app.setApplicationVersion("1.0")
app.setWindowIcon(gui.QIcon("img/icon.png"))

splash_pix = gui.QPixmap("img/heartBP.png").scaled(800, 800)
splash = widget.QSplashScreen(splash_pix, QtCore.Qt.WindowType.WindowStaysOnTopHint)
# add fade to splashscreen
opaqueness = 0.0
step = 0.02
splash.setWindowOpacity(opaqueness)
splash.show()
while opaqueness < 1:
    splash.setWindowOpacity(opaqueness)
    time.sleep(step) # Gradually appears
    opaqueness+=step
time.sleep(1) # hold image on screen for a while
splash.close() # close the splash screen

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
