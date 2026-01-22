import ctypes
import time
import random
import subprocess
import sys
from pathlib import Path

ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

try:
    ctypes.windll.kernel32.SetThreadExecutionState.argtypes = [ctypes.c_ulong]
    ctypes.windll.kernel32.SetThreadExecutionState.restype = ctypes.c_ulong
except AttributeError:
    print("Error: This application requires Windows.")
    sys.exit(1)


def keep_system_awake(enable=True):
    """
    Prevent Windows from sleeping or turning off the display.
    
    Args:
        enable (bool): True to keep system awake, False to allow sleep
    """
    if enable:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
        )
        print("[✓] System wake-lock enabled")
    else:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("[✓] System wake-lock disabled")


def find_brave_executable():
    """
    Locate the Brave browser executable on the system.
    
    Returns:
        str: Path to brave.exe or None if not found
    """
    possible_paths = [
        Path(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"),
        Path(r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"),
        Path.home() / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "Application" / "brave.exe"
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    return None


def open_url_in_brave(url, brave_path):
    """
    Open a URL in Brave browser using a new tab.
    
    Args:
        url (str): Website URL to open
        brave_path (str): Path to brave.exe
    """
    try:
        subprocess.Popen([brave_path, "--new-tab", url])
        print(f"[↻] Opened: {url}")
        time.sleep(3)
    except Exception as e:
        print(f"[✗] Error opening {url}: {e}")


def close_brave_tab():
    """
    Close the current Brave tab using Alt+F4 (closes window) or Ctrl+W (closes tab).
    Uses Ctrl+W which is more reliable for closing individual tabs.
    """
    try:
        time.sleep(0.5)
        import win32api
        import win32con
        
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYDOWN, win32con.VK_W, 0)
        ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
        time.sleep(0.1)
        ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYUP, win32con.VK_W, 0)
        ctypes.windll.user32.PostMessageW(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)
        
        print(f"[✗] Closed tab")
        time.sleep(1)
    except Exception as e:
        try:
            press_ctrl_w()
            print(f"[✗] Closed tab (fallback)")
            time.sleep(1)
        except Exception as e2:
            print(f"[!] Could not close tab: {e2}")


def press_ctrl_w():
    """
    Press Ctrl+W using ctypes keyboard simulation.
    """
    VK_CONTROL = 0x11
    VK_W = 0x57
    
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.05)
    
    ctypes.windll.user32.keybd_event(VK_W, 0, 0, 0)
    time.sleep(0.05)
    
    ctypes.windll.user32.keybd_event(VK_W, 0, 2, 0)
    time.sleep(0.05)
    
    ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 2, 0)


def reload_url_in_brave(url, brave_path, is_first=False):
    """
    Close previous tab (if not first) and open a new URL in Brave.
    
    Args:
        url (str): Website URL to open
        brave_path (str): Path to brave.exe
        is_first (bool): Whether this is the first website
    """
    try:
        if not is_first:
            close_brave_tab()
        
        open_url_in_brave(url, brave_path)
        
    except Exception as e:
        print(f"[✗] Error reloading {url}: {e}")


def main():
    """Main application loop."""
    
    websites = [
        "https://www.fiverr.com/sellers/uzair_programs/edit",
        "https://www.freelancer.pk/u/UzairArain554",
        "https://www.upwork.com/freelancers/~016bc28994db577ad5",
    ]
    
    min_interval = 100
    max_interval = 500
    
    brave_path = find_brave_executable()
    if not brave_path:
        print("[✗] Brave browser not found. Please install Brave.")
        print("    Download from: https://brave.com/download/")
        sys.exit(1)
    
    print("[•] Brave browser found at:", brave_path)
    print(f"[•] Configured websites: {len(websites)}")
    for i, site in enumerate(websites, 1):
        print(f"    {i}. {site}")
    
    keep_system_awake(True)
    
    print("[•] Application started. Press Ctrl+C to stop.")
    print(f"[•] Reload interval: {min_interval}–{max_interval} seconds")
    print()
    
    is_first_iteration = True
    
    try:
        while True:
            interval = random.randint(min_interval, max_interval)
            print(f"[⏱] Next reload cycle in {interval} seconds...")
            
            time.sleep(interval)
            
            print(f"[•] Starting reload cycle...")
            
            for idx, selected_url in enumerate(websites):
                is_first_tab = is_first_iteration and (idx == 0)
                reload_url_in_brave(selected_url, brave_path, is_first=is_first_tab)
                time.sleep(2)
            
            is_first_iteration = False
            
            keep_system_awake(True)
            print()
    
    except KeyboardInterrupt:
        print("\n[•] Stopping application...")
        keep_system_awake(False)
        print("[✓] System wake-lock disabled. Normal sleep behavior restored.")
        sys.exit(0)
    
    except Exception as e:
        print(f"[✗] Unexpected error: {e}")
        keep_system_awake(False)
        sys.exit(1)


if __name__ == "__main__":
    main()
