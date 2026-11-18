import json
import os.path
from pathlib import Path

CONFIG_LOCATION = Path(os.path.expandvars(r"%APPDATA%\PreviewBrowser\config.json"))

def load_config():
    try:
        with open(CONFIG_LOCATION, "r", encoding="utf-8") as file:
            data = json.load(file)
        preview_apps = data["preview-apps"]
        regular_browser = data["regular-browser-path"]
        preview_browser = data["preview-bowser-path"]
    except FileNotFoundError:
        preview_apps = ["Slack.exe"]
        regular_browser = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        preview_browser = "C:\\Users\\1744304\\PycharmProjects\\preview-browser\\dist\\preview-browser\\preview-browser.exe"
    return preview_apps, regular_browser, preview_browser

def save_config(preview_apps = None, regular_browser = None, preview_browser = None):
    config_data = {
        "preview-apps": preview_apps,
        "regular-browser-path": regular_browser,
        "preview-browser-path": preview_browser
    }
    CONFIG_LOCATION.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_LOCATION, "w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=4)