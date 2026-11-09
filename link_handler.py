import psutil
import ctypes
import subprocess
import sys

preview_apps = ["Slack.exe"]
regular_browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

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


def main():
    originating_app = get_active_app()
    browser_path = r'C:\Users\1744304\PycharmProjects\preview-browser\dist\Preview-Browser.exe'
    target_url = f"https://google.com/search?q={originating_app["name"]}"

    if len(sys.argv) > 1:
        target_url = sys.argv[1]

    if originating_app["name"] in preview_apps:
        arguments = ["--url", target_url]
        subprocess.Popen([browser_path] + arguments)
    else:
        subprocess.Popen([regular_browser_path, target_url])
if __name__ == '__main__':
    main()