import json
import random
import string
import os
from datetime import datetime, timedelta
import shutil

DATA_FILE = 'data.json'
BACKUP_FILE = 'data_backup.json'

def backup_data():
    """Create a backup of the data file."""
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE)

def restore_from_backup():
    """Restore data from the backup file."""
    if os.path.exists(BACKUP_FILE):
        shutil.copy(BACKUP_FILE, DATA_FILE)

# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Error loading data. Restoring from backup.")
            restore_from_backup()
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    return {}

# Save data to JSON file
def save_data(data):
    backup_data()  # Backup data before saving
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_code(amount, duration):
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    expiration = calculate_expiration(duration)
    
    data = load_data()
    data[code] = {
        "discount": amount,
        "expiration": expiration.strftime("%Y-%m-%d %H:%M:%S"),
        "used": False
    }
    save_data(data)
    return code

def calculate_expiration(duration):
    now = datetime.now()
    expiration_time = now
    expiration_time += timedelta(days=duration['days'])
    expiration_time += timedelta(hours=duration['hours'])
    expiration_time += timedelta(minutes=duration['minutes'])
    expiration_time += timedelta(seconds=duration['seconds'])
    
    if duration['months'] > 0:
        for _ in range(duration['months']):
            if expiration_time.month == 12:
                expiration_time = expiration_time.replace(year=expiration_time.year + 1, month=1)
            else:
                expiration_time = expiration_time.replace(month=expiration_time.month + 1)
    
    return expiration_time

def verify_code(code):
    data = load_data()
    if code in data:
        return data[code]
    return None

def mark_code_as_used(code):
    data = load_data()
    if code in data and not data[code]["used"]:
        data[code]["used"] = True
        save_data(data)
        return True
    return False
