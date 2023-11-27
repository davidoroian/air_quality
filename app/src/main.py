import os
from send_email import send_email
from meersens_api import get_api_response
from dotenv import load_dotenv

# loading environment variables
load_dotenv()
api_key = os.getenv('MEERSENS_API_KEY')


get_api_response(api_key)

