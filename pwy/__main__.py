#!/usr/bin/env python3
#
# pwy
# Copyright (C) 2021, Clint <https://github.com/clieg>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import requests
import argparse
import datetime
import sys

from pwy.key import KEY
from pwy.colours import BWHITE, GREEN, RESET
from pwy.ascii import *
from pwy.translation import LANGUAGES, TRANSLATIONS


def get_weather_info(city, unit, lang):
    # Get the data from the API.
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units={unit}&lang={lang}'
    
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.HTTPError:
        status = req.status_code
        
        if status == 401:
            print(f'Invalid API key.')
        elif status == 404:
            print(f'Invalid input. See pwy -h for more information.')
        elif status in (429, 443):
            print(f'API calls per minute exceeded.')

        sys.exit(1)

    data = req.json()
    weather_info = {
        'name': data['name'],
        'country': data['sys']['country'],
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'main': data['weather'][0]['main'],
        'description': data['weather'][0]['description'].title(),
        'pressure': data['main']['pressure'],
        'humidity': data['main']['humidity'],
        'speed': data['wind']['speed'],
        'timezone': data['timezone'],
        'unit': unit,
        'lang': lang
    }
    
    return weather_info


def get_ascii(info):
    # Find the language. If the language is present, get the key of TRANSLATION
    # dictionary that matches the language and return the designated list
    # containing the weather ASCII art of the conditions are met.
    
    weather = info['main']
    lang = info['lang']
    
    if lang in LANGUAGES:
            language = TRANSLATIONS.get(lang)
    else:
        return unknown
            
            if weather == language[0]:
                return clear_sky
            
    elif weather in (language[1], language[2]):
                return overcast_cloud
                
    elif weather in (language[3], language[4]):
                return few_clouds
                
    elif weather in (language[5], language[6], language[7]):
                return rain
                
            elif weather == language[8]:
                return thunderstorm
                
            elif weather == language[9]:
                return snow
                
            elif weather == language[10]:
                return mist
                
            else:
                return unknown


def get_units(info):
    # If info['unit'] is equal to 'metric', return the first first and second index.
    # Otherwise, return the second and third index.

    units = ['°C', 'm/s', '°F', 'mph', 'K']
    
    if info['unit'] == 'metric':
        return (units[0], units[1])
    elif info['unit'] == 'imperial':
        return (units[2], units[3])
    else:
        return (units[4], units[1])


def get_localtime(info):
    # Get the local time and timezone.

    timezone = datetime.timezone(datetime.timedelta(seconds = (info['timezone'])))
    return datetime.datetime.now(tz = timezone).strftime('%H:%M %Z')


def display_weather_info(info):
    # Invoke the get_ascii() function and print it by index.
    # Invoke the get_units() function and print the temperature's measurement.
    # Invoke the get_localtime function and print the local time.

    ascii = get_ascii(info)
    units = get_units(info)
    time = get_localtime(info)
    
    # Print the weather information.
    print(f'\t{ascii[0]}  {BWHITE}{info["name"]}, {info["country"]}{RESET}')
    print(f'\t{ascii[1]}  Temperature: {GREEN}{info["temp"]}{RESET}'
          f' ({info["feels_like"]}) {units[0]}')
    print(f'\t{ascii[2]}  {info["main"]}. {info["description"]}')
    print(f'\t{ascii[3]}  Pressure: {GREEN}{info["pressure"]}{RESET}hPa'
          f'  Humidity: {GREEN}{info["humidity"]}{RESET}%'
          f'  Wind: {GREEN}{info["speed"]}{RESET}{units[1]}')
    print(f'\t{ascii[4]}  Time: {GREEN}{time}{RESET}')


def main():
    # Get arguments.
    # Metric system is used by default. If unit is empty, use Metric system.
    # Otherwise use Imperial system.
    
    parser = argparse.ArgumentParser(
        description = 'pwy - A simple weather tool.')
    
    parser.add_argument('city', nargs='+', help='Input city name')
    parser.add_argument('--unit', dest = 'unit', metavar='', help='Input unit name')
    parser.add_argument('--lang', dest = 'language', metavar='', help='Input language')
    
    args = parser.parse_args()
    
    city = ' '.join(args.city)
    unit = args.unit
    lang = args.language
    
    if unit is None:
        unit = 'metric'
    if lang is None:
        lang = 'en'
    
    info = get_weather_info(city, unit, lang)
    display_weather_info(info)


if __name__ == '__main__':
    main()