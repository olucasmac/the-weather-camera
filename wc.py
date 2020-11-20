#! /usr/bin/python3 -u
# -*- coding: utf-8 -*-

import requests
import datetime
import json
import sys
import base64
from requests.exceptions import HTTPError
from PIL import Image, ImageFont, ImageDraw, ImageOps
from picamera import PiCamera
from time import sleep

###################
## Capture photo ##
###################

camera = PiCamera()
camera.resolution = (1080, 720)
sleep(5)
camera.capture('/tmp/picture.jpg')

try:

    ############################################################
    ## Get weather information from the OpenWatherMap.org API ##
    ############################################################

    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Belo Horizonte,br&APPID=YOUR-OWM-APP-ID')
    response.raise_for_status()
    jsonResponse = json.loads(response.text)

    ################################################
    ## Draws the weather information on the image ##
    ################################################

    now = datetime.datetime.now()
    city_name = "{}".format(jsonResponse['name'])
    date = "Date: " + now.strftime("%B,%d - %Y | %Hh%M")
    summary = "Summary: {}".format(jsonResponse['weather'][0]['main'])
    temperature = "Temperature: {:.1f}".format(jsonResponse['main']['temp']-273.15)+chr(176)+"C"
    pressure = "Pressure: {}".format(jsonResponse['main']['pressure'])+" mb"
    humidity = "Humidity: {}".format(jsonResponse['main']['humidity'])+"%"

    font_title = ImageFont.truetype("Impact", 55)
    font = ImageFont.truetype("FreeSans", 24)
    img = Image.open('/tmp/picture.jpg')

    draw = ImageDraw.Draw(img)

    draw.text((50, 40), city_name, (255,255,255), font=font_title, stroke_width=2, stroke_fill="#000")
    draw.text((50, 130), date, (255,255,255), font=font, stroke_width=2, stroke_fill="#000")
    draw.text((50, 170), summary, (255,255,255), font=font, stroke_width=2, stroke_fill="#000")
    draw.text((50, 210), temperature, (255,255,255), font=font, stroke_width=2, stroke_fill="#000")
    draw.text((50, 250), pressure, (255,255,255), font=font, stroke_width=2, stroke_fill="#000")
    draw.text((50, 290), humidity, (255,255,255), font=font, stroke_width=2, stroke_fill="#000")

    img.save('/tmp/picture.jpg')

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

#########################
## Send Image to ImGur ##
#########################

with open("/tmp/picture.jpg", "rb") as img_file:
    photo = base64.b64encode(img_file.read())

url = "https://api.imgur.com/3/image"
payload = {'image': photo,
        'name': 'YOUR-IMAGE-NAME',
        'title': 'YOUR-ALBUM-NAME',
        'album': 'YOUR-ALBUM-ID'
        }
files = [ ]
headers = {'Authorization': 'Bearer YOUR-IMGUR-API-KEY'}
response = requests.request("POST", url, headers=headers, data = payload)
