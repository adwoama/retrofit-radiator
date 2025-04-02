# retrofit-radiator
>Project for class 12770: Autonomous Sustainable Buildings at Carnegie Mellon University taught by Professor Mario Berges. 

### Authors of this project:
- Adwoa Asare (Electrical & Computer Engineering M.S.)
- Barbara Castro-Schell (Civil Engineering M.S.)
- Ziyuan Ma (Civil Engineering M.S.)

## Getting Started
Install micropython firmware on your Raspberry Pi Picos.

Make a file called wifi_config.py in the /lib folder and put the following lines:

```python

# Wi-Fi credentials (DO NOT SHARE THIS FILE)

WIFI_SSID = "YourWiFiSSID"
WIFI_PASSWORD = "YourWiFiPassword"

```
If you are running this experiment on campus you will need to connect the pico to CMU-DEVICE not CMU-SECURE. Your SSID will be "CMUE-SECURE" and the password will be "" (an empty string). You will need to submit the MAC address. *I'll add instructions about this later.*

## 1. Raspberry Pi Pico Setup

1. Download Thonny IDE for easy file transfer to the pico. Transfer the entire lib folder to the pico.

2. Depending on which sensing region the pico is for (radiator, room, or outside) choose the appropriate file frome /src, rename it to main.py and transfer it to the root directory of the pico so it will run automatically on startup.

3. Give the sensor a unique topic in datastream.py in the format ```TOPIC = "cmu/retrofit_radiator/unique_topic"```

4. save everything and run main.py. If yoour pico is plugged into a laptop you should see it print out the first data point and successful connection to the mqtt broker you are using.

## 2. Data Receipt PC Setup

1. run /data_receive/subscribe.py on a PC you are comfortable leaving runnig for a long time

2. The line ```TOPICS = "cmu/retrofit_radiator/+"``` allows you to see all topics that are part of *cmu/retrofit_radiator/+* If you want to subscribe only to specific topics you can comment out this line and uncomment the line right above. In this case format the topics you want in a list: 
    ```python
    TOPICS = [("cmu/retrofit_radiator/sensor1", 0),
        ("cmu/retrofit_radiator/sensor2", 0), 
        ("cmu/retrofit_radiator/sensor3", 0)] 
    ```
3. data will be saved to data_receive/data_[CURRENT DATE/TIME].json 
4. TODO: json to csv functionality for data analysis