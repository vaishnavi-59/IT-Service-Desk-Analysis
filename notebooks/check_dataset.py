
import pandas as pd
from pathlib import Path

# Get the project folder location
project_folder = Path(__file__).resolve().parent.parent

# Build the dataset file path
file_path = project_folder / "dataset" / "it_support_tickets.csv"

# Load CSV into a DataFrame
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print(df.head())

print("\n--- DATASET DIMENSIONS ---")

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])
print("Total records:", len(df))

print("\n--- COLUMN NAMES ---")

print(df.columns.tolist())
print("\n--- DATA TYPES ---")

print(df.dtypes)
print("\n--- MISSING VALUES ---")

print(df.isnull().sum())
print("\n--- DUPLICATE RECORDS ---")

print("Total duplicate rows:", df.duplicated().sum())

print("Duplicate Ticket IDs:", df["Ticket_ID"].duplicated().sum())
print("\n--- MISSING VALUES ---")

print(df.isnull().sum())
print("\n--- DUPLICATE RECORDS ---")

print("Total duplicate rows:", df.duplicated().sum())

print("Duplicate Ticket IDs:", df["Ticket_ID"].duplicated().sum())
print("\n--- STATISTICAL SUMMARY ---")

print(df.describe())
print("\n--- TICKET STATUS ---")

print(df["Status"].value_counts())

print("\n--- PRIORITY DISTRIBUTION ---")

print(df["Priority"].value_counts())

print("\n--- ISSUE TYPE DISTRIBUTION ---")

print(df["Issue_Type"].value_counts())

print("\n--- DEPARTMENT DISTRIBUTION ---")

print(df["Department"].value_counts())
print("\n--- FIRST 5 RECORDS ---")

print(df.head())

print("\n--- LAST 5 RECORDS ---")

print(df.tail())