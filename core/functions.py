import ctypes
import time
import random
import subprocess
import sys
import threading
from pathlib import Path
import pyautogui

ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

try:
    ctypes.windll.kernel32.SetThreadExecutionState.argtypes = [ctypes.c_ulong]
    ctypes.windll.kernel32.SetThreadExecutionState.restype = ctypes.c_ulong
except AttributeError:
    print("Error: This application requires Windows.")
    sys.exit(1)

def keep_system_awake(enable: bool = True):
    if enable:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
        )
        print("[✓] System wake-lock enabled")
    else:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("[✓] System wake-lock disabled")


def find_brave_executable():
    possible_paths = [
        Path(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"),
        Path(r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"),
        Path.home() / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "Application" / "brave.exe"
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    return None


def focus_brave_window():
    """
    Focus the Brave browser window.
    """
    try:
        # Get the foreground window
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        # Set it to foreground
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.2)
    except Exception as e:
        print(f"[!] Could not focus window: {e}")


def press_ctrl_tab():
    """
    Press and release Ctrl+Tab quickly.
    """
    VK_CONTROL = 0x11
    VK_TAB = 0x09
    
    # Press Ctrl
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.05)
    
    # Press Tab
    ctypes.windll.user32.keybd_event(VK_TAB, 0, 0, 0)
    time.sleep(0.05)
    
    # Release Tab
    ctypes.windll.user32.keybd_event(VK_TAB, 0, 2, 0)
    time.sleep(0.05)
    
    # Release Ctrl
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.1)
    
    print("[↻] Pressed Ctrl+Tab")


def press_ctrl_r():
    """
    Press and release Ctrl+R to reload the page.
    """
    VK_CONTROL = 0x11
    VK_R = 0x52
    
    # Press Ctrl
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.05)
    
    # Press R
    ctypes.windll.user32.keybd_event(VK_R, 0, 0, 0)
    time.sleep(0.05)
    
    # Release R
    ctypes.windll.user32.keybd_event(VK_R, 0, 2, 0)
    time.sleep(0.05)
    
    # Release Ctrl
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.1)
    
    print("[↻] Pressed Ctrl+R (reload)")


def open_urls_in_brave(websites, brave_path):
    """
    Open all websites in Brave browser (each in a new tab).
    
    Args:
        websites (list): List of URLs to open
        brave_path (str): Path to brave.exe
    """
    try:
        # Open first URL
        subprocess.Popen([brave_path, websites[0]])
        print(f"[•] Opened Brave with: {websites[0]}")
        time.sleep(3)
        
        # Open remaining URLs in new tabs
        for url in websites[1:]:
            subprocess.Popen([brave_path, "--new-tab", url])
            print(f"[•] Opened in new tab: {url}")
            time.sleep(1)
    
    except Exception as e:
        print(f"[✗] Error opening URLs: {e}")


def reload_cycle(num_cycles: int = 1):
    for cycle in range(num_cycles):
        print(f"\n[•] Cycle {cycle + 1}/{num_cycles}")
        press_ctrl_tab()
        time.sleep(0.3)
        press_ctrl_r()
        time.sleep(1)



def cursor_movement_thread():
    """
    Background thread for continuous cursor movement.
    Prevents screen from going to sleep by moving the cursor randomly.
    """
    screen_width, screen_height = pyautogui.size()
    
    try:
        while True:
            # Generate random coordinates
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            
            # Move the cursor with animation
            pyautogui.moveTo(x, y, duration=0.25)
            
            # Wait for a random interval before the next move
            time.sleep(random.uniform(0.5, 2.0))
    
    except Exception as e:
        print(f"[!] Cursor movement error: {e}")

