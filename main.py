import time
import random
import sys
import threading

from core.functions import (
    keep_system_awake,
    find_brave_executable,
    focus_brave_window,
    open_urls_in_brave,
    reload_cycle,
    cursor_movement_thread,
)


def main(websites, keep_awake, min_interval=120, max_interval=180):
    num_reload_cycles = len(websites)  # one reload per website

    brave_path = find_brave_executable()
    if not brave_path:
        print("[✗] Brave browser not found.")
        sys.exit(1)

    print("[•] Brave browser found:", brave_path)
    print(f"[•] Websites to refresh ({num_reload_cycles}):")
    for site in websites:
        print(f"    - {site}")

    if keep_awake:
        keep_system_awake(True)

    cursor_thread = threading.Thread(
        target=cursor_movement_thread, daemon=True
    )
    cursor_thread.start()

    open_urls_in_brave(websites, brave_path)
    time.sleep(2)
    focus_brave_window()

    print("[•] Application started. Press Ctrl+C to stop.")

    try:
        while True:
            interval = random.randint(min_interval, max_interval)
            print(f"[⏱] Next reload in {interval} seconds")
            time.sleep(interval)

            focus_brave_window()
            reload_cycle(num_cycles=num_reload_cycles)

            if keep_awake:
                keep_system_awake(True)

    except KeyboardInterrupt:
        print("\n[•] Stopping application...")
        keep_system_awake(False)
        sys.exit(0)

    except Exception as e:
        print(f"[✗] Error: {e}")
        keep_system_awake(False)
        sys.exit(1)


default_websites = [
    "https://www.freelancer.pk/dashboard",
    "https://upwork.com",
    "https://www.fiverr.com/seller_dashboard",
]

websites = default_websites.copy()

change_links = input("[•] Do you want to change websites? (T/F): ").strip().upper()
if change_links == "T":
    try:
        count = int(input("[•] How many websites you want to refresh? "))
        if count <= 0:
            raise ValueError
        websites = []
        for i in range(count):
            url = input(f"Enter website {i + 1}: ").strip()
            websites.append(url)
    except ValueError:
        print("[✗] Invalid number of websites.")
        sys.exit(1)

keep_awake_input = input("[•] Keep system awake? (True/False): ").strip().lower()
keep_awake = keep_awake_input == "true"

try:
    min_interval = int(input("[•] Minimum interval in seconds (default 120): ") or 120)
    max_interval = int(input("[•] Maximum interval in seconds (default 180): ") or 180)
    if min_interval <= 0 or max_interval <= 0 or min_interval > max_interval:
        raise ValueError
except ValueError:
    print("[✗] Invalid interval input. Using defaults 120–180s.")
    min_interval, max_interval = 120, 180

if __name__ == "__main__":
    main(websites, keep_awake, min_interval, max_interval)
