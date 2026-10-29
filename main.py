from PySide6.QtGui import QIcon
import pyperclip
import webbrowser
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout, QMainWindow, QToolBar, QStyle
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


def open_in_browser(url):
    webbrowser.open(url)
    return "done"

def copy_to_clipboard(text):
    pyperclip.copy(text)
    return "done"

class AddressBar(QToolBar):
    def __init__(self, web_viewer):
        super().__init__()
        self.web_viewer = web_viewer

        self.back_button = QtWidgets.QPushButton("", self)
        self.back_button.clicked.connect(self.web_viewer.go_back)
        back_icon = QIcon("assets/back_icon.svg")
        self.back_button.setIcon(back_icon)

        self.forward_button = QtWidgets.QPushButton("", self)
        self.forward_button.clicked.connect(self.web_viewer.go_forward)
        forward_icon = QIcon("assets/forward_icon.svg")
        self.forward_button.setIcon(forward_icon)

        self.open_browser = QtWidgets.QPushButton("Open in Browser")
        self.open_browser.clicked.connect(lambda: open_in_browser(self.web_viewer.get_webpage_url()))
        open_icon = QIcon("assets/open_browser_icon.svg")
        self.open_browser.setIcon(open_icon)

        self.address_copy = QtWidgets.QPushButton("Copy to Clipboard")
        self.address_copy.clicked.connect(lambda: copy_to_clipboard(self.web_viewer.get_webpage_url()))
        copy_icon = QIcon("assets/copy_icon.svg")
        self.address_copy.setIcon(copy_icon)

        self.addWidget(self.back_button)
        self.addWidget(self.forward_button)
        self.addWidget(self.open_browser)
        self.addWidget(self.address_copy)
        self.setMovable(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Preview Browser")
        self.resize(800,600)

        self.web_viewer = WebViewer()
        self.setCentralWidget(self.web_viewer)
        self.address_bar = AddressBar(self.web_viewer)
        self.addToolBar(self.address_bar)

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