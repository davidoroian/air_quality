from src.database.database import get_conn
import pyodbc

def get_pm10_entries():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pm10")

        for row in cursor.fetchall():
            print(row.id, row.entry_id, row.qualification, row.description, row.value)
            rows.append(f"{row.id}, {row.entry_id}, {row.qualification}, {row.description}, {row.value}")
        return rows

def get_pm10_by_entry_id(id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pm10 WHERE entry_id = ?", id)

        row = cursor.fetchone()
        return row
    
def create_pm10_entry(entry_id, qualification, description, value):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO pm10 (entry_id, qualification, description, value) VALUES (?, ?, ?, ?)", entry_id, qualification, description, value)
        conn.commit()