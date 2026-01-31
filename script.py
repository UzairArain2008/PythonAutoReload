import time
import random
import sys
import threading

from functions import (
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
    "https://www.freelancer.pk/u/UzairArain554",
    "https://www.upwork.com/freelancers/~016bc28994db577ad5",
    "https://www.fiverr.com/sellers/uzair_programs/edit",
]

keep_awake_input = input(
    "[•] Keep system awake? (True/False): "
).strip().lower()
keep_awake = keep_awake_input == "true"

print("[•] Default websites: Fiverr, Upwork, Freelancer")
change_links = input(
    "[•] Change websites? (T/F): "
).strip().upper()

websites = default_websites

if change_links == "T":
    try:
        count = int(input("[•] How many websites: "))
        if count <= 0:
            raise ValueError

        websites = []
        for i in range(count):
            url = input(f"Enter website {i + 1}: ")
            websites.append(url)

    except ValueError:
        print("[✗] Invalid number of websites.")
        sys.exit(1)

try:
    num_reload_cycles = int(
        input("[•] Reload cycles per interval: ")
    )
    if num_reload_cycles <= 0:
        raise ValueError
except ValueError:
    print("[✗] Invalid reload cycle count.")
    sys.exit(1)

if __name__ == "__main__":
    main(websites, num_reload_cycles, keep_awake)
