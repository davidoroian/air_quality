import os
import datetime
from src.email.send_email import send_email
from src.api.meersens_api import get_api_response
from src.models.entry_model import get_entries, get_entry
from dotenv import load_dotenv

# loading environment variables
load_dotenv()
api_key = os.getenv('MEERSENS_API_KEY')

# result = get_entries()
get_api_response(api_key)


