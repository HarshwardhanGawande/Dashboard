import os
import requests
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.getenv("FYERS_ID")
PIN = os.getenv("FYERS_PIN")
ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")
MOBILE_NUMBER = os.getenv("FYERS_MOBILE")
APP_ID = "2"  # Assuming this is constant, if not, can also be moved to .env

s = requests.Session()

mobile_url = "https://api-t2.fyers.in/vagator/v2/get_user_id_v3"
verify_otp_url = "https://api-t2.fyers.in/vagator/v2/verify_otp"
verify_pin_url = "https://api-t2.fyers.in/vagator/v2/verify_pin_v2"


headers = {
    "Content-Type": "application/json"
}

from datetime import datetime

# Function to convert date string to Unix timestamp
def convert_to_timestamp(date_string):
    # Define the date format
    date_format = "%d-%m-%Y"  # day-month-year format

    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_string, date_format)

    # Convert the datetime object to a Unix timestamp
    timestamp = int(date_obj.timestamp())

    return timestamp


# ✅ Test token validity
def is_token_valid(token):
    test_url = "https://api-t1.fyers.in/api/v3/profile"
    h = {"Authorization": token}
    r = s.get(test_url, headers=h)
    print("Token test status:", r.status_code)
    return r.status_code == 200


# ✅ Save token to .env
def save_token_to_env(token):
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()
    else:
        lines = []

    # remove old token
    lines = [l for l in lines if not l.startswith("FYERS_ACCESS_TOKEN=")]
    lines.append(f"FYERS_ACCESS_TOKEN={token}\n")

    with open(".env", "w") as f:
        f.writelines(lines)


# ✅ Generate new token
def generate_new_token():
    # Step 1: Send OTP
    payload1 = {"fy_id": USER_ID, "app_id": "2"}
    r1 = s.post(login_otp_url, json=payload1, headers=headers)
    print(r1.json())
    exit()
    request_key = r1.json()["request_key"]

    # Step 2: Verify OTP
    otp = input("Enter OTP: ")
    payload2 = {"otp": otp, "request_key": request_key}
    r2 = s.post(verify_otp_url, json=payload2, headers=headers)
    request_key2 = r2.json()["request_key"]

    # Step 3: Verify PIN
    payload3 = {
        "request_key": request_key2,
        "identity_type": "pin",
        "identifier": PIN
    }
    r3 = s.post(verify_pin_url, json=payload3, headers=headers)

    token = r3.json()["data"]["access_token"]
    return token


# ✅ Main logic
if ACCESS_TOKEN and is_token_valid(ACCESS_TOKEN):
    print("Using existing token")
    access_token = ACCESS_TOKEN
else:
    print("Generating new token...")
    access_token = generate_new_token()
    save_token_to_env(access_token)

# ✅ Use token
s.headers.update({"Authorization": access_token})

print("Final Access Token:", access_token)