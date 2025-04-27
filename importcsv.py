import csv
import requests

API_URL = "https://example.com/api/create_user"
ERROR_LOG_FILE = "error_log.txt"
REQUIRED_FIELDS = ["email"]  # You can add more required fields if needed

def log_error(message):
    """Log error messages to a file."""
    with open(ERROR_LOG_FILE, "a") as f:
        f.write(message + "\n")

def is_valid_user(row):
    """Check if required fields are present."""
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            return False
    return True

def create_user(user_data):
    """Send a POST request to create a user."""
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code != 201:
            log_error(f"Failed to create user {user_data.get('email')}: {response.text}")
    except Exception as e:
        log_error(f"Exception creating user {user_data.get('email')}: {str(e)}")

def create_users(file_path):
    """Main function to read users from CSV and create them."""
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not is_valid_user(row):
                log_error(f"Skipping user due to missing required fields: {row}")
                continue
            create_user(row)

if __name__ == "__main__":
    create_users("users.csv")
