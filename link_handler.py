import psutil
import os
import sys

def get_triggering_process():
    try:
        parent_pid = os.getppid()
        parent_process = psutil.Process(parent_pid)
        parent_name = parent_process.name()
        parent_exe = parent_process.exe()

        return {"pid": parent_pid, "name": parent_name, "exe": parent_exe}
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # when the app was closed immediately
        return {"pid": None, "name": None, "path": None}


def main():
    target_url = "https://google.com"

    if len(sys.argv) > 1:
        target_url = sys.argv[1]

if __name__ == '__main__':
    main()