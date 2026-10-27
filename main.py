from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout
import sys
from PySide6 import QtWidgets, QtCore


class WebViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #self.text = QtWidgets.QLabel("Preview Browser", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.view = QWebEngineView()
        self.view.load(QUrl("https://example.com"))

        layout = QVBoxLayout(self)
        #layout.addWidget(self.text)
        layout.addWidget(self.view)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = WebViewer()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())