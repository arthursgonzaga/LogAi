import pandas as pd
import numpy as np
import re
from datetime import datetime
from sklearn.ensemble import IsolationForest
import os

LOG_FILE = './data/app.log'

LOG_LEVEL_MAPPING = {
    'INFO': 0,
    'DEBUG': 1,
    'WARN': 2,
    'ERROR': 3
}

def read_log(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split(' ', 2)
                if len(parts) < 3:
                    continue
                timestamp = f"{parts[0]} {parts[1]}"
                log_level = parts[2].split(' ', 1)[0]
                message = parts[2].split(' ', 1)[1]
                data.append({
                    'timestamp': timestamp,
                    'log_level': log_level,
                    'message': message
                })
            except (IndexError, ValueError):
                continue

    if not data:
        raise ValueError(f"O arquivo {file_path} está vazio ou não contém linhas válidas no formato esperado.")

    # Crie o DataFrame
    df = pd.DataFrame(data)

    return df

# Add new features to the DataFrame
def extract_features(df):
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp_dt'].dt.hour
    df['level_num'] = df['log_level'].map(LOG_LEVEL_MAPPING)
    df['message_length'] = df['message'].apply(len)
    
    # Feature: slow_query (simples busca por "Query executed in XXms")
    def detect_slow_query(msg):
        match = re.search(r'Query executed in (\d+)ms', msg)
        if match:
            return int(match.group(1)) > 100
        return 0

    df['slow_query'] = df['message'].apply(detect_slow_query)

    # Feature extra 1: has_error_keyword
    df['has_error_keyword'] = df['message'].str.contains('error|failed|exception', case=False, regex=True).astype(int)

    # Feature extra 2: is_database_related
    df['is_database_related'] = df['message'].str.contains('database|query|SQL', case=False, regex=True).astype(int)

    # Feature extra 3: word_count
    df['word_count'] = df['message'].apply(lambda x: len(x.split()))

    # Feature extra 4: is_warning
    df['is_warning'] = (df['log_level'] == 'WARN').astype(int)

    return df

# Model to detect anomalies
def detect_anomalies(df, features):
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = iso_forest.fit_predict(df[features])
    df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})  # 1 para anomalia
    return df

def generate_report(df):
    print("\n====== Relatório de Análise de Logs ======")
    print(f"Total de registros: {len(df)}")
    print(f"Anomalias detectadas: {df['anomaly'].sum()}")
    print("\nDistribuição dos níveis de log:")
    print(df['log_level'].value_counts())
    print("\nExemplos de anomalias:")
    print(df[df['anomaly'] == 1][['timestamp', 'log_level', 'message']].head(10))

def main():
    if not os.path.exists(LOG_FILE):
        print(f"Arquivo {LOG_FILE} não encontrado.")
        return

    df = read_log(LOG_FILE)
    df = extract_features(df)

    feature_cols = [
        'hour', 'level_num', 'message_length', 'slow_query',
        'has_error_keyword', 'is_database_related', 'word_count', 'is_warning'
    ]

    df = detect_anomalies(df, feature_cols)

    os.makedirs('./data/output/', exist_ok=True)
    df.to_csv('./data/output/processed_logs.csv', index=False)

    anomalies = df[df['anomaly'] == 1]
    anomalies.to_csv('./data/output/anomalies.csv', index=False)

    generate_report(df)

if __name__ == '__main__':
    main()
