import csv
from datetime import datetime, timedelta
import pytz

# Define the timezone
eastern = pytz.timezone("US/Eastern")

# Define the schedule
schedule = [
    # Format: (start_time, end_time, occupancy)
    ("2025-04-23 08:00:00", "2025-04-23 15:00:00", 1),  # Occupied
    ("2025-04-23 15:00:00", "2025-04-23 18:00:00", 0),  # Unoccupied
    ("2025-04-23 18:00:00", "2025-04-23 20:00:00", 1),  # Occupied
    ("2025-04-23 20:00:00", "2025-04-24 08:00:00", 0),  # Unoccupied
    ("2025-04-24 08:00:00", "2025-04-24 10:00:00", 1),  # Occupied
    ("2025-04-24 10:00:00", "2025-04-24 12:00:00", 0),  # Unoccupied
    ("2025-04-24 12:00:00", "2025-04-24 14:00:00", 1),  # Occupied
    ("2025-04-24 14:00:00", "2025-04-25 00:00:00", 0),  # Unoccupied
]

# Generate the CSV file
with open("/lib/schedule.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Unix Time", "Eastern Time", "Occupancy"])

    # Process each time range in the schedule
    for start, end, occupancy in schedule:
        # Parse the start and end times
        start_dt = eastern.localize(datetime.strptime(start, "%Y-%m-%d %H:%M:%S"))
        end_dt = eastern.localize(datetime.strptime(end, "%Y-%m-%d %H:%M:%S"))

        # Generate timestamps for every minute in the range
        current_dt = start_dt
        while current_dt < end_dt:
            # Convert to Unix time
            unix_time = int(current_dt.timestamp())
            # Write the row to the CSV
            writer.writerow([unix_time, current_dt.strftime("%Y-%m-%d %H:%M:%S"), occupancy])
            # Increment by one minute
            current_dt += timedelta(minutes=1)

print("schedule.csv has been generated.")