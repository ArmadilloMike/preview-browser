import json
import os.path
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

CONFIG_LOCATION = Path(os.path.expandvars(r"%APPDATA%\PreviewBrowser\config.json"))

def load_config():
    try:
        with open(CONFIG_LOCATION, "r", encoding="utf-8") as file:
            data = json.load(file)
        preview_apps = data["preview-apps"]
        regular_browser = data["regular-browser-path"]
        preview_browser = data["preview-browser-path"]
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

class ConfigWindow(tk.Toplevel):
    def __init__(self, parent, on_save_callback=None):
        super().__init__(parent)
        self.title("Preview Browser Config")
        self.geometry("530x360")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.on_save_callback = on_save_callback

        apps, reg_browser, prev_browser = load_config()

        self.reg_browser_var = tk.StringVar(value=reg_browser)
        self.prev_browser_var = tk.StringVar(value=prev_browser)
        self.new_app_var = tk.StringVar()

        self.create_widgets(apps)

    def create_widgets(self, initial_apps):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Regular Browser Path:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.reg_browser_var, width=55).grid(row=1, column=0, pady=(2, 10), padx=(0, 5))
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_exe(self.reg_browser_var)).grid(row=1, column=1, pady=(2,10))

        ttk.Label(frame, text="Preview Browser Path:").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.prev_browser_var, width=55).grid(row=3, column=0, pady=(2, 15), padx=(0, 5))
        ttk.Button(frame, text="Browse...", command=lambda: self.browse_exe(self.prev_browser_var)).grid(row=3, column=1, pady=(2, 15))

        ttk.Label(frame, text="Preview Apps (Slack.exe)").grid(row=4, column=0, sticky="w")
        add_frame = ttk.Frame(frame)
        add_frame.grid(row=5, column=0, columnspan=2, sticky="we", pady=(2, 5))
        ttk.Entry(add_frame, textvariable=self.new_app_var, width=40).pack(side="left", padx=(0, 5))
        ttk.Button(add_frame, text="Add App", command=self.add_app).pack(side="left")
        ttk.Button(add_frame, text="Remove Selected", command=self.remove_app).pack(side="left", padx=(5, 0))

        self.apps_listbox = tk.Listbox(frame, height=5, width=55)
        self.apps_listbox.grid(row=6, column=0, columnspan=2, sticky="we", pady=(0, 15))
        for app in initial_apps:
            self.apps_listbox.insert(tk.END, app)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, sticky="e")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=(5, 0))
        ttk.Button(btn_frame, text="Save", command=self.save_and_close).pack(side="right")

    def browse_exe(self, target_var):
        filepath = filedialog.askopenfilename(
            title="Select Exe File",
            filetypes=[("Exe Files", "*.exe"), ("All Files","*.*")]
        )
        if filepath:
            target_var.set(str(Path(filepath)))

    def add_app(self):
        app_name = self.new_app_var.get().strip()
        if app_name and app_name not in self.apps_listbox.get(0, tk.END):
            self.apps_listbox.insert(tk.END, app_name)
            self.new_app_var.set("")

    def remove_app(self):
        selected = self.apps_listbox.curselection()
        if selected:
            self.apps_listbox.delete(selected[0])

    def save_and_close(self):
        apps_list = list(self.apps_listbox.get(0, tk.END))

        save_config(
            preview_apps=apps_list,
            regular_browser=self.reg_browser_var.get(),
            preview_browser=self.prev_browser_var.get()
        )

        if self.on_save_callback:
            self.on_save_callback()
        self.destroy()