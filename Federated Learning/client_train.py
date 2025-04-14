import tensorflow as tf
import numpy as np
import requests
import json

# Dummy data
X = np.random.rand(100, 5)
y = np.random.randint(0, 2, 100)

# Simple model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')

# Train locally
model.fit(X, y, epochs=3)

# Serialize weights
weights = [w.tolist() for w in model.get_weights()]

# Send to central server
res = requests.post("http://192.168.137.177:5000/upload_weights", json={'weights': weights})
print("Server response:", res.text)
