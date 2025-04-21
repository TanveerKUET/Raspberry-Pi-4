# ==============================
# File: aggregator/aggregator.py
# ==============================

import os
import joblib
import numpy as np
import tensorflow as tf
from flask import Flask, request, send_file
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from preprocess import load_data
from io import BytesIO

app = Flask(__name__)

weights_buffer = []
ROUND = 0

X_train, X_test, y_train, y_test = load_data()
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

def aggregate(weights_list):
    avg_weights = list()
    for weights in zip(*weights_list):
        avg_weights.append(np.mean(weights, axis=0))
    return avg_weights

@app.route('/upload', methods=['POST'])
def upload_weights():
    global weights_buffer
    weights = joblib.load(BytesIO(request.data))  # FIXED HERE
    weights_buffer.append(weights)
    print(f"[Aggregator] Received weights: {len(weights_buffer)}")

    # Proceed to aggregate after receiving from all clients (example: 3 clients)
    if len(weights_buffer) >= 3:
        global ROUND
        aggregated_weights = aggregate(weights_buffer)
        model.set_weights(aggregated_weights)

        # Evaluate
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        y_pred = (model.predict(X_test) > 0.5).astype(int)
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        os.makedirs("aggregator/logs", exist_ok=True)
        plt.savefig(f"aggregator/logs/confusion_round_{ROUND}.png")
        plt.close()

        with open(f"aggregator/logs/metrics_round_{ROUND}.txt", "w") as f:
            f.write(f"Round {ROUND}: Loss={loss:.4f}, Accuracy={accuracy:.4f}\n")

        weights_buffer = []
        ROUND += 1
    return "OK"

@app.route('/global', methods=['GET'])
def send_global():
    joblib.dump(model.get_weights(), 'global_weights.pkl')
    return send_file('global_weights.pkl', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
