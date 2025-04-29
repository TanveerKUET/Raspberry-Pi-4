import pandas as pd

# Config
input_file = 'KDDTrain+.csv'
output_prefix = 'KDDTrain_Client_'
num_clients = 2

# Load dataset
df = pd.read_csv(input_file)

# Shuffle the dataset (optional but recommended)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Calculate size per client
chunk_size = len(df) // num_clients

# Save each chunk
for i in range(num_clients):
    start = i * chunk_size
    end = (i + 1) * chunk_size if i != num_clients - 1 else len(df)
    client_df = df.iloc[start:end]
    client_df.to_csv(f'{output_prefix}{i+1}.csv', index=False)
    print(f'Client {i+1} data saved: {len(client_df)} rows')
