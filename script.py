import ctypes
import time
import random
import subprocess
import sys
import threading
from pathlib import Path
import pyautogui

# Windows API constants for system wake-lock
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

# Get SetThreadExecutionState function from Windows API
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
        # Keep system and display awake
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
        )
        print("[✓] System wake-lock enabled")
    else:
        # Allow normal sleep behavior
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


def reload_cycle(num_cycles=3):
    """
    Perform the reload cycle: Ctrl+Tab followed by Ctrl+R, repeated num_cycles times.
    
    Args:
        num_cycles (int): Number of times to repeat the cycle
    """
    for cycle in range(num_cycles):
        print(f"\n[•] Cycle {cycle + 1}/{num_cycles}")
        
        # Press Ctrl+Tab (switch to next tab)
        press_ctrl_tab()
        time.sleep(0.3)
        
        # Press Ctrl+R (reload)
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


def main():
    """Main application loop."""
    
    # Configuration: Add your websites here
    websites = [
        "https://www.freelancer.pk/u/UzairArain554",
        "https://www.upwork.com/freelancers/~016bc28994db577ad5",
        "https://www.fiverr.com/sellers/uzair_programs/edit",
    ]
    
    min_interval = 120  # seconds (2 minutes)
    max_interval = 180  # seconds (3 minutes)
    
    # Find Brave browser
    brave_path = find_brave_executable()
    if not brave_path:
        print("[✗] Brave browser not found. Please install Brave.")
        print("    Download from: https://brave.com/download/")
        sys.exit(1)
    
    print("[•] Brave browser found at:", brave_path)
    print(f"[•] Configured websites: {len(websites)}")
    for i, site in enumerate(websites, 1):
        print(f"    {i}. {site}")
    
    # Enable system wake-lock
    keep_system_awake(True)
    
    # Start cursor movement in a background thread (daemon thread)
    cursor_thread = threading.Thread(target=cursor_movement_thread, daemon=True)
    cursor_thread.start()
    print("[•] Cursor movement thread started")
    
    # Open all websites
    open_urls_in_brave(websites, brave_path)
    time.sleep(2)
    
    # Focus Brave window
    focus_brave_window()
    
    print("[•] Application started. Press Ctrl+C to stop.")
    print(f"[•] Reload interval: {min_interval}–{max_interval} seconds")
    print()
    
    try:
        while True:
            # Randomly select interval
            interval = random.randint(min_interval, max_interval)
            print(f"\n[⏱] Next reload cycle in {interval} seconds...")
            
            # Wait for the interval
            time.sleep(interval)
            
            # Focus Brave window
            focus_brave_window()
            
            print(f"[•] Starting reload cycle...")
            
            # Perform reload cycle 3 times
            reload_cycle(num_cycles=3)
            
            # Refresh system wake-lock to ensure it stays active
            keep_system_awake(True)
    
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