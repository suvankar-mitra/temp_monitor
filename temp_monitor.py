import requests
import subprocess
import time
import logging
import os
import socket

hostname = socket.gethostname()

# Telegram setup
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("API keys not found! Make sure they're set in the environment.")


home_directory = os.getenv("HOME")

HIGH_TEMP_THRESHOLD = 80  # Celsius

# Set up logging
LOG_FILE = f"{home_directory}/logs/temp_monitor.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to check system temperatures
def get_temperatures():
    result = subprocess.run(["sensors"], capture_output=True, text=True)
    temps = {}

    for line in result.stdout.split("\n"):
        if "Core" in line or "Package id" in line or "Composite" in line or "Sensor" in line:
            parts = line.split()
            try:
                temp = float(parts[1].replace("+", "").replace("°C", ""))
                component = " ".join(parts[:-1])
                temps[component] = temp
            except ValueError:
                continue

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
        
        # Send info update every 1 hour (3600 seconds)
        if current_time - last_info_time >= 3600:
            send_info(temp)
            last_info_time = current_time

    time.sleep(60)  # Check every 60 seconds