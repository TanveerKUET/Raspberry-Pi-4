# ==============================
# File: high_dense_aggregator.py
# ==============================

import os
import csv
import joblib
import numpy as np
import tensorflow as tf
from flask import Flask, request, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from pcc_preprocess import load_data
from io import BytesIO
from tensorflow.keras.utils import to_categorical

app = Flask(__name__)
weights_buffer = []
ROUND = 0

# Load and preprocess data
X_train, X_test, y_train, y_test, selected_features = load_data(return_features=True)

# Save selected feature list
os.makedirs('aggregator', exist_ok=True)
joblib.dump(selected_features, 'aggregator/selected_features.pkl')

# Standardize feature data
X_train = X_train.to_numpy().reshape(-1, X_train.shape[1], 1)
X_test = X_test.to_numpy().reshape(-1, X_test.shape[1], 1)
y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

# Define deeper CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(filters=128, kernel_size=5, activation='relu', input_shape=(X_train.shape[1], 1)),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(filters=128, kernel_size=3, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(2, activation='softmax')
])
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
              loss='categorical_crossentropy', metrics=['accuracy'])

def weighted_aggregate(weight_data):
    total_samples = sum(n for _, n in weight_data)
    num_layers = len(weight_data[0][0])
    avg_weights = []

    for layer_idx in range(num_layers):
        layer_weights = [np.array(weights[layer_idx]) * (n / total_samples) for weights, n in weight_data]
        weighted_sum = np.sum(layer_weights, axis=0)
        avg_weights.append(weighted_sum)

    return avg_weights

@app.route('/upload', methods=['POST'])
def upload_weights():
    global weights_buffer, ROUND
    data = joblib.load(BytesIO(request.data))
    weights = data['weights']
    num_samples = data['num_samples']
    weights_buffer.append((weights, num_samples))
    print(f"[Aggregator] Received weights from client with {num_samples} samples (total: {len(weights_buffer)})")

    if len(weights_buffer) >= 2:
        print("[Aggregator] Aggregating weights using Weighted FedAvg")
        aggregated_weights = weighted_aggregate(weights_buffer)
        model.set_weights(aggregated_weights)

        # Evaluate
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        y_pred = np.argmax(model.predict(X_test), axis=1)
        y_true = np.argmax(y_test, axis=1)
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        os.makedirs("aggregator/logs", exist_ok=True)
        plt.savefig(f"aggregator/logs/confusion_round_{ROUND}.png")
        plt.close()

        # Save results
        with open(f"aggregator/logs/metrics_round_{ROUND}.txt", "w") as f:
            f.write(f"Round {ROUND}: Loss={loss:.4f}, Accuracy={accuracy:.4f}\n")
            f.write(f"Client sample counts: {[n for _, n in weights_buffer]}\n")

        os.makedirs("aggregator/weights", exist_ok=True)
        joblib.dump(model.get_weights(), f"aggregator/weights/global_weights_round_{ROUND}.pkl")

        history_path = "aggregator/logs/training_history.csv"
        file_exists = os.path.exists(history_path)
        with open(history_path, mode='a', newline='') as history_file:
            writer = csv.writer(history_file)
            if not file_exists:
                writer.writerow(['Round', 'Loss', 'Accuracy', 'SampleCounts'])
            writer.writerow([ROUND, loss, accuracy, [n for _, n in weights_buffer]])

        weights_buffer = []
        ROUND += 1
        print(f"[Aggregator] Finished Round {ROUND - 1} - Accuracy: {accuracy:.4f}")

    return "OK"

@app.route('/global', methods=['GET'])
def send_global():
    joblib.dump(model.get_weights(), 'global_weights.pkl')
    return send_file('global_weights.pkl', as_attachment=True)

@app.route('/features', methods=['GET'])
def send_selected_features():
    return send_file('aggregator/selected_features.pkl', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
