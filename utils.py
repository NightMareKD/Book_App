import csv
from database import get_weekly_stats

def export_stats_to_csv():
    data = get_weekly_stats()
    with open("exports/stats.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Book ID", "Page", "Timestamp"])
        writer.writerows(data)
