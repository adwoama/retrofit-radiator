The code from the RPi Pico W will be remotely received on a webserver via https.

Currently, we will recieve the data on a RPi 4 running server.py.

## 1. Run Server.py

This will start your server and make it accessible locally on port 5000.

## 2. Run ngrok in the Terminal

In a separate terminal window or tab, run the following command to expose your Flask server:

```
ngrok http 5000
```

- ngrok will create a public URL (e.g., https://abcd1234.ngrok.io) that forwards requests to your local Flask server running on port 5000.
- You will see output like this:

```
Forwarding    https://abcd1234.ngrok.io -> http://localhost:5000
```

## 3. Use the ngrok HTTPS URL

Use the url for the Pico W to recieve the data.

```
server_url = "https://abcd1234.ngrok.io/receive-data"
send_data_to_server(data, server_url)
```