
import pandas as pd
import mysql.connector
from pathlib import Path
from getpass import getpass

# Locate cleaned CSV file
project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "dataset" / "it_support_tickets_cleaned.csv"

df = pd.read_csv(file_path)

# Convert date columns
df["Created_Date"] = pd.to_datetime(df["Created_Date"])
df["Resolved_Date"] = pd.to_datetime(df["Resolved_Date"], errors="coerce")

# Connect to MySQL
password = getpass("Enter your MySQL root password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="it_service_desk"
)

cursor = connection.cursor()

columns = [
    "Ticket_ID", "Created_Date", "Resolved_Date",
    "Department", "Issue_Type", "Priority", "Status",
    "Assigned_Team", "Assigned_Agent",
    "Resolution_Hours", "SLA_Hours", "SLA_Status"
]

# Convert missing values to None
rows = []
for row in df[columns].itertuples(index=False, name=None):
    clean_row = tuple(
        None if pd.isna(value)
        else value.to_pydatetime() if isinstance(value, pd.Timestamp)
        else value
        for value in row
    )
    rows.append(clean_row)

placeholders = ", ".join(["%s"] * len(columns))
column_names = ", ".join(columns)

query = f"""
INSERT INTO tickets ({column_names})
VALUES ({placeholders})
"""

cursor.executemany(query, rows)
connection.commit()

print("Data imported successfully!")
print("Total records imported:", cursor.rowcount)

cursor.close()
connection.close()
