import time
import socket
import threading
import json
import pystray
import os
import psutil
import ctypes
import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageDraw
import pygetwindow
from link_handler_ui import ConfigWindow

preview_apps = ["Slack.exe"]
regular_browser_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
preview_browser_path = "C:\\Users\\1744304\\PycharmProjects\\preview-browser\\dist\\preview-browser\\mpreview-browser.exe"

CONFIG_LOCATION = os.path.expandvars(r"%APPDATA%\PreviewBrowser\config.json")

HOST = "127.0.0.1"
PORT = 42053
server_socket = None


# Configuration

def load_config():
    global preview_apps, regular_browser_path, preview_browser_path

    try:
        with open(CONFIG_LOCATION, "r", encoding="utf-8") as file:
            data = json.load(file)

        preview_apps = data["preview-apps"]
        regular_browser_path = data["regular-browser-path"]
        preview_browser_path = data["preview-browser-path"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass


# Routing

def route_url(url: str, preview = False):
    if preview:
        arguments = ["--url", url]
        subprocess.Popen([preview_browser_path] + arguments)
        time.sleep(0.5)
        windows = pygetwindow.getWindowsWithTitle("Preview Browser")
        if windows:
            win = windows[0]
            if win.isMinimized:
                win.restore()
            ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)
            win.activate()
    else:
        subprocess.Popen([regular_browser_path, url])

def get_active_app():
    try:
        handle = ctypes.windll.user32.GetForegroundWindow()
        if not handle:
            return None

        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(handle, ctypes.byref(pid))

        if pid.value == 0: return None

        proc = psutil.Process(pid.value)
        return {
            "pid": proc.pid,
            "name": proc.name(),
            "exe": proc.exe()
        }
    except Exception:
        return None

def process_incoming_click(url, app_info):
    app_name = app_info.get("name") if isinstance(app_info, dict) else None

    if not url:
        url = "https://google.com/"

    if app_name in preview_apps:
        route_url(url, preview=True)
    else:
        route_url(url, preview=False)

# Sockets

def socket_listener():
    while True:
        try:
            conn, _ = server_socket.accept()  # ty: ignore[unresolved-attribute]
            with conn:
                data = conn.recv(4096)
                if data:
                    payload = json.loads(data.decode("utf-8"))
                    url = payload.get("url")
                    app_info = payload.get("app_info")
                    threading.Thread(target=process_incoming_click, args=(url, app_info), daemon=True).start()
        except OSError:
            break

def forward_to_running_instance(url, app_info):
    try:
        payload = json.dumps({"url": url, "app_info": app_info}).encode("utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(2.0)
            client.connect((HOST, PORT))
            client.sendall(payload)
    except Exception:
        process_incoming_click(url, app_info)
    sys.exit(0)

# System Tray Icon

def create_image():
    image = Image.new('RGB', (64, 64), color=(30, 144, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image


def open_config_window(icon, item):
    window = ConfigWindow(
        on_save_callback=load_config  # ty: ignore[unknown-argument]
    )
    window.update()
    window.deiconify()
    window.lift()
    window.focus_force()
    window.mainloop()


def on_exit(icon, item):
    if server_socket:
        server_socket.close()
    icon.stop()
    os._exit(0)

menu = pystray.Menu(
    pystray.MenuItem("Configure", open_config_window),
    pystray.MenuItem("Exit", on_exit)
)
icon = pystray.Icon(
    name="PreviewBrowser",
    icon=create_image(),
    title="Preview Browser and Link Router",
    menu=menu
)

def main():
    global server_socket
    load_config()

    originating_app = get_active_app()
    target_url = sys.argv[1] if len(sys.argv) > 1 else None

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
    except OSError:
        forward_to_running_instance(target_url, originating_app)

    threading.Thread(target=socket_listener, daemon=True).start()

    #threading.Thread(target=icon.run, daemon=True).start()
    #open_config_window(None, None)
    if target_url:
        process_incoming_click(target_url, originating_app)

    icon.run()
if __name__ == '__main__':
    main()