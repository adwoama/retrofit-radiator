import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime

BROKER = "test.mosquitto.org" #broker.hivemq.com
PORT = 1883
#TOPICS = [("cmu/retrofit_radiator/sensor1", 0), 
#          ("cmu/retrofit_radiator/sensor2", 0), 
#          ("cmu/retrofit_radiator/sensor3", 0)]

TOPICS = "cmu/retrofit_radiator/+"
# Generate a new filename based on the current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
DATA_FILE = f"data_receive/data_{current_time}.json"  # Path to the JSON file


def on_message(client, userdata, message):
    """
    Callback function triggered when a message is received.
    Saves the received JSON data to a file.
    """
    try:
        # Decode the message payload
        data = json.loads(message.payload.decode())
        print(f"Received message: {data} on topic {message.topic}")

        # Check if the file exists
        if os.path.exists(DATA_FILE):
            # Load existing data from the file
            with open(DATA_FILE, "r") as file:
                existing_data = json.load(file)
        else:
            # Initialize an empty list if the file doesn't exist
            existing_data = []

        # Append the new data to the existing data
        existing_data.append(data)

        # Save the updated data back to the file
        with open(DATA_FILE, "w") as file:
            json.dump(existing_data, file, indent=4)
        print(f"Data saved to {DATA_FILE}")

    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPICS)

print(f"Subscribed to topic '{TOPICS}' on broker '{BROKER}'")
client.loop_forever()