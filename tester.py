import requests
import json
from tzlocal import get_localzone

url = "http://localhost:8080/"
local_tz = str(get_localzone())
try:
    response = requests.get(url)
    if not response.status_code == 200:
        raise Exception()
    if not local_tz in response.text:
        raise Exception()
except:
    print("Test 1: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)
    
try:
    response = requests.get(url + "UTC")
    if not response.status_code == 200:
        raise Exception()
    if not "UTC" in response.text:
        raise Exception()
except:
    print("Test 2: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.get(url + "Europe/Moscow")
    if not response.status_code == 200:
        raise Exception()
    if not "Europe/Moscow" in response.text:
        raise Exception()
except:
    print("Test 3: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.get(url + "api")
    if not response.status_code == 400:
        raise Exception()
except:
    print("Test 4: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.get(url + "api/adss")
    if not response.status_code == 400:
        raise Exception()
except:
    print("Test 5: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.get(url + "api/adss")
    if not response.status_code == 400:
        raise Exception()
except:
    print("Test 6: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.get(url + "api/v1")
    if not response.status_code == 400:
        raise Exception()
except:
    print("Test 7: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.post(url + "api/v1/time")
    if not response.status_code == 200:
        raise Exception()
except:
    print("Test 8: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.post(url + "api/v1/time")
    if not response.status_code == 200:
        raise Exception()
    obj = json.loads(response.text)
    if not obj["tz"] == local_tz:
        raise Exception()
except:
    print("Test 9: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.post(url + "api/v1/time", data= json.dumps({"tz": "UTC"}))
    if not response.status_code == 200:
        raise Exception()
    obj = json.loads(response.text)
    if not obj["tz"] == "UTC":
        raise Exception()
except:
    print("Test 10: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)
try:
    response = requests.post(url + "api/v1/time", data= json.dumps({"tz": "Europe/Moscow"}))
    if not response.status_code == 200:
        raise Exception()
    obj = json.loads(response.text)
    if not obj["tz"] == "Europe/Moscow":
        raise Exception()
except:
    print("Test 11: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.post(url + "api/v1/time", data= json.dumps({"tz": "UFO"}))
    if not response.status_code == 400:
        raise Exception()
except:
    print("Test 12: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.post(url + "api/v1/date", data= json.dumps({"tz": "Europe/Moscow"}))
    if not response.status_code == 200:
        raise Exception()
    obj = json.loads(response.text)
    if not obj["tz"] == "Europe/Moscow":
        raise Exception()
except:
    print("Test 13: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    response = requests.post(url + "api/v1/datediff", data= json.dumps({
        "start": {
            "date": "3:30pm 2020-12-01"
        },
        "end": {
            "date": "12.20.2020 22:21:05",
            "tz": "UTC"
        }
    }))
    if not response.status_code == 200:
        raise Exception()
    obj = json.loads(response.text)
except:
    print("Test 14: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)

try:
    obj = {
        "begin": {
            "date": "12:30pm 2020-12-01",
            "timezone": local_tz
        },
        "end": {
            "date": "12.20.2021 22:21:05",
            "tz": "UTC"
        }
    }
    response = requests.post(url + "api/v1/datediff", data= json.dumps(obj))
    if not response.status_code == 400:
        raise Exception()
except:
    print("Test 15: ")
    print("Response status: " + str(response.status_code))
    print("Response body:" + response.text)