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

4. Save everything and run main.py. If yoour pico is plugged into a laptop you should see it print out the first data point and successful connection to the mqtt broker you are using.

## 2. Data Receipt PC Setup

1. Run /data_receive/subscribe.py on a PC you are comfortable leaving runnig for a long time

2. The line ```TOPICS = "cmu/retrofit_radiator/+"``` allows you to see all topics that are part of *cmu/retrofit_radiator/+* If you want to subscribe only to specific topics you can comment out this line and uncomment the line right above. In this case format the topics you want in a list: 
    ```python
    TOPICS = [("cmu/retrofit_radiator/sensor1", 0),
        ("cmu/retrofit_radiator/sensor2", 0), 
        ("cmu/retrofit_radiator/sensor3", 0)] 
    ```
3. Data will be saved to data_receive/data_[CURRENT DATE/TIME].json
   
4. Convert the data from json to csv using data_receive/jsonToCSV.py. You can put an API key for OpenWeather API to get the outside weather data, otherwise that collumn will be blank. We ended up updating the we Crowdsourced data from [PurpleAir](https://api.purpleair.com/#api-sensors-get-sensor-history) to fill in our outdoor data.

5. If you want to remotely turn the fan on and off you can use data_receive/fan_setting.py. When you run it, it will prompt you to enter which fan mode you want on the command line.

## 3. Retrofit Set-up

1. Cut  and tape rigid foam boardinsulation to fit around your radiator.

2. Cut a hole for your small DC fan in one of the walls of the foam insulation and insert the fan in there. Make sure you secure the pico outside of the box so it doesn't overheat, but keep the dht sensor inside the box.

3. Secure the other picos and their sensors to the wall or set them on the table. The main.py file on each pico will start collecting and transmitting data immediately after being turned on, then once every ten minutes.
   
## 4. Data Analysis
Our data analysis is available in /analysis/modeling1.ipynb

