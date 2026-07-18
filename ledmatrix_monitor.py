#!/usr/bin/env python3
"""
ledmatrix_monitor.py

Continuously reads CPU or RAM usage and displays it as a percentage bar
on a Framework Laptop 16 LED Matrix Input Module, via ledmatrixctl.

Usage:
    ledmatrix_monitor.py --metric cpu --device /dev/ttyACM1
    ledmatrix_monitor.py --metric ram --device /dev/ttyACM0

Requires:
    pip install --user psutil
    ledmatrixctl must be on PATH (installed via framework16-inputmodule)
"""

import argparse
import subprocess
import sys
import time

try:
    import psutil
except ImportError:
    sys.exit("Missing dependency. Install with: python -m pip install --user psutil")


def get_value(metric: str) -> int:
    if metric == "cpu":
        # interval=None uses the delta since the last call (non-blocking,
        # relies on the sleep() in the main loop to space out samples)
        return int(round(psutil.cpu_percent(interval=None)))
    elif metric == "ram":
        return int(round(psutil.virtual_memory().percent))
    else:
        raise ValueError(f"Unknown metric: {metric}")


def send_percentage(device: str, value: int) -> None:
    value = max(0, min(100, value))
    try:
        subprocess.run(
            ["ledmatrixctl", "--serial-dev", device, "--percentage", str(value)],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        sys.exit("ledmatrixctl not found on PATH. Check `fish_add_path $HOME/.ledmatrix`.")
    except subprocess.CalledProcessError as e:
        print(f"ledmatrixctl error: {e.stderr.strip()}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Display CPU/RAM usage on a Framework LED Matrix module")
    parser.add_argument("--metric", choices=["cpu", "ram"], required=True, help="Which stat to display")
    parser.add_argument("--device", required=True, help="Serial device, e.g. /dev/ttyACM0")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between updates (default: 2)")
    args = parser.parse_args()

    # Prime psutil's internal CPU counter so the first real reading is accurate
    if args.metric == "cpu":
        psutil.cpu_percent(interval=None)
        time.sleep(1)

    print(f"Displaying {args.metric.upper()} usage on {args.device} every {args.interval}s. Ctrl+C to stop.")

    while True:
        value = get_value(args.metric)
        send_percentage(args.device, value)
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
