# Auto Move Downloads

This project contains a Python script and systemd service to **automatically move completed downloads** from a specific directory to a user-defined destination (like an external drive).

The script ensures that files are no longer being written to before moving them, which is especially useful for large downloads or media files.

---

## 🚀 What It Does

- Periodically checks a downloads folder (every 60 seconds)
- Verifies each file is stable (not being written to)
- Moves stable files and folders to a target directory
- Runs continuously in the background using `systemd`

---

## 📁 Default Source Directory

The script checks this location:

```
$HOME/Downloads/complete
```

---

## 📦 Destination Directory

The destination is **not hardcoded**. Instead, it reads the value from the `SSD2TB` environment variable, which you should define in your shell configuration.

In your shell config (e.g. `~/.zshrc` or `~/.bashrc`), add:

```sh
export SSD2TB=/path/to/your/destination
```

Then run:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

---

## ⚙️ Setting Up the systemd Service (User-level)

### 1. Move the script

```bash
mkdir -p ~/.local/scripts
cp move_downloads.py ~/.local/scripts/
chmod +x ~/.local/scripts/move_downloads.py
```

### 2. Create the systemd unit file

Save this as `~/.config/systemd/user/move_downloads.service`:

```ini
[Unit]
Description=Move completed downloads to external drive
After=default.target

[Service]
Type=simple
ExecStart=/usr/bin/zsh -c 'source ~/.zshrc && python3 ~/.local/scripts/move_downloads.py'
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
```

### 3. Enable and start the service

```bash
systemctl --user daemon-reload
systemctl --user enable --now move_downloads.service
```

### 4. (Optional) Keep the service running after logout

```bash
loginctl enable-linger $USER
```

---

## 🛠️ Management Commands

| Action       | Command                                     |
|--------------|---------------------------------------------|
| Start        | `systemctl --user start move_downloads`     |
| Stop         | `systemctl --user stop move_downloads`      |
| View status  | `systemctl --user status move_downloads`    |
| View logs    | `journalctl --user -u move_downloads -f`    |

---

## ✅ Notes

- The script uses Zsh to load environment variables from `.zshrc`. If you use a different shell, adjust the `ExecStart` line in the service file accordingly.
- The script ignores files that are actively being written and retries them in the next cycle.

---

## 📄 License

MIT