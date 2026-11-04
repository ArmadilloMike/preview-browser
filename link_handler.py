import sys


def main():
    target_url = "https://google.com"

    if len(sys.argv) > 1:
        target_url = sys.argv[1]