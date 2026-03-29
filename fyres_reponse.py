{
    "s": "ok",
    "code": 1043,
    "message": "Success",
    "user_count": 1,
    "data": {
        "FH0441": {
            "s": "ok",
            "code": 1019,
            "message": "User exists",
            "client_name": "HARSHWARDHANMANOHARRAO",
            "nick_name": "HARSHWARDHANMANOHARRAO",
            "avatar_link": "",
            "pin_created": true,
            "totp_enabled": false,
            "biometric_enabled": false,
            "request_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiIyIiwiY2xpZW50X25hbWUiOiJIQVJTSFdBUkRIQU5NQU5PSEFSUkFPIiwiZXhwIjoxNzc0NjI0MjkyLCJmeV9pZCI6IkZIMDQ0MSIsImlhdCI6MTc3NDYyMzM5MiwibmJmIjoxNzc0NjIzMzkyLCJyZXF1ZXN0X2tleSI6InpVbDNCVkU4cGttazNDOXI2SUhVVWdNUGdwejhraGQ0bVJ2Vzl3UzgzRDJXRVlZejdHIiwic3ViIjoib3RwX2xvZ2luIn0.yGflEMJgMqwEb202qPn83XYQIHc7-otXCl4TekjSMdM"
        }
    }
}


verify otp
https://api-t2.fyers.in/vagator/v2/verify_otp
payload
otp
:
"388253"
request_key
:
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiIyIiwiY2xpZW50X25hbWUiOiJIQVJTSFdBUkRIQU5NQU5PSEFSUkFPIiwiZXhwIjoxNzc0NjI0MjkyLCJmeV9pZCI6IkZIMDQ0MSIsImlhdCI6MTc3NDYyMzM5MiwibmJmIjoxNzc0NjIzMzkyLCJyZXF1ZXN0X2tleSI6InpVbDNCVkU4cGttazNDOXI2SUhVVWdNUGdwejhraGQ0bVJ2Vzl3UzgzRDJXRVlZejdHIiwic3ViIjoib3RwX2xvZ2luIn0.yGflEMJgMqwEb202qPn83XYQIHc7-otXCl4TekjSMdM"
response
{
    "s": "ok",
    "code": 2,
    "request_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NzQ2MjM0NTIsImV4cCI6MTc3NDcwOTg1MiwibmJmIjoxNzc0NjIzNDUyLCJmeV9pZCI6IkZIMDQ0MSIsInJlcXVlc3Rfa2V5IjoibGx3dmV3NDAwNkJEUU9RN0x6SXg1SzNBZFFCdzNFdkRHNUxPdmQ0dkNBRU11QWNHTlAifQ.2YpNsCAj1M0J3iXFqhxVKZsKHQ_GcJTOHQB2nwGqNuM",
    "client_name": "Harshwardhanmanoharrao Gawande",
    "nick_name": "Harshwardhanmanoharrao",
    "pin_created": true,
    "message": "fy_id and OTP verified successfully"
}



verify pin

https://api-t2.fyers.in/vagator/v2/verify_pin_v2

payload
identifier
:
"MTA1MA=="
identity_type
:
"pin"
request_key
:
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NzQ2MjM0NTIsImV4cCI6MTc3NDcwOTg1MiwibmJmIjoxNzc0NjIzNDUyLCJmeV9pZCI6IkZIMDQ0MSIsInJlcXVlc3Rfa2V5IjoibGx3dmV3NDAwNkJEUU9RN0x6SXg1SzNBZFFCdzNFdkRHNUxPdmQ0dkNBRU11QWNHTlAifQ.2YpNsCAj1M0J3iXFqhxVKZsKHQ_GcJTOHQB2nwGqNuM"



while selecting any chart interval

resolution=  3 => 3min

