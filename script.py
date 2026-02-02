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


def main(websites, num_reload_cycles, keep_awake):
    min_interval = 120
    max_interval = 180

    brave_path = find_brave_executable()
    if not brave_path:
        print("[✗] Brave browser not found.")
        sys.exit(1)

    print("[•] Brave browser found:", brave_path)

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


# ================= USER INPUT =================

default_websites = [
    "https://www.freelancer.pk/dashboard",
    "https://upwork.com",
    "https://www.fiverr.com/seller_dashboard",
]

keep_awake_input = input(
    "[•] Keep system awake? (True/False): "
).strip().lower()
keep_awake = keep_awake_input == "true"

print("[•] Default websites are: Fiverr, Upwork, Freelancer")
change_links = input(
    "[•] Want to Change websites? (T/F): "
).strip().upper()

websites = default_websites

if change_links == "T":
    try:
        count = int(input("[•] How many websites You want to Refresh (ex: 2): "))
        if count <= 0:
            raise ValueError

        websites = []
        for i in range(count):
            url = input(f"Enter website {i + 1}: ")
            websites.append(url)

    except ValueError:
        print("[✗] Invalid number of websites.")
        sys.exit(1)

num_reload_cycles = len(websites)

if __name__ == "__main__":
    main(websites, num_reload_cycles, keep_awake)
