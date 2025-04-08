The code from the RPi Pico W will be remotely received via an MQTT broker.

You can subscribe to the MQTT broker using subscribe.py. We are using the public Mosquitto Broker in the final version, but any broker should work. Mosquitto can also be run locally, but we used the public broker for simplicity.

Data will be saved to data_receieve/data[CURRENT DATE/TIME].json. This will give you data in the following formats depending on if you use DHT or BME sensors (since BME has an extra data field):

TODO

If you want the data in csv format you can run jsontoCSV.py to convert. This will give you data in the following format:

TODO
