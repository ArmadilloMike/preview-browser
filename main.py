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
        layout.addWidget(self.view)
        self.setLayout(layout)

    def go_back(self):
        self.view.back()

    def go_forward(self):
        self.view.forward()

    def reload_page(self):
        self.view.reload()

    def set_url(self, url):
        self.view.setUrl(QUrl.url(url))

    def get_webpage_title(self):
        return self.view.title()

    def get_webpage_icon(self):
        return self.view.icon()

    def get_webpage_url(self):
        return self.view.url().toString()

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
    window.web_viewer.view.titleChanged.connect(
        lambda _: window.setWindowTitle(f"Preview Browser - {window.web_viewer.get_webpage_title()} - {window.web_viewer.get_webpage_url()}")
    )
    window.web_viewer.view.iconChanged.connect(
        lambda _: window.setWindowIcon(window.web_viewer.get_webpage_icon())
    )

    sys.exit(app.exec())