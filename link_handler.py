import socket
import threading
import json
import pystray
import os
import re
import winreg

import psutil
import ctypes
import subprocess
import sys

from PIL import Image, ImageDraw

preview_apps = ["Slack.exe"]
regular_browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
preview_browser_path = r'C:\Users\1744304\PycharmProjects\preview-browser\dist\Preview-Browser.exe'

HOST = "127.0.0.1"
PORT = 42053
server_socket = None

def route_url(url: str, preview = False):
    if preview:
        arguments = ["--url", url]
        subprocess.Popen([preview_browser_path] + arguments)
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
    except Exception as e:
        return None

def process_incoming_click(url, app_info):
    app_name = app_info.get("name") if isinstance(app_info, dict) else None

    if not url:
        url = "https://google.com/"

    if app_name in preview_apps:
        route_url(url, preview=True)
    else:
        route_url(url, preview=False)

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

def on_exit(icon, item):
    if server_socket:
        server_socket.close()
    icon.stop()
    os._exit(0)

menu = pystray.Menu(
    pystray.MenuItem("Exit", on_exit)
)
icon = pystray.Icon(
    name="PreviewBrowser",
    icon=create_image(),
    title="Preview Browser and Link Router",
    menu=menu
)

def find_all_installed_browsers():
    browsers = []
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Clients\StartMenuInternet"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Clients\StartMenuInternet")
    ]
    for hive, base_path in reg_paths:
        try:
            with winreg.OpenKey(hive, base_path) as base_key:
                for i in range(winreg.QueryInfoKey(base_key)[0]):
                    subkey_name = winreg.EnumKey(base_key, i)
                    try:
                        cmd_path = fr"{base_path}\{subkey_name}\shell\open\command"
                        with winreg.OpenKey(hive, cmd_path) as cmd_key:
                            raw_command = winreg.QueryValue(cmd_key, None)
                            clean_path = re.sub(r'(^"[^"]+"|^[^\s]+).*', r'\1', raw_command).strip('"')

                            if os.path.exists(clean_path) and clean_path not in browsers:
                                browsers.append(clean_path)
                    except Exception:
                        continue
        except Exception:
            continue
    return browsers

def main():
    global server_socket

    originating_app = get_active_app()
    target_url = sys.argv[1] if len(sys.argv) > 1 else None

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
    except OSError:
        forward_to_running_instance(target_url, originating_app)

    threading.Thread(target=socket_listener, daemon=True).start()

    if target_url:
        threading.Thread(target=process_incoming_click, args=(target_url, originating_app), daemon=True).start()

    icon.run()
if __name__ == '__main__':
    main()