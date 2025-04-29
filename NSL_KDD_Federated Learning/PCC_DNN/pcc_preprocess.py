# ==============================
# File: common/pcc_preprocess.py
# ==============================

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

COLUMN_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
    'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login',
    'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'labels', 'None'
]

def load_data(train_file='KDDTrain+.csv', test_file='KDDTest+.csv', return_features=False):
    def preprocess(df, selected_features=None, dataset_name="dataset"):
        columns_to_drop = ['protocol_type', 'service', 'flag', 'None']
        df = df.drop(columns=columns_to_drop)

        df['labels'] = df['labels'].apply(lambda x: 0 if x == 'normal' else 1)
        feature_cols = df.columns.difference(['labels'])

        scaler = StandardScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])

        if selected_features is None:
            # Automatically select best threshold
            correlations = df.corr(method='pearson')['labels'].drop('labels')
            correlations_sorted = correlations.abs().sort_values(ascending=False)

            thresholds = [0.009, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
            best_accuracy = 0
            best_features = []
            best_threshold = None

            for thresh in thresholds:
                features = correlations_sorted[correlations_sorted >= thresh].index.tolist()
                if not features:
                    continue

                X_temp = df[features]
                y_temp = df['labels']
                X_train_temp, X_val_temp, y_train_temp, y_val_temp = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)

                model = LogisticRegression(max_iter=500)
                model.fit(X_train_temp, y_train_temp)
                acc = model.score(X_val_temp, y_val_temp)

                print(f"[{dataset_name}] Threshold {thresh:.2f}: {len(features)} features, Accuracy = {acc:.4f}")
                if acc > best_accuracy:
                    best_accuracy = acc
                    best_features = features
                    best_threshold = thresh

            selected_features = best_features
            print(f"\n🏆 [{dataset_name}] Best threshold = {best_threshold:.2f}, Accuracy = {best_accuracy:.4f}")
            print(f"[{dataset_name}] Selected features: {selected_features}")

        X = df[selected_features]
        y = df['labels']
        return X, y, selected_features

    train_df = pd.read_csv(train_file, names=COLUMN_NAMES, skiprows=1)
    test_df = pd.read_csv(test_file, names=COLUMN_NAMES, skiprows=1)

    X_train, y_train, selected_features = preprocess(train_df, dataset_name="Train")
    X_test, y_test, _ = preprocess(test_df, selected_features=selected_features, dataset_name="Test")

    if return_features:
        return X_train, X_test, y_train, y_test, selected_features
    else:
        return X_train, X_test, y_train, y_test
