from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout, QMainWindow
import sys
from PySide6 import QtWidgets, QtCore


class WebViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.view = QWebEngineView()
        self.view.load(QUrl("https://example.com"))

        layout = QVBoxLayout(self)
        #layout.addWidget(self.text)
        layout.addWidget(self.view)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Preview Browser")
        self.resize(800,600)

        self.web_viewer = WebViewer()
        self.setCentralWidget(self.web_viewer)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())