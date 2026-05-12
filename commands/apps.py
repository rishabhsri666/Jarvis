import subprocess
import os

apps = {
    "calculator": "calc.exe",
    "powershell": "powershell.exe",
    "chrome": "chrome.exe",
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "spotify": "spotify.exe",
    "vscode": "code"
}

folders = {
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "desktop": os.path.expanduser("~/Desktop"),
    "pictures": os.path.expanduser("~/Pictures"),
    "music": os.path.expanduser("~/Music"),
    "videos": os.path.expanduser("~/Videos")
}


def open_app(app_name):

    if app_name in apps:

        subprocess.Popen(apps[app_name])

        return True

    return False


def open_folder(folder_name):

    if folder_name in folders:

        os.startfile(folders[folder_name])

        return True

    return False