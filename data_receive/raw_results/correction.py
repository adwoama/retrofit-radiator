import json

# File paths
input_file = "data_receive/rad_off_data.json"  # Replace with your file path
output_file = "data_receive/rad_off_data_corrected.json"

# Time offset in seconds
TIME_OFFSET = 134162640

# Load the JSON data
with open(input_file, "r") as file:
    data = json.load(file)

# Correct the timestamps for sensor_id: room
for entry in data:
    if entry.get("sensor_id") == "room":
        entry["timestamp"] += TIME_OFFSET

# Save the corrected data to a new file
with open(output_file, "w") as file:
    json.dump(data, file, indent=4)

print(f"Timestamps corrected and saved to {output_file}")