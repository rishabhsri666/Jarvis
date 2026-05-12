import psutil
import os

def get_battery():

    battery = psutil.sensors_battery()

    if battery:

        return f"Battery is at {battery.percent} percent"

    return "Battery information not available"


def shutdown_pc():

    os.system("shutdown /s /t 1")


def restart_pc():

    os.system("shutdown /r /t 1")


def lock_pc():

    os.system("rundll32.exe user32.dll,LockWorkStation")