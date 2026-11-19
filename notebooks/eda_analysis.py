
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Locate project folder
project_folder = Path(__file__).resolve().parent.parent

# Load cleaned dataset
file_path = (
    project_folder / "dataset" / "it_support_tickets_cleaned.csv"
)

df = pd.read_csv(file_path)
# Create reports folder if it does not exist
reports_folder = project_folder / "reports"
reports_folder.mkdir(exist_ok=True)

# Convert date columns
df["Created_Date"] = pd.to_datetime(df["Created_Date"])
df["Resolved_Date"] = pd.to_datetime(df["Resolved_Date"])

print("Cleaned dataset loaded successfully!")

print("Dataset shape:", df.shape)

print(df.head())

print("\n--- QUESTION 1: TICKET STATUS ANALYSIS ---")

status_count = df["Status"].value_counts()
# Chart 1: Ticket Status Distribution

status_count.plot(
    kind="bar",
    title="IT Support Ticket Status Distribution"
)

plt.xlabel("Ticket Status")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


print(status_count)

print("\nStatus percentage:")

status_percentage = (
    df["Status"].value_counts(normalize=True) * 100
)

print(status_percentage.round(2))
# Export Ticket Status Report

status_report = pd.DataFrame({
    "Total_Tickets": status_count,
    "Percentage": status_percentage.round(2)
})

status_report.to_csv(
    reports_folder / "ticket_status_report.csv"
)

print("Ticket Status Report exported successfully!")
print("\n--- QUESTION 2: DEPARTMENT ANALYSIS ---")

department_count = (
    df["Department"]
    .value_counts()
)
print("\n--- QUESTION 2: DEPARTMENT ANALYSIS ---")

department_count = (
    df["Department"]
    .value_counts()
)

print(department_count)

# Export Department Analysis Report

department_report = pd.DataFrame({
    "Total_Tickets": department_count
})

department_report.to_csv(
    reports_folder / "department_analysis_report.csv"
)

print("Department Analysis Report exported successfully!")

print("\n--- QUESTION 3: ISSUE TYPE ANALYSIS ---")
# Chart 2: Department-wise Ticket Distribution

department_count.plot(
    kind="bar",
    title="Department-wise Ticket Distribution"
)

plt.xlabel("Department")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print(department_count)
print("\n--- QUESTION 3: ISSUE TYPE ANALYSIS ---")

issue_count = (
    df["Issue_Type"]
    .value_counts()
)

print(issue_count)
# Export Issue Type Analysis Report

issue_report = pd.DataFrame({
    "Total_Tickets": issue_count
})

issue_report.to_csv(
    reports_folder / "issue_type_analysis_report.csv"
)

print("Issue Type Analysis Report exported successfully!")
# Chart 3: Issue Type Distribution

issue_count.plot(
    kind="bar",
    title="IT Support Ticket Issue Type Distribution"
)

plt.xlabel("Issue Type")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
print("\n--- QUESTION 4: PRIORITY ANALYSIS ---")

priority_count = (
    df["Priority"]
    .value_counts()
)

print(priority_count)
# Export Priority Analysis Report

priority_report = pd.DataFrame({
    "Total_Tickets": priority_count
})

priority_report.to_csv(
    reports_folder / "priority_analysis_report.csv"
)

print("Priority Analysis Report exported successfully!")
# Chart 4: Priority Distribution

priority_count.plot(
    kind="bar",
    title="IT Support Ticket Priority Distribution"
)

plt.xlabel("Priority")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()
print("\n--- QUESTION 5: RESOLUTION TIME ANALYSIS ---")

resolved_df = df[df["Status"] == "Resolved"].copy()

average_resolution = (
    resolved_df["Resolution_Hours"].mean()
)

median_resolution = (
    resolved_df["Resolution_Hours"].median()
)

maximum_resolution = (
    resolved_df["Resolution_Hours"].max()
)

minimum_resolution = (
    resolved_df["Resolution_Hours"].min()
)

print("Average resolution hours:", round(average_resolution, 2))

print("Median resolution hours:", round(median_resolution, 2))

print("Maximum resolution hours:", round(maximum_resolution, 2))

print("Minimum resolution hours:", round(minimum_resolution, 2))
print("\n--- QUESTION 6: SLA PERFORMANCE ---")

