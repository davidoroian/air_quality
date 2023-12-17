import pyodbc
import os
from dotenv import load_dotenv

# loading secrets
load_dotenv()

server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('AZURE_USERNAME')
password = os.getenv('AZURE_PASSWORD')


def get_conn():
    conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    try:
        conn = pyodbc.connect(conn_str)
    except Exception as e:
        print(f"Error initializing the database: {str(e)}")
    return conn
    
