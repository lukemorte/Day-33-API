import requests
from datetime import datetime

MY_LAT = 49.414165 # Your latitude
MY_LONG = 14.658742 # Your longitude
MARGIN_TOLERANCE = 5 # tolerance


def is_dark(hour_sunrise, hour_sunset, hour_now):
    if hour_now > hour_sunset or hour_now < hour_sunrise:
        return True
    else:
        return False


def is_ISS_close_to_me(iss_lat, iss_lng):
    if (
        iss_lat > MY_LAT - MARGIN_TOLERANCE
        and iss_lat < MY_LAT + MARGIN_TOLERANCE
        and iss_lng > MY_LONG - MARGIN_TOLERANCE
        and iss_lng < MY_LONG + MARGIN_TOLERANCE
    ):
        return True
    else:
        return False


# code


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
    "tzid": "Europe/Prague",
}


response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


time_now_hour = int(str(time_now).split(" ")[1].split(":")[0])

if (
    is_dark(sunrise, sunset, time_now_hour)
    and is_ISS_close_to_me(iss_latitude, iss_longitude)
):
    pass
