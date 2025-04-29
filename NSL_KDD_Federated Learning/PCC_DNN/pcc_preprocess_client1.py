# ==============================
# File: common/preprocess.py
# ==============================

import pandas as pd
import joblib
import requests
from io import BytesIO
from sklearn.preprocessing import MinMaxScaler, StandardScaler

COLUMN_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
    'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login',
    'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'labels', 'None'
]

# Fetch selected features from aggregator
def fetch_selected_features(aggregator_url="http://192.168.0.110:5000/features"):  # <-- CHANGE IP
    response = requests.get(aggregator_url)
    response.raise_for_status()
    return joblib.load(BytesIO(response.content))

selected_features = fetch_selected_features()

def load_data(train_file='KDDTrain_Client_1.csv', test_file='KDDTest+.csv'):
    def preprocess(df, dataset_name="dataset"):
        columns_to_drop = ['protocol_type', 'service', 'flag', 'None']
        df = df.drop(columns=columns_to_drop)

        df['labels'] = df['labels'].apply(lambda x: 0 if x == 'normal' else 1)
        feature_cols = df.columns.difference(['labels'])
        scaler = StandardScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])

        X = df[selected_features]
        y = df['labels']
        return X, y

    train_df = pd.read_csv(train_file, names=COLUMN_NAMES, skiprows=1)
    test_df = pd.read_csv(test_file, names=COLUMN_NAMES, skiprows=1)
    X_train, y_train = preprocess(train_df, dataset_name="Train")
    X_test, y_test = preprocess(test_df, dataset_name="Test")
    return X_train, X_test, y_train, y_test

