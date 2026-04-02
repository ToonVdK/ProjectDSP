import time
import PyQt6 as qt
import PyQt6.QtWidgets as widget
import PyQt6.QtGui as gui
from PyQt6 import QtCore
import sys
from window import Ui_MainWindow

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
window = widget.QMainWindow()
mainWindow = Ui_MainWindow()
mainWindow.setupUi(window)
window.setFixedSize(window.size())
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
