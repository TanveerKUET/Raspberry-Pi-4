# server.py
from flask import Flask, request
import numpy as np

app = Flask(__name__)
client_weights = []

@app.route("/upload_weights", methods=["POST"])
def upload_weights():
    data = request.get_json()
    weights = data["weights"]
    client_weights.append(weights)
    print(f"Received weights from client. Total clients: {len(client_weights)}")
    return "Weights received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)