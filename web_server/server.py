from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive-data', methods=['POST'])
def receive_data():
    """
    Endpoint to receive data from the Raspberry Pi Pico W.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Respond to the sender
        return jsonify({"status": "success", "message": "Data received"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(host='0.0.0.0', port=5000)