import requests
import datetime
import sys
import os
from json2xml import json2xml
from utils import write_to_file
from dotenv import load_dotenv

load_dotenv()

def get_wanted_pollutants(response, result):
    for item in response['values']:
            hour_report = {}
            hour_report['pollutants'] = {}

            hour_report['datetime'] = item['datetime']
            hour_report['pollutants']['co'] = item['pollutants']['co']
            hour_report['pollutants']['pm10'] = item['pollutants']['pm10']
            hour_report['pollutants']['pm25'] = item['pollutants']['pm25']

            result.append(hour_report)



def get_api_response(api_key):
    lat = os.getenv('LAT')
    long = os.getenv('LONG')

    from_date = datetime.datetime.today() - datetime.timedelta(days=10)
    to_date = datetime.datetime.today()
    hours = to_date.hour
    to_date_modif = to_date.replace(hour=hours-3, minute=0)

    url = f'https://api.meersens.com/environment/public/air/history?lat={lat}&lng={long}&index_type=meersens&from={from_date}&to={to_date_modif}&page=0'
    payload = {"accept": "application/json",
            "apikey": api_key}
    response = requests.get(url, params=payload)

    if response.status_code == 200:
        response_json = response.json()
        page_number = response_json['page']['totalPages'] # get no. of pages for the API query
        wanted_values = []  # list of items from API
        get_wanted_pollutants(response_json, wanted_values)

        # looping through all of the found API pages
        for i in range(1, page_number):
            url = f'https://api.meersens.com/environment/public/air/history?lat={lat}&lng={long}&index_type=meersens&from={from_date}&to={to_date_modif}&page={i}'
            response = requests.get(url, params=payload)

            if response.status_code == 200:
                response_json = response.json()
                get_wanted_pollutants(response_json, wanted_values)
            else:
                sys.exit(f"Failed to fetch data from the API on page {i}")

        response_xml = json2xml.Json2xml(wanted_values).to_xml()
        write_to_file(os.getenv('FILENAME'), response_xml)
    else:
        sys.exit("Failed to fetch data from the API")
