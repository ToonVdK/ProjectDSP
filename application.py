import PyQt6 as qt
import PyQt6.QtWidgets as widget
import PyQt6.QtGui as gui

# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.

class MainWindow(widget.QMainWindow):
    def __init__(self):
        widget.QMainWindow.__init__(self)

        self.setWindowTitle("HeartBP")
        # self.showFullScreen()
        self.setFixedSize(800, 600)
        button = widget.QPushButton("Start")
        button.clicked.connect(self.buttonPressed)

        #set central object of window
        self.setCentralWidget(button)

    def buttonPressed(self):
        print("Button pressed")

app = widget.QApplication(sys.argv)
app.setApplicationName("HeartBP")
app.setApplicationVersion("1.0")
app.setWindowIcon(gui.QIcon("img/icon.png"))

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
