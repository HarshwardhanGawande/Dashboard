from requests import Session
from datetime import datetime as dt
import os
s= Session()
today = dt.today()
file_name = today.strftime("%m_%d_%Y")
access_token_file_name='fyres_access_token'+file_name+".txt"

access_file_path=r"C:\\Users\\SSD\Dropbox\\Git\market2022\\rocketplus\\token files\\access_token\\"+access_token_file_name
is_token_exists = os.path.exists(access_file_path)

def get_access_token():
    with open(access_file_path, 'r') as file:
        access_token = file.read().rstrip()
    return access_token
if is_token_exists:
    access_token = get_access_token()
else:
    login_otp='https://api-t2.fyers.in/vagator/v2/send_login_otp'
    verify_otp='https://api-t2.fyers.in/vagator/v2/verify_otp'
    verify_pin='https://api-t2.fyers.in/vagator/v2/verify_pin'
    login_otp_payload={"fy_id":"FH0441","app_id":"2"}
    s.headers.update(h)
    data1=s.post(url=login_otp,json=login_otp_payload)
    request_key2=data1.json()['request_key']
    print(request_key2)
    otp=input("Enter otp :")
    verify_otp_payload={'otp':otp,'request_key':request_key2}
    data2=s.post(url=verify_otp,json=verify_otp_payload)
    request_key3=data2.json()['request_key']
    verify_pin_payload={"request_key":request_key3,"identity_type":"pin","identifier":"1050"}
    data3=s.post(url=verify_pin,json=verify_pin_payload)
    access_token= data3.json()['data']['access_token']
    with open(access_file_path, 'w') as f:
        f.write(token)
s.headers.update({"Authorization":access_token})
print(access_token)