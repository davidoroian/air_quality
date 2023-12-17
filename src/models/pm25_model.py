from src.database.database import get_conn
import pyodbc

def get_pm25_entries():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pm25")

        for row in cursor.fetchall():
            print(row.id, row.entry_id, row.qualification, row.description, row.value)
            rows.append(f"{row.id}, {row.entry_id}, {row.qualification}, {row.description}, {row.value}")
        return rows

def get_pm25_by_entry_id(id):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pm25 WHERE entry_id = ?", id)

        row = cursor.fetchone()
        return row
    
def create_pm25_entry(entry_id, qualification, description, value):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO pm25 (entry_id, qualification, description, value) VALUES (?, ?, ?, ?)", entry_id, qualification, description, value)
        conn.commit()