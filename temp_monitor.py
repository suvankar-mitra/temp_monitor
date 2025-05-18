import requests
import subprocess
import time
import logging
import os
import socket
import re

hostname = socket.gethostname()

# Telegram setup
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("API keys not found! Make sure they're set in the environment.")

import os

# Get the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
logs_directory = os.path.join(script_directory, "logs")

# Create logs directory if it doesn't exist
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

HIGH_TEMP_THRESHOLD = 80  # Celsius

# Set up logging
LOG_FILE = os.path.join(logs_directory, "temp_monitor.log")

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Temperature monitoring started.")

# Function to check system temperatures
def get_temperatures():
    result = subprocess.run(["sensors"], capture_output=True, text=True)
    temps = {}

    for line in result.stdout.splitlines():
        # Match lines like:
        # Core 0:        +74.0°C
        # Package id 0:  +74.0°C
        # Composite:     +40.9°C
        match = re.match(r'^\s*(Core \d+|Package id \d+|Composite|temp\d+|Sensor \d+):\s+\+?([0-9.]+)°C', line)
        if match:
            label = match.group(1)
            temperature = float(match.group(2))
            temps[label] = temperature

    return temps

# Function to send an alert
def send_alert(component, temp):
    message = f"[{hostname}] 🔥 Warning! Temperature High: {temp}°C exceeded safe temperature {HIGH_TEMP_THRESHOLD}°C"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)
    
    # Log alert
    logging.warning(f"ALERT: {component} exceeded safe temperature {HIGH_TEMP_THRESHOLD}°C, Current: {temp}°C")

# Function to send periodic info message
def send_info(temp):
    message = f"[{hostname}] 🧊 Info: Current temperature : {temp}°C"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)
    
    # Log info message
    logging.info(f"INFO: Current temperature update sent - {temp}°C")

# Monitoring loop
last_info_time = time.time()  # Track last info message time

while True:
    temperatures = get_temperatures()
    current_time = time.time()
    
    for component, temp in temperatures.items():
        logging.info(f"{component} Temperature: {temp}°C")  # Log regular readings        
        # Send alert if temperature exceeds 80°C
        if temp > HIGH_TEMP_THRESHOLD:
            send_alert(component, temp)

    # Send info update once per hour
    if current_time - last_info_time >= 3600:
        # send max temp
        max_temp = max(temperatures.values())
        send_info(max_temp)
        last_info_time = current_time

    time.sleep(60)  # Check every 60 seconds
