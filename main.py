from this import d
import darkdetect
import os
from PySide6.QtGui import QIcon, QShortcut, QKeySequence, QAction
import pyperclip
import webbrowser
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QToolBar
import sys
from PySide6 import QtWidgets, QtCore
import argparse
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=preferredColorScheme=1"

back_icon = QIcon("assets/light/back_icon.svg")
forward_icon = QIcon("assets/light/forward_icon.svg")
reload_icon = QIcon("assets/light/reload_icon.svg")
open_icon = QIcon("assets/light/open_browser_icon.svg")
copy_icon = QIcon("assets/light/copy_icon.svg")

def open_in_browser(url):
    webbrowser.open(url)
    return None

def copy_to_clipboard(text):
    pyperclip.copy(text)
    return None

class WebViewer(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.load(QUrl("https://google.com"))

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.clear()

        back_action = QAction("Back", self, icon=back_icon)
        back_action.triggered.connect(self.go_back)
        menu.addAction(back_action)

        forward_action = QAction("Forward", self, icon=forward_icon)
        forward_action.triggered.connect(self.go_forward)
        menu.addAction(forward_action)

        menu.addSeparator()

        reload_action = QAction("Reload", self, icon=reload_icon)
        reload_action.triggered.connect(self.reload_page)
        menu.addAction(reload_action)

        menu.addSeparator()

        open_browser_action = QAction("Open in Browser", self, icon=open_icon)
        open_browser_action.triggered.connect(lambda: open_in_browser(self.get_webpage_url()))
        menu.addAction(open_browser_action)

        address_copy_action = QAction("Copy URL to Clipboard", self, icon=copy_icon)
        address_copy_action.triggered.connect(lambda: copy_to_clipboard(self.get_webpage_url()))
        menu.addAction(address_copy_action)

        menu.exec(event.globalPos())
    def go_back(self):
        self.back()

    def go_forward(self):
        self.forward()

    def reload_page(self):
        self.reload()

    def set_url(self, url):
        self.setUrl(QUrl.url(url))

    def get_webpage_title(self):
        return self.title()

    def get_webpage_icon(self):
        return self.icon()

    def get_webpage_url(self):
        return self.url().toString()

class AddressBar(QToolBar):
    def __init__(self, web_viewer):
        super().__init__()
        self.web_viewer = web_viewer

        self.back_button = QtWidgets.QPushButton("", self)
        self.back_button.clicked.connect(self.web_viewer.go_back)
        self.back_button.setIcon(back_icon)

        self.forward_button = QtWidgets.QPushButton("", self)
        self.forward_button.clicked.connect(self.web_viewer.go_forward)
        self.forward_button.setIcon(forward_icon)

        self.reload_button  = QtWidgets.QPushButton("")
        self.reload_button.clicked.connect(self.web_viewer.reload_page)
        self.reload_button.setIcon(reload_icon)

        self.address_bar = QtWidgets.QLineEdit()
        self.address_bar.setReadOnly(True)
        self.address_bar.setPlaceholderText("https://example.com")
        self.address_bar.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.open_browser = QtWidgets.QPushButton("Open in Browser")
        self.open_browser.clicked.connect(lambda: open_in_browser(self.web_viewer.get_webpage_url()))
        self.open_browser.setIcon(open_icon)

        self.address_copy = QtWidgets.QPushButton("Copy to Clipboard")
        self.address_copy.clicked.connect(lambda: copy_to_clipboard(self.web_viewer.get_webpage_url()))
        self.address_copy.setIcon(copy_icon)

        self.addWidget(self.back_button)
        self.addWidget(self.forward_button)
        self.addWidget(self.reload_button)
        self.addWidget(self.address_bar)
        self.addWidget(self.open_browser)
        self.addWidget(self.address_copy)
        self.setMovable(False)

    def set_address_bar_text(self, text):
        self.address_bar.setText(text)


class MainWindow(QMainWindow):
    def __init__(self, initial_url=None):
        super().__init__()

        self.shortcut_escape = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.shortcut_escape.activated.connect(self.close)

        self.setWindowTitle("Preview Browser")
        self.resize(800,600)

        self.web_viewer = WebViewer()
        self.setCentralWidget(self.web_viewer)
        self.address_bar = AddressBar(self.web_viewer)
        self.addToolBar(self.address_bar)

        self.setWindowIcon(QIcon("assets/light/globe_icon.svg"))

        if initial_url:
            self.web_viewer.set_url(QtCore.QUrl(initial_url))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preview Browser")
    parser.add_argument('--url', dest='text' ,type=str, help='URL to pass to the browser')

    args, qt_args = parser.parse_known_args()

    app = QtWidgets.QApplication([sys.argv[0]] + qt_args)
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

    if darkdetect.isDark():
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
        back_icon = QIcon("assets/dark/back_icon.svg")
        forward_icon = QIcon("assets/dark/forward_icon.svg")
        reload_icon = QIcon("assets/dark/reload_icon.svg")
        open_icon = QIcon("assets/dark/open_browser_icon.svg")
        copy_icon = QIcon("assets/dark/copy_icon.svg")

    window = MainWindow(initial_url=args.text)
    window.show()
    window.web_viewer.titleChanged.connect(
        lambda _: window.setWindowTitle(f"Preview Browser - {window.web_viewer.get_webpage_title()}")
    )
    window.web_viewer.titleChanged.connect(
        lambda _: window.address_bar.set_address_bar_text(window.web_viewer.get_webpage_url())
    )

    sys.exit(app.exec())