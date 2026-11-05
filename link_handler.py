import subprocess
import sys

def main():
    browser_path = r'C:\Users\1744304\PycharmProjects\preview-browser\dist\Preview-Browser.exe'
    target_url = "https://google.com"

    if len(sys.argv) > 1:
        target_url = sys.argv[1]

    arguments = ["--url", target_url]

    subprocess.Popen([browser_path] + arguments)
if __name__ == '__main__':
    main()