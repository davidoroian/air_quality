import sys
import os
import requests
import datetime
from json2xml import json2xml
from dotenv import load_dotenv
from src.utils.utils import write_to_file
from src.models.entry_model import get_entries, get_entry, create_entry
from src.models.co_model import get_co_by_entry_id, get_co_entries, create_co_entry
from src.models.pm10_model import get_pm10_by_entry_id, get_pm10_entries, create_pm10_entry
from src.models.pm25_model import get_pm25_by_entry_id, get_pm25_entries, create_pm25_entry

load_dotenv()

def get_wanted_pollutants(response, result):
    for item in response['values']:
            hour_report = {}
            hour_report['pollutants'] = {}

            hour_report['datetime'] = datetime.datetime.strptime(item['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            hour_report['pollutants']['co'] = item['pollutants']['co']
            hour_report['pollutants']['pm10'] = item['pollutants']['pm10']
            hour_report['pollutants']['pm25'] = item['pollutants']['pm25']

            result.append(hour_report)

def insert_pollutants_into_database(entries):
    existing_entries=get_entries()
    if existing_entries:
        for entry in entries:
            if entry['datetime'] > existing_entries[-1].recording_date or entry['datetime'] < existing_entries[0].recording_date:
                create_entry(entry['datetime'])
                entry_id = get_entry(entry['datetime']).id
                create_pm10_entry(entry_id=entry_id, qualification=entry['pollutants']['pm10']['index']['qualification'], description=entry['pollutants']['pm10']['index']['description'], value=entry['pollutants']['pm10']['index']['value'])
                create_pm25_entry(entry_id=entry_id, qualification=entry['pollutants']['pm25']['index']['qualification'], description=entry['pollutants']['pm25']['index']['description'], value=entry['pollutants']['pm25']['index']['value'])
                create_co_entry(entry_id=entry_id, qualification=entry['pollutants']['co']['index']['qualification'], description=entry['pollutants']['co']['index']['description'], value=entry['pollutants']['co']['index']['value'])
    else:
        for entry in entries:
            create_entry(entry['datetime'])
            entry_id = get_entry(entry['datetime']).id
            create_pm10_entry(entry_id=entry_id, qualification=entry['pollutants']['pm10']['index']['qualification'], description=entry['pollutants']['pm10']['index']['description'], value=entry['pollutants']['pm10']['index']['value'])
            create_pm25_entry(entry_id=entry_id, qualification=entry['pollutants']['pm25']['index']['qualification'], description=entry['pollutants']['pm25']['index']['description'], value=entry['pollutants']['pm25']['index']['value'])
            create_co_entry(entry_id=entry_id, qualification=entry['pollutants']['co']['index']['qualification'], description=entry['pollutants']['co']['index']['description'], value=entry['pollutants']['co']['index']['value'])

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

        # looping through all of the found API pages
        for i in range(1, page_number):
            url = f'https://api.meersens.com/environment/public/air/history?lat={lat}&lng={long}&index_type=meersens&from={from_date}&to={to_date_modif}&page={i}'
            response = requests.get(url, params=payload)

            if response.status_code == 200:
                response_json = response.json()
                get_wanted_pollutants(response_json, wanted_values)
            else:
                sys.exit(f"Failed to fetch data from the API on page {i}")

        insert_pollutants_into_database(wanted_values)
        response_xml = json2xml.Json2xml(wanted_values).to_xml()
        write_to_file(os.getenv('FILENAME'), response_xml)
    else:
        sys.exit("Failed to fetch data from the API")
