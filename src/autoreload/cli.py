import os
import sys
import time
import random
import threading
from datetime import datetime
import argparse
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

from .core.functions import (
    keep_system_awake,
    find_brave_executable,
    focus_brave_window,
    open_urls_in_brave,
    reload_cycle,
    cursor_movement_thread,
)

VERSION = "0.1.0"

# -----------------------------
# Terminal utilities & banner
# -----------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print(Fore.YELLOW + Style.BRIGHT + "        AUTO RELOAD CLI")
    print(Fore.GREEN + f"    Version: {VERSION}")
    print(Fore.MAGENTA + f"    Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.CYAN + Style.BRIGHT + "="*50 + "\n")

# -----------------------------
# Logging helpers
# -----------------------------
def log_info(msg):
    print(Fore.BLUE + "[INFO] " + Style.RESET_ALL + msg)

def log_success(msg):
    print(Fore.GREEN + "[ OK ] " + Style.RESET_ALL + msg)

def log_warning(msg):
    print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + msg)

def log_error(msg):
    print(Fore.RED + "[ERR ] " + Style.RESET_ALL + msg)

# -----------------------------
# User configuration prompts
# -----------------------------
def prompt_user_config():
    default_websites = [
        "https://www.freelancer.pk/dashboard",
        "https://upwork.com",
        "https://www.fiverr.com/seller_dashboard",
    ]

    websites = default_websites.copy()

    change_links = input("[INFO] Change websites? (T/F): ").strip().upper()
    if change_links == "T":
        try:
            count = int(input("[INFO] Number of websites: "))
            websites = []
            for i in range(count):
                url = input(f"[INFO] Enter website {i+1}: ").strip()
                websites.append(url)
        except ValueError:
            log_error("Invalid number")
            sys.exit(1)

    keep_awake_input = input("[INFO] Keep system awake? (True/False): ").strip().lower()
    keep_awake = keep_awake_input == "true"

    try:
        min_interval = int(input("[INFO] Min interval (seconds, default 120): ") or 120)
        max_interval = int(input("[INFO] Max interval (seconds, default 180): ") or 180)
        if min_interval <= 0 or max_interval <= 0 or min_interval > max_interval:
            raise ValueError
    except ValueError:
        log_warning("Invalid interval input. Using defaults 120–180s.")
        min_interval, max_interval = 120, 180

    return websites, keep_awake, min_interval, max_interval

# -----------------------------
# Main logic
# -----------------------------
def main(websites, keep_awake, min_interval=120, max_interval=180):
    num_reload_cycles = len(websites)
    brave_path = find_brave_executable()

    if not brave_path:
        log_error("Brave browser not found.")
        sys.exit(1)

    log_success(f"Brave browser detected: {brave_path}")
    log_info(f"Websites to refresh ({num_reload_cycles}):")
    for site in websites:
        print(f"    - {site}")

    if keep_awake:
        keep_system_awake(True)

    cursor_thread = threading.Thread(target=cursor_movement_thread, daemon=True)
    cursor_thread.start()

    open_urls_in_brave(websites, brave_path)
    time.sleep(2)
    focus_brave_window()

    log_info("Monitoring started — press Ctrl+C to exit")

    try:
        while True:
            interval = random.randint(min_interval, max_interval)
            log_info(f"Next reload scheduled in {interval} seconds")
            time.sleep(interval)

            focus_brave_window()
            reload_cycle(num_cycles=num_reload_cycles)

            if keep_awake:
                keep_system_awake(True)

    except KeyboardInterrupt:
        log_warning("Shutting down gracefully...")
        keep_system_awake(False)
        sys.exit(0)

    except Exception as e:
        log_error(f"Unexpected error: {e}")
        keep_system_awake(False)
        sys.exit(1)

# -----------------------------
# CLI entry point
# -----------------------------
def main_entry():
    parser = argparse.ArgumentParser(
        prog="autoreload",
        description="AutoReload CLI — browser automation tool"
    )

    # Optional arguments
    parser.add_argument(
        "--version",
        action="version",
        version=f"AutoReload CLI {VERSION}",
        help="Show the version and exit"
    )

    parser.add_argument(
        "--websites", nargs='+', help="List of websites to reload"
    )
    parser.add_argument(
        "--keep-awake", type=str, choices=["True", "False"], help="Keep system awake"
    )
    parser.add_argument(
        "--min-interval", type=int, help="Minimum reload interval in seconds"
    )
    parser.add_argument(
        "--max-interval", type=int, help="Maximum reload interval in seconds"
    )

    args = parser.parse_args()

    clear_screen()
    show_banner()

    # Use CLI args if provided, otherwise fallback to interactive prompts
    if args.websites or args.keep_awake or args.min_interval or args.max_interval:
        websites = args.websites if args.websites else [
            "https://www.freelancer.pk/dashboard",
            "https://upwork.com",
            "https://www.fiverr.com/seller_dashboard"
        ]
        keep_awake = args.keep_awake == "True" if args.keep_awake else False
        min_interval = args.min_interval if args.min_interval else 120
        max_interval = args.max_interval if args.max_interval else 180
    else:
        websites, keep_awake, min_interval, max_interval = prompt_user_config()

    main(websites, keep_awake, min_interval, max_interval)


if __name__ == "__main__":
    main_entry()