import requests

url = "https://api-t1.fyers.in/data/history"
token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X3N0YXR1cyI6IiIsImFwcFR5cGUiOiIiLCJhdF9oYXNoIjoiZ0FBQUFBQnB4cHM2UlBNSzJpcnJHMmVKcWRyZXdVZnpGNDkweE9HczJhRUVlVDdZME9ZaHpXdmZpYUZIZlFqQmJYMlBzajRwVXRxbXVhcmg0WmNCc19BUzFwd2tuYXZEYzdtMV94dU12SmVXRkI0UkdmYVZaZWM9IiwiYXVkIjpbIng6MCIsIng6MSIsIng6MiIsImQ6MSJdLCJkZXZpY2VfaGFzaCI6ImdBQUFBQUJweHBzNjlmbW9EYlJFaS1LODlfcllJenFpUTFaTng1MHRtVkN6bTIxSV9JaWRRa19kTWJkVkkzX1dyTW03ZEEyUzBrSk41b2dGd0tleXp0cDJwZzZUR3RXdUdJTnNKVzJGMS0wdmtJdkJyVHBsQjBDekR2MmtfUUpFdG9iV2dWT3BWM1c3IiwiZGlzcGxheV9uYW1lIjoiSEFSU0hXQVJESEFOTUFOT0hBUlJBTyBHQVdBTkRFIiwiZXhwIjoxNzc0NjU5NjAwLCJmeV9pZCI6IkZIMDQ0MSIsImhzbV9rZXkiOiJmZmJhYTg3ZTZmNDIzYTMzNjViMzBhZDc1ZDRkOWRhZGFkODAyYTJhMTYzYjAwM2VjNzEyY2YxNSIsImlhdCI6MTc3NDYyMzU0NiwiaXNEZHBpRW5hYmxlZCI6Ik4iLCJpc010ZkVuYWJsZWQiOiJOIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc3NDYyMzU0Niwib21zIjoiSzEiLCJwb2FfZmxhZyI6Ik4iLCJzdWIiOiJhY2Nlc3NfdG9rZW4ifQ.65kHE5JZHHLpZx1_w6Wekl2QFQIn4h6_a0lzImd3lL0"


params = {
    "symbol": "NSE:NIFTY50-INDEX",
    "resolution": "5",
    "from": 1773961362,
    "to": 1774624626,
    "token_id": token,
    "dataReq": 1774624565,
    "contFlag": 0,
    "countback": 329,
    "currencyCode": "INR"
}

headers = {
    "accept": "*/*",
    "authorization": token,
    "origin": "https://fyers.in",
    "referer": "https://fyers.in/",
    "user-agent": "Mozilla/5.0"
}

cookies = {
    "__cf_bm": "PUwPlC5aWmRM1i8YGE9adegGtJU.iiExB2zyNj0at8c-1774624453.233414-1.0.1.1-7r5NYTz9dqN90pWEytGlTa1K2RV0yjamnSS6z4Yr8crpTMSQWfyvIL5FdAFlnU4cucVu6MGOIXriRTsQACqyFdUjCe4LKsmVoiRdtcRsamXspBMQV0Og308J9a_BuK.t",
    "_cfuvid": "ihIAZWgkdYUNgVVnOW_40poZdlUVzFUHxG2_j2T0pW0-1774624987.927994-1.0.1.1-4JvMBCKGyoh9CXYrpL50z1IyDEhVG69djL1260H96HE"
}

response = requests.get(url, params=params, headers=headers)#, cookies=cookies)

print(response.status_code)
print(response.json())