# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from main import process_segment, process_segment_with_figure


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # --- THE SPLIT LAYOUT FIX ---
        # A master horizontal layout to hold the left (fixed) and right (dynamic) halves
        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Left Container: Locks your absolute-positioned text strictly in place
        self.left_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.left_container.setMinimumSize(QtCore.QSize(635, 720))
        self.left_container.setMaximumSize(QtCore.QSize(635, 16777215))  # Width fixed, height can grow
        self.left_container.setObjectName("left_container")

        # 2. Right Container: Flexes to fill the rest of the screen for the plots
        self.right_container = QtWidgets.QWidget(parent=self.centralwidget)
        self.right_container.setObjectName("right_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.right_container)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")

        self.main_layout.addWidget(self.left_container)
        self.main_layout.addWidget(self.right_container)
        # ----------------------------

        self.figure1 = Figure(layout="constrained")
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setMinimumSize(QtCore.QSize(400, 250))

        self.figure2 = Figure(layout="constrained")
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setMinimumSize(QtCore.QSize(400, 250))

        # --- LEFT SIDE METRICS (Parented to left_container instead of centralwidget) ---
        self.metrics_title = QtWidgets.QLabel(parent=self.left_container)
        self.metrics_title.setGeometry(QtCore.QRect(230, 30, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.metrics_title.setFont(font)
        self.metrics_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.metrics_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.metrics_title.setObjectName("metrics_title")

        self.metric_top = QtWidgets.QFrame(parent=self.left_container)
        self.metric_top.setGeometry(QtCore.QRect(10, 80, 621, 16))
        self.metric_top.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.metric_top.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.metric_top.setObjectName("metric_top")

        self.metric_bottom = QtWidgets.QFrame(parent=self.left_container)
        self.metric_bottom.setGeometry(QtCore.QRect(10, 533, 621, 16))
        self.metric_bottom.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.metric_bottom.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.metric_bottom.setObjectName("metric_bottom")

        self.vertical_metric = QtWidgets.QFrame(parent=self.left_container)
        self.vertical_metric.setGeometry(QtCore.QRect(80, 90, 21, 450))
        self.vertical_metric.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.vertical_metric.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vertical_metric.setObjectName("vertical_metric")

        self.metric_middle = QtWidgets.QFrame(parent=self.left_container)
        self.metric_middle.setGeometry(QtCore.QRect(10, 310, 621, 16))
        self.metric_middle.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.metric_middle.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.metric_middle.setObjectName("metric_middle")

        self.ecg_title = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_title.setGeometry(QtCore.QRect(11, 180, 57, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_title.setFont(font)
        self.ecg_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ecg_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ecg_title.setObjectName("ecg_title")

        self.ppg_title = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_title.setGeometry(QtCore.QRect(11, 410, 58, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_title.setFont(font)
        self.ppg_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ppg_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ppg_title.setObjectName("ppg_title")

        self.vertical_metric_2 = QtWidgets.QFrame(parent=self.left_container)
        self.vertical_metric_2.setGeometry(QtCore.QRect(620, -10, 21, 740))
        self.vertical_metric_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.vertical_metric_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vertical_metric_2.setObjectName("vertical_metric_2")

        self.ecg_heartrate_value = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_heartrate_value.setGeometry(QtCore.QRect(260, 111, 361, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_heartrate_value.setFont(font)
        self.ecg_heartrate_value.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ecg_heartrate_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ecg_heartrate_value.setObjectName("ecg_heartrate_value")

        self.ecg_sqi_title = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_sqi_title.setGeometry(QtCore.QRect(110, 180, 71, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_sqi_title.setFont(font)
        self.ecg_sqi_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ecg_sqi_title.setObjectName("ecg_sqi_title")

        self.ecg_heartrate_title = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_heartrate_title.setGeometry(QtCore.QRect(110, 110, 141, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_heartrate_title.setFont(font)
        self.ecg_heartrate_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ecg_heartrate_title.setObjectName("ecg_heartrate_title")

        self.ecg_weight_value = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_weight_value.setGeometry(QtCore.QRect(230, 250, 391, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_weight_value.setFont(font)
        self.ecg_weight_value.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ecg_weight_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ecg_weight_value.setObjectName("ecg_weight_value")

        self.ecg_sqi_value = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_sqi_value.setGeometry(QtCore.QRect(180, 180, 441, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_sqi_value.setFont(font)
        self.ecg_sqi_value.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ecg_sqi_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ecg_sqi_value.setObjectName("ecg_sqi_value")

        self.ecg_weight_title = QtWidgets.QLabel(parent=self.left_container)
        self.ecg_weight_title.setGeometry(QtCore.QRect(110, 250, 121, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ecg_weight_title.setFont(font)
        self.ecg_weight_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ecg_weight_title.setObjectName("ecg_weight_title")

        self.ppg_sqi_title = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_sqi_title.setGeometry(QtCore.QRect(110, 410, 71, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_sqi_title.setFont(font)
        self.ppg_sqi_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ppg_sqi_title.setObjectName("ppg_sqi_title")

        self.ppg_sqi_value = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_sqi_value.setGeometry(QtCore.QRect(180, 410, 441, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_sqi_value.setFont(font)
        self.ppg_sqi_value.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ppg_sqi_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ppg_sqi_value.setObjectName("ppg_sqi_value")

        self.ppg_weight_title = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_weight_title.setGeometry(QtCore.QRect(110, 480, 121, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_weight_title.setFont(font)
        self.ppg_weight_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ppg_weight_title.setObjectName("ppg_weight_title")

        self.ppg_heartrate_title = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_heartrate_title.setGeometry(QtCore.QRect(110, 340, 141, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_heartrate_title.setFont(font)
        self.ppg_heartrate_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ppg_heartrate_title.setObjectName("ppg_heartrate_title")

        self.ppg_heartrate_value = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_heartrate_value.setGeometry(QtCore.QRect(260, 341, 361, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_heartrate_value.setFont(font)
        self.ppg_heartrate_value.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ppg_heartrate_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ppg_heartrate_value.setObjectName("ppg_heartrate_value")

        self.ppg_weight_value = QtWidgets.QLabel(parent=self.left_container)
        self.ppg_weight_value.setGeometry(QtCore.QRect(230, 480, 391, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ppg_weight_value.setFont(font)
        self.ppg_weight_value.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ppg_weight_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ppg_weight_value.setObjectName("ppg_weight_value")

        self.fhr_value = QtWidgets.QLabel(parent=self.left_container)
        self.fhr_value.setGeometry(QtCore.QRect(270, 560, 351, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fhr_value.setFont(font)
        self.fhr_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fhr_value.setObjectName("fhr_value")

        self.fhr_title = QtWidgets.QLabel(parent=self.left_container)
        self.fhr_title.setGeometry(QtCore.QRect(30, 560, 241, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fhr_title.setFont(font)
        self.fhr_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fhr_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.fhr_title.setObjectName("fhr_title")

        self.fhrvsdnn_value = QtWidgets.QLabel(parent=self.left_container)
        self.fhrvsdnn_value.setGeometry(QtCore.QRect(220, 610, 401, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fhrvsdnn_value.setFont(font)
        self.fhrvsdnn_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fhrvsdnn_value.setObjectName("fhrvsdnn_value")

        self.fhrvsdnn_title = QtWidgets.QLabel(parent=self.left_container)
        self.fhrvsdnn_title.setGeometry(QtCore.QRect(30, 610, 191, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fhrvsdnn_title.setFont(font)
        self.fhrvsdnn_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fhrvsdnn_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.fhrvsdnn_title.setObjectName("fhrvsdnn_title")

        self.fhrvrmssd_title = QtWidgets.QLabel(parent=self.left_container)
        self.fhrvrmssd_title.setGeometry(QtCore.QRect(30, 660, 211, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fhrvrmssd_title.setFont(font)
        self.fhrvrmssd_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fhrvrmssd_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.fhrvrmssd_title.setObjectName("fhrvrmssd_title")

        self.fhrvrmssd_value = QtWidgets.QLabel(parent=self.left_container)
        self.fhrvrmssd_value.setGeometry(QtCore.QRect(240, 660, 381, 43))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fhrvrmssd_value.setFont(font)
        self.fhrvrmssd_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fhrvrmssd_value.setObjectName("fhrvrmssd_value")

        # --- RIGHT SIDE PLOTS (Parented to the flexible vertical layout) ---
        self.verticalLayout.addWidget(self.canvas1)

        self.load_data = QtWidgets.QPushButton(parent=self.right_container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.load_data.setSizePolicy(sizePolicy)
        self.load_data.setObjectName("load_data")
        self.verticalLayout.addWidget(self.load_data, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(self.canvas2)

        self.export_data = QtWidgets.QPushButton(parent=self.right_container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.export_data.setSizePolicy(sizePolicy)
        self.export_data.setObjectName("export_data")
        self.verticalLayout.addWidget(self.export_data, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.bindButtons()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.metrics_title.setText(_translate("MainWindow", "Metrics"))
        self.load_data.setText(_translate("MainWindow", "Load Data"))
        self.export_data.setText(_translate("MainWindow", "Export Data"))
        self.ecg_title.setText(_translate("MainWindow", "ECG"))
        self.ppg_title.setText(_translate("MainWindow", "PPG"))
        self.ecg_heartrate_value.setText(_translate("MainWindow", "XX"))
        self.ecg_sqi_title.setText(_translate("MainWindow", "SQI:"))
        self.ecg_heartrate_title.setText(_translate("MainWindow", "Heartrate:"))
        self.ecg_weight_value.setText(_translate("MainWindow", "XX"))
        self.ecg_sqi_value.setText(_translate("MainWindow", "XX"))
        self.ecg_weight_title.setText(_translate("MainWindow", "Weight:"))
        self.ppg_sqi_title.setText(_translate("MainWindow", "SQI:"))
        self.ppg_sqi_value.setText(_translate("MainWindow", "XX"))
        self.ppg_weight_title.setText(_translate("MainWindow", "Weight:"))
        self.ppg_heartrate_title.setText(_translate("MainWindow", "Heartrate:"))
        self.ppg_heartrate_value.setText(_translate("MainWindow", "XX"))
        self.ppg_weight_value.setText(_translate("MainWindow", "XX"))
        self.fhr_value.setText(_translate("MainWindow", "XX"))
        self.fhr_title.setText(_translate("MainWindow", "Fused Heartrate:"))
        self.fhrvsdnn_value.setText(_translate("MainWindow", "XX"))
        self.fhrvsdnn_title.setText(_translate("MainWindow", "FHRV SDNN:"))
        self.fhrvrmssd_title.setText(_translate("MainWindow", "FHRV RMSSD:"))
        self.fhrvrmssd_value.setText(_translate("MainWindow", "XX"))

    def bindButtons(self):
        self.load_data.clicked.connect(self.loadData)
        self.export_data.clicked.connect(self.exportData)

    def loadData(self):
        print("Loading Data")
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Select .npy data file", "",
                                                            "NumPy files (*.npy)")
        if not filepath:
            return  # Cancelled dialog safeguard

        patient_num = filepath.split("/")[-1].split("_")[0]
        path = filepath.strip(filepath.split("/")[-1])
        results = []
        print("Processing segment: ", 0)
        metrics, self.figure1, self.figure2 = process_segment_with_figure(path, patient_num, 0)
        results.append(metrics)
        for i in range(1, 30):
            print("Processing segment: ", i)
            metrics = process_segment(path, patient_num, i)
            results.append(metrics)

        if results:
            print("Calculating Values")
            mean_ecg_hr = np.mean([res['ecg_hr'] for res in results])
            mean_ppg_hr = np.mean([res['ppg_hr'] for res in results])
            mean_ecg_sqi = np.mean([res['ecg_sqi'] for res in results])
            mean_ppg_sqi = np.mean([res['ppg_sqi'] for res in results])
            mean_w_ecg = np.mean([res['ecg_weight'] for res in results])
            mean_w_ppg = np.mean([res['ppg_weight'] for res in results])
            mean_fused_hr = np.mean([res['fused_hr'] for res in results])
            mean_fused_sdnn = np.mean([res['fused_sdnn'] for res in results])
            mean_fused_rmssd = np.mean([res['fused_rmssd'] for res in results])
        else:
            print("No results found")
            mean_ecg_hr = mean_ppg_hr = mean_ecg_sqi = mean_ppg_sqi = "XX"
            mean_w_ecg = mean_w_ppg = mean_fused_hr = mean_fused_sdnn = mean_fused_rmssd = "XX"

        self.ecg_heartrate_value.setText(str(mean_ecg_hr))
        self.ecg_sqi_value.setText(str(mean_ecg_sqi))
        self.ecg_weight_value.setText(str(mean_w_ecg))
        self.ppg_heartrate_value.setText(str(mean_ppg_hr))
        self.ppg_sqi_value.setText(str(mean_ppg_sqi))
        self.ppg_weight_value.setText(str(mean_w_ppg))
        self.fhr_value.setText(str(mean_fused_hr))
        self.fhrvsdnn_value.setText(str(mean_fused_sdnn))
        self.fhrvrmssd_value.setText(str(mean_fused_rmssd))

        self.plot(self.canvas1, self.figure1)
        self.plot(self.canvas2, self.figure2)

    def exportData(self):
        print("Exporting Data")

    def plot(self, canvas, fig):
        canvas.figure = fig
        fig.set_canvas(canvas)
        fig.tight_layout(pad=1.5)  # Added minor padding to ensure axis labels don't get chopped off
        canvas.draw()