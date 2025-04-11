import pandas as pd
import matplotlib.pyplot as plt

# Filepath to the CSV file
csv_file = "data_receive/rad_off_data_corrected.csv"

# Load the CSV file into a DataFrame
data = pd.read_csv(csv_file)

# Convert the 'timestamp' column to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Separate data by sensor_id
radiator_data = data[data['sensor_id'] == 'radiator']
room_data = data[data['sensor_id'] == 'room']

# Plot temperature over time
plt.figure(figsize=(12, 6))
plt.plot(radiator_data['timestamp'], radiator_data['temperature (sensor reading)'], label='Radiator Temperature', color='red')
plt.plot(room_data['timestamp'], room_data['temperature (sensor reading)'], label='Room Temperature', color='blue')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot humidity over time
plt.figure(figsize=(12, 6))
plt.plot(radiator_data['timestamp'], radiator_data['humidity'], label='Radiator Humidity', color='orange')
plt.plot(room_data['timestamp'], room_data['humidity'], label='Room Humidity', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Humidity (%)')
plt.title('Humidity Over Time')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()