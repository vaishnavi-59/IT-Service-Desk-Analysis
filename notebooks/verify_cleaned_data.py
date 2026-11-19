import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

file_path = (
    project_folder / "dataset" / "it_support_tickets_cleaned.csv"
)

df = pd.read_csv(file_path)

print("CLEANED DATASET VERIFICATION")

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

print("\nSLA status:")
print(df["SLA_Status"].value_counts())

print("\nFirst 5 records:")
print(df.head())