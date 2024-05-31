import os
import requests
from datetime import datetime
import smtplib
import time

my_lat = 23.259933
my_long = 77.412613
my_email = os.getenv('smtp_username')
password = os.getenv('smtp_password')


def proximity():
    responses = requests.get('http://api.open-notify.org/iss-now.json')
    responses.raise_for_status()
    datas = responses.json()

    iss_lat = float(datas['iss_position']['latitude'])
    iss_lng = float(datas['iss_position']['longitude'])

    if my_lat+5 > iss_lat > my_lat-5 and my_long+5 > iss_lng > my_long-5:
        return True
    else:
        return False


def is_night():
    parameters = {
        'lat': my_lat,
        'lng': my_long,
        'formatted': 0,
        'tzid': 'Asia/Calcutta'
    }
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    # print(sunrise)

    now = datetime.now()

    if now.hour > sunset or now.hour <= sunrise:
        return True
    else:
        return False


while True:
    if proximity() & is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="alokjswl99@outlook.com",
                                msg="Subject:ISS Position Alert\n\nIss is visible if you look up now.")
    else:
        print("No luck")
        time.sleep(60)
