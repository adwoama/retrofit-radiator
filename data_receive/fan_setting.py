import paho.mqtt.client as mqtt

# MQTT broker details
BROKER = "test.mosquitto.org"  # Replace with your broker address if different
PORT = 1883
TOPIC_FAN_STATE = "cmu/retrofit_radiator/fan_state"  # Topic to control the fan state

def send_fan_state(state):
    """
    Sends the fan state ('on' or 'off') to the MQTT broker.
    """
    try:
        # Initialize MQTT client
        client = mqtt.Client()
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT broker at {BROKER}")

        # Publish the fan state to the topic
        client.publish(TOPIC_FAN_STATE, state)
        print(f"Sent '{state}' to topic '{TOPIC_FAN_STATE}'")

        # Disconnect from the broker
        client.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        # Prompt the user for input
        state = input("Enter fan state ('on' or 'off', or 'exit' to quit): ").strip().lower()
        if state == "exit":
            print("Exiting...")
            break
        elif state in ["on", "off"]:
            send_fan_state(state)
        else:
            print("Invalid input. Please enter 'on', 'off', or 'exit'.")