url = Request URL
"https://api-t1.fyers.in/indus/history?symbol=NSE%3ANIFTY50-INDEX&resolution=3&from=1774343153&to=1774396375&token_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X3N0YXR1cyI6IiIsImFwcFR5cGUiOiIiLCJhdF9oYXNoIjoiZ0FBQUFBQnB4cHM2UlBNSzJpcnJHMmVKcWRyZXdVZnpGNDkweE9HczJhRUVlVDdZME9ZaHpXdmZpYUZIZlFqQmJYMlBzajRwVXRxbXVhcmg0WmNCc19BUzFwd2tuYXZEYzdtMV94dU12SmVXRkI0UkdmYVZaZWM9IiwiYXVkIjpbIng6MCIsIng6MSIsIng6MiIsImQ6MSJdLCJkZXZpY2VfaGFzaCI6ImdBQUFBQUJweHBzNjlmbW9EYlJFaS1LODlfcllJenFpUTFaTng1MHRtVkN6bTIxSV9JaWRRa19kTWJkVkkzX1dyTW03ZEEyUzBrSk41b2dGd0tleXp0cDJwZzZUR3RXdUdJTnNKVzJGMS0wdmtJdkJyVHBsQjBDekR2MmtfUUpFdG9iV2dWT3BWM1c3IiwiZGlzcGxheV9uYW1lIjoiSEFSU0hXQVJESEFOTUFOT0hBUlJBTyBHQVdBTkRFIiwiZXhwIjoxNzc0NjU5NjAwLCJmeV9pZCI6IkZIMDQ0MSIsImhzbV9rZXkiOiJmZmJhYTg3ZTZmNDIzYTMzNjViMzBhZDc1ZDRkOWRhZGFkODAyYTJhMTYzYjAwM2VjNzEyY2YxNSIsImlhdCI6MTc3NDYyMzU0NiwiaXNEZHBpRW5hYmxlZCI6Ik4iLCJpc010ZkVuYWJsZWQiOiJOIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3NDYyMzU0Niwib21zIjoiSzEiLCJwb2FfZmxhZyI6Ik4iLCJzdWIiOiJhY2Nlc3NfdG9rZW4ifQ.65kHE5JZHHLpZx1_w6Wekl2QFQIn4h6_a0lzImd3lL0&dataReq=1774623719&contFlag=0&countback=77&currencyCode=INR"


payload

symbol
NSE:NIFTY50-INDEX
resolution
3
from
1774343153
to
1774396375
token_id
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X3N0YXR1cyI6IiIsImFwcFR5cGUiOiIiLCJhdF9oYXNoIjoiZ0FBQUFBQnB4cHM2UlBNSzJpcnJHMmVKcWRyZXdVZnpGNDkweE9HczJhRUVlVDdZME9ZaHpXdmZpYUZIZlFqQmJYMlBzajRwVXRxbXVhcmg0WmNCc19BUzFwd2tuYXZEYzdtMV94dU12SmVXRkI0UkdmYVZaZWM9IiwiYXVkIjpbIng6MCIsIng6MSIsIng6MiIsImQ6MSJdLCJkZXZpY2VfaGFzaCI6ImdBQUFBQUJweHBzNjlmbW9EYlJFaS1LODlfcllJenFpUTFaTng1MHRtVkN6bTIxSV9JaWRRa19kTWJkVkkzX1dyTW03ZEEyUzBrSk41b2dGd0tleXp0cDJwZzZUR3RXdUdJTnNKVzJGMS0wdmtJdkJyVHBsQjBDekR2MmtfUUpFdG9iV2dWT3BWM1c3IiwiZGlzcGxheV9uYW1lIjoiSEFSU0hXQVJESEFOTUFOT0hBUlJBTyBHQVdBTkRFIiwiZXhwIjoxNzc0NjU5NjAwLCJmeV9pZCI6IkZIMDQ0MSIsImhzbV9rZXkiOiJmZmJhYTg3ZTZmNDIzYTMzNjViMzBhZDc1ZDRkOWRhZGFkODAyYTJhMTYzYjAwM2VjNzEyY2YxNSIsImlhdCI6MTc3NDYyMzU0NiwiaXNEZHBpRW5hYmxlZCI6Ik4iLCJpc010ZkVuYWJsZWQiOiJOIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3NDYyMzU0Niwib21zIjoiSzEiLCJwb2FfZmxhZyI6Ik4iLCJzdWIiOiJhY2Nlc3NfdG9rZW4ifQ.65kHE5JZHHLpZx1_w6Wekl2QFQIn4h6_a0lzImd3lL0
dataReq
1774623719
contFlag
0
countback
77
currencyCode
INR