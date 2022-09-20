import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com"

nutritionix_header = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0"  # developer mode
}

user_exercise = input("Tell me which exercises you did?: ")
content = {
    "query": user_exercise,
    "gender": "male",
    "weight_kg": "90",
    "height_cm": "171",
    "age": "22"
}

exercise_response = requests.post(url=f"{NUTRITIONIX_ENDPOINT}/v2/natural/exercise",
                                  headers=nutritionix_header,
                                  json=content)
exercise_data = exercise_response.json()["exercises"]

# send the info retrieved to google sheet
SHEETY_ENDPOINT = "https://api.sheety.co/6ac448a1b35998883d74352e2b1723df/myWorkouts/workouts"
SHEETY_KEY = os.environ.get("SHEETY_KEY")

SHEETY_HEADER = {
    "Authorization": SHEETY_KEY
}

# get all content inside the google sheet
"""sheety_response = requests.get(url=SHEETY_ENDPOINT, headers=SHEETY_HEADER)
print(sheety_response.text)"""

today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%X")

for workout in exercise_data:
    sheety_content = {
        "workout": {  # put all the data inside the sheet name (aka: the last part of the url endPoint with no "s")
            "date": date,
            "time": time,
            "exercise": workout["name"].title(),
            "duration": workout["duration_min"],
            "calories": workout["nf_calories"]
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_content, headers=SHEETY_HEADER)
    print(sheety_response.text)
