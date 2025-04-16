# ==============================
# File: client/client.py
# ==============================

import requests
import time
import joblib
import tensorflow as tf
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from preprocess import load_data

SERVER_URL = 'http://192.168.137.177:5000'  # Replace with actual aggregator IP


def build_model(input_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def get_global_weights():
    res = requests.get(f'{SERVER_URL}/global')
    with open("temp_global.pkl", "wb") as f:
        f.write(res.content)
    with open("temp_global.pkl", "rb") as f:
        return joblib.load(f)


def send_weights(weights):
    with open("temp_weights.pkl", "wb") as f:
        joblib.dump(weights, f)
    with open("temp_weights.pkl", "rb") as f:
        requests.post(f'{SERVER_URL}/upload', data=f.read())


if __name__ == '__main__':
    X_train, _, y_train, _ = load_data()
    model = build_model(X_train.shape[1])

    for round_num in range(1, 11):
        print(f"\n[Client] Round {round_num} started")

        # Get global weights
        try:
            global_weights = get_global_weights()
            model.set_weights(global_weights)
            print("[Client] Received global weights")
        except Exception as e:
            print(f"[Client] Waiting for global weights: {e}")
            time.sleep(5)
            continue

        # Local training
        model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=1)

        # Send updated weights to aggregator
        updated_weights = model.get_weights()
        send_weights(updated_weights)
        print("[Client] Sent updated weights to aggregator")

        # Optional pause
        time.sleep(5)