sla_count = df["SLA_Status"].value_counts()

print(sla_count)

# Chart 5: SLA Performance Distribution

sla_count.plot(
    kind="pie",
    autopct="%1.1f%%",
    title="SLA Performance Distribution"
)

plt.ylabel("")
plt.tight_layout()
plt.show()

print("\nSLA percentage:")

sla_percentage = (
    df["SLA_Status"].value_counts(normalize=True) * 100
)

print(sla_percentage.round(2))
# Export SLA Performance Report

sla_report = pd.DataFrame({
    "Total_Tickets": sla_count,
    "Percentage": sla_percentage.round(2)
})

sla_report.to_csv(
    reports_folder / "sla_performance_report.csv"
)

print("SLA Performance Report exported successfully!")
resolved_df = df[df["Status"] == "Resolved"].copy()

within_sla = (
    resolved_df["SLA_Status"] == "Within SLA"
).sum()

total_resolved = len(resolved_df)

sla_compliance_rate = (
    within_sla / total_resolved * 100
    if total_resolved > 0 else 0
)

print(
    "\nSLA Compliance Rate:",
    round(sla_compliance_rate, 2),
    "%"
)
print("\n--- QUESTION 7: PRIORITY-WISE SLA BREACH ---")

resolved_df = df[df["Status"] == "Resolved"].copy()

priority_sla = (
    resolved_df
    .groupby("Priority")
    .agg(
        Total_Resolved=("Ticket_ID", "count"),
        SLA_Breaches=(
            "SLA_Status",
            lambda x: (x == "SLA Breached").sum()
        )
    )
)

priority_sla["Breach_Rate_Percent"] = (
    priority_sla["SLA_Breaches"]
    / priority_sla["Total_Resolved"] * 100
).round(2)

print(priority_sla)
# Export Priority-wise SLA Breach Report

priority_sla.to_csv(
    reports_folder / "priority_wise_sla_breach_report.csv"
)

print("Priority-wise SLA Breach Report exported successfully!")
print("\n--- QUESTION 8: SUPPORT TEAM PERFORMANCE ---")

team_performance = (
    resolved_df
    .groupby("Assigned_Team")
    .agg(
        Total_Resolved=("Ticket_ID", "count"),
        Average_Resolution_Hours=(
            "Resolution_Hours", "mean"
        ),
        Median_Resolution_Hours=(
            "Resolution_Hours", "median"
        )
    )
)

team_performance = team_performance.round(2)

print(team_performance)
# Export Support Team Performance Report

team_performance.to_csv(
    reports_folder / "support_team_performance_report.csv"
)

print("Support Team Performance Report exported successfully!")
print("\n--- QUESTION 9: MONTHLY TICKET TRENDS ---")

df["Created_Month"] = (
    df["Created_Date"].dt.to_period("M")
)

monthly_tickets = (
    df.groupby("Created_Month")
    .size()
    .reset_index(name="Total_Tickets")
)

print(monthly_tickets)
# Export Monthly Ticket Trends
monthly_tickets.to_csv(
    reports_folder / "monthly_ticket_trends_report.csv",
    index=False
)
# Chart 6: Monthly Ticket Trends

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_tickets["Created_Month"].astype(str),
    monthly_tickets["Total_Tickets"],
    marker="o"
)

plt.title("Monthly IT Support Ticket Trends")
plt.xlabel("Month")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
print("\n--- QUESTION 10: AGENT PRODUCTIVITY ---")

agent_performance = (
    resolved_df
    .groupby("Assigned_Agent")
    .agg(
        Total_Resolved=("Ticket_ID", "count"),
        Average_Resolution_Hours=(
            "Resolution_Hours", "mean"
        )
    )
    .sort_values(
        by="Total_Resolved",
        ascending=False
    )
)

print(agent_performance.round(2))
# Export Agent Productivity
agent_performance.to_csv(
    reports_folder / "agent_productivity_report.csv"
)

print("All analysis reports exported successfully!")
# Chart 8: Agent Productivity

agent_performance["Total_Resolved"].head(10).plot(
    kind="bar",
    title="Top 10 Support Agents by Tickets Resolved"
)

plt.xlabel("Support Agent")
plt.ylabel("Total Resolved Tickets")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
