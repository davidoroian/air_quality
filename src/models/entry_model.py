from src.database.database import get_conn
import pyodbc

def get_entries():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries ORDER BY recording_date ASC")

        for row in cursor.fetchall():
            rows.append(row)
        return rows

def get_entry(date):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries WHERE recording_date = ?", str(date))

        row = cursor.fetchone()
        return row
    
def create_entry(date):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (recording_date) VALUES (?)", date)
        conn.commit()