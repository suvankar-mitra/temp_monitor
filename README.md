
# Temp Monitor Service

This project runs a Python script, `temp_monitor.py`, as a **systemd** service to monitor system temperature and send alerts via Telegram when the temperature exceeds a specified threshold.

## Script Description

### `temp_monitor.py` Overview:
- Continuously monitors system temperature using `sensors`.
- Sends Telegram alerts if the temperature exceeds **80°C**.
- Logs regular temperature readings in a log file.
- Sends periodic updates every **hour** via Telegram.
- Requires **Telegram Bot API key** and **user ID** for notifications.

## Prerequisites

- Linux system with **systemd** support.
- Python installed (`python3 --version` to check).
- Your script (`temp_monitor.py`) located at `/path/to/temp_monitor.py`.
- `lm-sensors` installed (`sudo apt install lm-sensors` or `sudo yum install lm_sensors`).
- A Telegram bot with an API key.
- Your Telegram user ID to receive alerts.

## Setup Instructions

### 1. Create the systemd service file
Run the following command to create the service file:
```sh
sudo nano /etc/systemd/system/temp_monitor.service
```

### 2. Define the service
Add the following content to `temp_monitor.service`:

```ini
[Unit]
Description=Temperature Monitoring Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/temp_monitor.py
Restart=always
User=your_username
WorkingDirectory=/path/to
Environment="TELEGRAM_BOT_TOKEN=your_bot_api_key"
Environment="TELEGRAM_CHAT_ID=your_chat_id"
StandardOutput=append:/var/log/temp_monitor.log
StandardError=append:/var/log/temp_monitor.err

[Install]
WantedBy=multi-user.target
```

- Replace `/path/to/temp_monitor.py` with the actual script path.
- Ensure Python is installed at `/usr/bin/python3`.
- Add your **Telegram Bot API key** and **chat ID** in the environment variables.

### 3. Reload systemd
Apply changes using:
```sh
sudo systemctl daemon-reload
```

### 4. Enable service (start on boot)
```sh
sudo systemctl enable temp_monitor.service
```

### 5. Start the service
```sh
sudo systemctl start temp_monitor.service
```

### 6. Check status
To verify if the service is running:
```sh
sudo systemctl status temp_monitor.service
```

### 7. Stop or restart the service
If needed, stop or restart the service using:
```sh
sudo systemctl stop temp_monitor.service
sudo systemctl restart temp_monitor.service
```

### Troubleshooting
If the script isn't working as expected:
- Check logs:
  ```sh
  journalctl -u temp_monitor.service --no-pager --lines=50
  ```
- Ensure the script has executable permissions:
  ```sh
  chmod +x /path/to/temp_monitor.py
  ```
- Verify systemd unit syntax:
  ```sh
  systemctl daemon-reexec
  ```
- Make sure `lm-sensors` is installed and configured:
  ```sh
  sudo sensors-detect
  ```

### Additional Configuration
- Adjust the **temperature threshold** inside `temp_monitor.py` as per your system requirements.
- If using a virtual environment, modify `ExecStart`:
  ```sh
  ExecStart=/bin/bash -c 'source /path/to/venv/bin/activate && python /path/to/temp_monitor.py'
  ```
- Modify Telegram settings inside the script if needed.

## Conclusion
Now your **temperature monitoring script** will run as a **systemd service**, ensuring continuous execution and automatic restart.

🚀 Stay cool, and happy monitoring!
