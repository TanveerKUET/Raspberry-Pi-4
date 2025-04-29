# ==============================
# File: pcc_cnn_client1.py
# ==============================

import requests
import time
import joblib
import tensorflow as tf
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from preprocessclient1 import load_data
from pcc_preprocess_client1 import load_data
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers

SERVER_URL = 'http://192.168.0.110:5000'  # Replace with your aggregator IP

def build_model(input_shape):
    '''
    model = tf.keras.Sequential([
        tf.keras.layers.Conv1D(filters=64, kernel_size=5, activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling1D(pool_size=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(2, activation='softmax')  # 2 classes: normal vs. attack
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    '''
    model = tf.keras.Sequential([
        # 1st Conv1D layer (91 × 64)
        tf.keras.layers.Conv1D(filters=64, kernel_size=10, activation='relu', input_shape=(X_train.shape[1], 1),
                               kernel_regularizer=regularizers.l2(0.001)),

        # 2nd Conv1D layer (10 × 64)
        tf.keras.layers.Conv1D(filters=64, kernel_size=10, activation='relu',
                               kernel_regularizer=regularizers.l2(0.001)),

        # 2. MaxPooling
        tf.keras.layers.MaxPooling1D(pool_size=2),

        # 3. Flatten
        tf.keras.layers.Flatten(),

        # 4. Dense 128
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),

        # 5. Dropout
        tf.keras.layers.Dropout(0.5),

        # 6. Dense 2 (softmax layer)
        tf.keras.layers.Dense(2, activation='softmax')
    ])

    # 7. Compile
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def get_global_weights():
    res = requests.get(f'{SERVER_URL}/global')
    with open("temp_global.pkl", "wb") as f:
        f.write(res.content)
    with open("temp_global.pkl", "rb") as f:
        return joblib.load(f)

def send_weights(weights, num_samples):
    # Convert each weight to a NumPy array explicitly
    weights_np = [np.array(w) for w in weights]

    payload = {
        'weights': weights_np,
        'num_samples': num_samples
    }
    with open("temp_weights.pkl", "wb") as f:
        joblib.dump(payload, f)
    with open("temp_weights.pkl", "rb") as f:
        requests.post(f'{SERVER_URL}/upload', data=f.read())


if __name__ == '__main__':
    X_train, _, y_train, _ = load_data()

    # Convert to NumPy and reshape for Conv1D: (samples, timesteps, channels)
    X_train = X_train.to_numpy().reshape(-1, X_train.shape[1], 1)
    print("Extracted Features: ", X_train)
    y_train = to_categorical(y_train, num_classes=2)

    model = build_model((X_train.shape[1], 1))  # input_shape = (timesteps, channels)

    for round_num in range(1, 30):
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

        # Train locally
        model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=1)

        # Send updated weights
        updated_weights = model.get_weights()
        send_weights(updated_weights, len(X_train))
        print("[Client] Sent updated weights to aggregator")

        time.sleep(5)
