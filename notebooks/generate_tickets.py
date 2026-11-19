
import pandas as pd
import numpy as np
from pathlib import Path

# 1. Set random seed
np.random.seed(42)

# 2. Number of tickets
total_tickets = 3000

# 3. Define categories
departments = ["IT", "HR", "Finance", "Sales", "Marketing"]

issue_types = [
    "Network", "Software", "Hardware", "Login", "Email"
]

priorities = ["Critical", "High", "Medium", "Low"]

statuses = ["Resolved", "In Progress", "Open"]

# 4. Assign support teams
support_teams = {
    "Network": "Network Team",
    "Software": "Application Support",
    "Hardware": "Hardware Support",
    "Login": "Access Support",
    "Email": "Access Support"
}

# 5. Define SLA targets (illustrative project assumptions)
sla_mapping = {
    "Critical": 4,
    "High": 8,
    "Medium": 24,
    "Low": 48
}

# 6. Generate ticket IDs
ticket_ids = [
    f"TKT{1001 + i}" for i in range(total_tickets)
]

# 7. Generate ticket creation dates
created_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start="2026-01-01",
            end="2026-10-31",
            freq="h"
        ),
        size=total_tickets
    )
)

# 8. Generate ticket details
department_data = np.random.choice(
    departments, size=total_tickets
)

issue_data = np.random.choice(
    issue_types, size=total_tickets
)

priority_data = np.random.choice(
    priorities,
    size=total_tickets,
    p=[0.10, 0.25, 0.40, 0.25]
)

status_data = np.random.choice(
    statuses,
    size=total_tickets,
    p=[0.70, 0.18, 0.12]
)

# 9. Assign teams and agents
team_data = [
    support_teams[issue] for issue in issue_data
]

agent_pools = {
    "Network Team": ["Agent_01", "Agent_02", "Agent_03"],
    "Application Support": ["Agent_04", "Agent_05", "Agent_06"],
    "Hardware Support": ["Agent_07", "Agent_08", "Agent_09"],
    "Access Support": ["Agent_10", "Agent_11", "Agent_12"]
}

agent_data = [
    np.random.choice(agent_pools[team])
    for team in team_data
]

# 10. Assign SLA hours
sla_hours = [
    sla_mapping[priority] for priority in priority_data
]

# 11. Generate resolution details
resolution_hours = []
resolved_dates = []

for i in range(total_tickets):

    if status_data[i] == "Resolved":

        hours = round(
            np.random.uniform(0.5, sla_hours[i] * 1.8), 2
        )

        resolution_hours.append(hours)

        resolved_date = (
            created_dates[i] + pd.to_timedelta(hours, unit="h")
        )

        resolved_dates.append(resolved_date)

    else:
        resolution_hours.append(np.nan)
        resolved_dates.append(pd.NaT)

# 12. Create DataFrame
df = pd.DataFrame({
    "Ticket_ID": ticket_ids,
    "Created_Date": created_dates,
    "Resolved_Date": resolved_dates,
    "Department": department_data,
    "Issue_Type": issue_data,
    "Priority": priority_data,
    "Status": status_data,
    "Assigned_Team": team_data,
    "Assigned_Agent": agent_data,
    "Resolution_Hours": resolution_hours,
    "SLA_Hours": sla_hours
})

# 13. Sort records by creation date
df = df.sort_values(
    by="Created_Date"
).reset_index(drop=True)

# 14. Save CSV file in dataset folder
project_folder = Path(__file__).resolve().parent.parent

dataset_folder = project_folder / "dataset"

dataset_folder.mkdir(
    parents=True,
    exist_ok=True
)

output_file = dataset_folder / "it_support_tickets.csv"

df.to_csv(
    output_file,
    index=False,
    date_format="%Y-%m-%d %H:%M:%S"
)

# 15. Display results
print("\nDataset generated successfully!")

print("\nFirst 5 records:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nTicket status distribution:")
print(df["Status"].value_counts())

print("\nDataset saved at:")
print(output_file)
