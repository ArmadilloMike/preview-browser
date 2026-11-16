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

# System Tray Icon
def create_image():
    image = Image.new('RGB', (64, 64), color=(30, 144, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image

def on_exit(icon, item):
    icon.stop()

menu = pystray.Menu(
    pystray.MenuItem("Exit", on_exit)
)
icon = pystray.Icon(
    name="PreviewBrowser",
    icon=create_image(),
    title="Preview Browser and Link Router",
    menu=menu
)

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
        return f"error: {e}"

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
    originating_app = get_active_app()
    browser_path = r'C:\Users\1744304\PycharmProjects\preview-browser\dist\Preview-Browser.exe'
    target_url = f"https://google.com/search?q={originating_app["name"]}"
    icon.run()

    if len(sys.argv) > 1:
        target_url = sys.argv[1]

    if originating_app["name"] in preview_apps:
        arguments = ["--url", target_url]
        subprocess.Popen([browser_path] + arguments)
    else:
        subprocess.Popen([regular_browser_path, target_url])
if __name__ == '__main__':
    main()