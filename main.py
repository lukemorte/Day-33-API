import requests
import smtplib
from email.message import EmailMessage
from datetime import datetime
import time

MY_LAT = 49.414165  # Your latitude
MY_LONG = 14.658742  # Your longitude
MARGIN_TOLERANCE = 5  # tolerance

SMTP = "smtp.seznam.cz"
EMAIL = "py_test@seznam.cz"
PASSWORD = "jjz!AtuDYiN#46@"

timer = None


def is_dark(hour_sunrise, hour_sunset, hour_now):
    if hour_now > hour_sunset or hour_now < hour_sunrise:
        return True
    else:
        return False


def is_ISS_over_head(iss_lat, iss_lng):
    if (
        MY_LAT - MARGIN_TOLERANCE <= iss_lat <= MY_LAT + MARGIN_TOLERANCE
        and MY_LONG - MARGIN_TOLERANCE <= iss_lng <= MY_LONG + MARGIN_TOLERANCE
    ):
        return True
    else:
        return False


def send_mail():
    with smtplib.SMTP(SMTP) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)

        msg = EmailMessage()
        msg.set_content("ISS is right over your head and it's dark. Just look out and watch :) Enjoy.")
        msg["Subject"] = "ISS right over your head"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        connection.send_message(msg)


def control_every_minute():
    print("1 minute run code.")
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

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
    time_now_hour = int(str(time_now).split(" ")[1].split(":")[0])

    if is_dark(sunrise, sunset, time_now_hour) and is_ISS_over_head(iss_latitude, iss_longitude):
        send_mail()


while True:
    control_every_minute()
    time.sleep(5)
