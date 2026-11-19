
import pandas as pd
import numpy as np
from pathlib import Path

# Locate project folder
project_folder = Path(__file__).resolve().parent.parent

# Load original dataset
input_file = project_folder / "dataset" / "it_support_tickets.csv"

df = pd.read_csv(input_file)

print("Original dataset loaded successfully!")
print("Original shape:", df.shape)
print("\n--- MISSING VALUES BEFORE CLEANING ---")

print(df.isnull().sum())

print("\nTotal missing values:")
print(df.isnull().sum().sum())
print("\n--- DUPLICATE CHECK ---")

print("Duplicate rows:", df.duplicated().sum())

print("Duplicate Ticket IDs:", df["Ticket_ID"].duplicated().sum())

# Remove exact duplicate rows
df = df.drop_duplicates()

# Keep only the first occurrence of each Ticket_ID
df = df.drop_duplicates(subset="Ticket_ID", keep="first")

print("\nDuplicates removed successfully!")
print("Current shape:", df.shape)
print("\n--- CONVERTING DATE COLUMNS ---")

df["Created_Date"] = pd.to_datetime(
    df["Created_Date"],
    errors="coerce"
)

df["Resolved_Date"] = pd.to_datetime(
    df["Resolved_Date"],
    errors="coerce"
)

print(df[["Created_Date", "Resolved_Date"]].dtypes)
print("\n--- CLEANING TEXT COLUMNS ---")

text_columns = [
    "Ticket_ID",
    "Department",
    "Issue_Type",
    "Priority",
    "Status",
    "Assigned_Team",
    "Assigned_Agent"
]

for column in text_columns:

    df[column] = df[column].astype("string").str.strip()

print("Text columns cleaned successfully!")
print("\n--- VALIDATING TICKET DATA ---")

# Check missing ticket IDs
print("Missing Ticket IDs:", df["Ticket_ID"].isnull().sum())

# Check missing creation dates
print("Missing Created Dates:", df["Created_Date"].isnull().sum())

# Check invalid priorities
valid_priorities = ["Critical", "High", "Medium", "Low"]

print(
    "Invalid priorities:",
    (~df["Priority"].isin(valid_priorities)).sum()
)

# Check invalid statuses
valid_statuses = ["Resolved", "In Progress", "Open"]

print(
    "Invalid statuses:",
    (~df["Status"].isin(valid_statuses)).sum()
)

# Check resolved tickets without resolution hours
resolved_without_hours = (
    (df["Status"] == "Resolved") &
    (df["Resolution_Hours"].isnull())
)

print(
    "Resolved tickets without resolution hours:",
    resolved_without_hours.sum()
)

# Check pending tickets with resolution hours
pending_with_hours = (
    (df["Status"] != "Resolved") &
    (df["Resolution_Hours"].notnull())
)

print(
    "Pending tickets with resolution hours:",
    pending_with_hours.sum()
)
print("\n--- SLA PERFORMANCE ---")

# Create a new SLA status column
df["SLA_Status"] = np.where(
    df["Status"] != "Resolved",
    "Pending",
    np.where(
        df["Resolution_Hours"] <= df["SLA_Hours"],
        "Within SLA",
        "SLA Breached"
    )
)

print(df["SLA_Status"].value_counts())
print("\n--- RESOLUTION TIME VALIDATION ---")

resolved_mask = df["Status"] == "Resolved"

calculated_hours = (
    df.loc[resolved_mask, "Resolved_Date"] -
    df.loc[resolved_mask, "Created_Date"]
).dt.total_seconds() / 3600

time_difference = (
    calculated_hours - df.loc[resolved_mask, "Resolution_Hours"]
).abs()

print(
    "Records with mismatched resolution time:",
    (time_difference > 0.02).sum()
)
print("\n--- EXPORTING CLEANED DATASET ---")

output_file = (
    project_folder / "dataset" / "it_support_tickets_cleaned.csv"
)

df.to_csv(
    output_file,
    index=False,
    date_format="%Y-%m-%d %H:%M:%S"
)

print("Cleaned dataset saved successfully!")
print("File location:", output_file)

print("\nFinal dataset shape:", df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nFinal SLA distribution:")
print(df["SLA_Status"].value_counts())
