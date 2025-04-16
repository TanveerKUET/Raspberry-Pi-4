# ==============================
# File: common/preprocess.py
# ==============================

import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

COLUMN_NAMES = [
    'duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent',
    'hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root',
    'num_file_creations','num_shells','num_access_files','num_outbound_cmds','is_host_login','is_guest_login',
    'count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate',
    'diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count','dst_host_same_srv_rate',
    'dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate',
    'dst_host_srv_serror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate','labels','None'
]

def load_data(train_file='KDDTrain+.csv', test_file='KDDTest+.csv'):
    def preprocess(df):
        categorical_cols = ['protocol_type', 'service', 'flag','None']
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
        df['labels'] = df['labels'].apply(lambda x: 0 if x == 'normal' else 1)
        feature_cols = df.columns.difference(['labels'])
        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])
        X = df.drop('labels', axis=1)
        y = df['labels']
        return X, y

    train_df = pd.read_csv(train_file, names=COLUMN_NAMES, skiprows=1)
    test_df = pd.read_csv(test_file, names=COLUMN_NAMES, skiprows=1)
    X_train, y_train = preprocess(train_df)
    X_test, y_test = preprocess(test_df)
    return X_train, X_test, y_train, y_test
