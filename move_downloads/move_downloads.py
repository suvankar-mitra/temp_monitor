# This script moves files from the Downloads/complete directory to a specified SSD directory.
# It checks if the files are stable (not being written to) before moving them.
# It also sources environment variables from .zshrc to get the destination path.

#!/usr/bin/env python3

import os
import shutil
import time
from pathlib import Path

# Load environment variables by sourcing .zshrc
import subprocess
subprocess.call(['zsh', '-c', 'source ~/.zshrc && env > /tmp/env_vars'])

# Inject sourced env vars into Python's os.environ
with open('/tmp/env_vars') as f:
    for line in f:
        key, _, value = line.partition("=")
        os.environ[key.strip()] = value.strip()

# Fetch destination directory from $SSD2TB
ssd2tb_path = os.environ.get("SSD2TB")
if not ssd2tb_path:
    raise EnvironmentError("SSD2TB environment variable not set. Please define it in your .zshrc")

SOURCE_DIR = Path.home() / "Downloads" / "complete"
DEST_DIR = Path(ssd2tb_path)
CHECK_INTERVAL = 60  # seconds
STABILITY_WAIT = 3  # seconds

def is_file_stable(path):
    try:
        initial_size = path.stat().st_size
        time.sleep(STABILITY_WAIT)
        final_size = path.stat().st_size
        return initial_size == final_size
    except FileNotFoundError:
        return False

def move_items():
    if not SOURCE_DIR.exists():
        print(f"Source directory {SOURCE_DIR} does not exist.")
        return

    for item in SOURCE_DIR.iterdir():
        target = DEST_DIR / item.name
        if is_file_stable(item):
            try:
                shutil.move(str(item), str(target))
                print(f"Moved: {item} → {target}")
            except Exception as e:
                print(f"Failed to move {item}: {e}")
        else:
            print(f"Skipping (not stable): {item}")

def main():
    while True:
        move_items()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
