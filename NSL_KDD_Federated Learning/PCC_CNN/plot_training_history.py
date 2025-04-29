# ==============================
# File: plot_training_history.py
# ==============================

import pandas as pd
import matplotlib.pyplot as plt

# Load the training history CSV
df = pd.read_csv("aggregator/logs/training_history.csv")

# Plot Loss and Accuracy
plt.figure(figsize=(10, 5))

# Loss plot
plt.subplot(1, 2, 1)
plt.plot(df['Round'], df['Loss'], marker='o')
plt.title("Global Loss per Round")
plt.xlabel("Round")
plt.ylabel("Loss")
plt.grid(True)

# Accuracy plot
plt.subplot(1, 2, 2)
plt.plot(df['Round'], df['Accuracy'], marker='o', color='green')
plt.title("Global Accuracy per Round")
plt.xlabel("Round")
plt.ylabel("Accuracy")
plt.grid(True)

plt.tight_layout()
plt.savefig("aggregator/logs/training_progress.png")
plt.show()
