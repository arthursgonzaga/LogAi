# log_analyzer.py

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
import openai
from datetime import datetime

# Configurar API do OpenAI (coloque sua chave aqui se for usar)
# openai.api_key = "sua-chave-aqui"

# Caminho do log
LOG_FILE = 'data/app.log'

# --- 1. Pré-processamento dos Logs ---
def preprocess_logs():
    data = []
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)'
    
    with open(LOG_FILE, 'r') as file:
        for line in file:
            match = re.match(log_pattern, line)
            if match:
                timestamp_str, level, message = match.groups()
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                hour = timestamp.hour
                level_num = {"INFO": 0, "DEBUG": 1, "WARN": 2, "ERROR": 3}.get(level, -1)
                message_length = len(message)
                slow_query = int('Query executed in' in message and int(message.split()[-1][:-2]) > 100)
                
                data.append([timestamp, hour, level, level_num, message, message_length, slow_query])
    
    df = pd.DataFrame(data, columns=['timestamp', 'hour', 'level', 'level_num', 'message', 'message_length', 'slow_query'])
    return df

# --- 2. Detecção de Anomalias ---
def detect_anomalies(df):
    features = df[['hour', 'level_num', 'message_length', 'slow_query']]
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(features)
    df['anomaly'] = model.predict(features)
    return df

# --- 3. Classificação de Eventos ---
def classify_events(df):
    categories = []
    for message in df['message']:
        if "logged in" in message.lower():
            categories.append('login_success')
        elif "failed to connect" in message.lower() or "connection error" in message.lower():
            categories.append('connection_error')
        elif "query executed in" in message.lower():
            categories.append('slow_query')
        else:
            categories.append('other')
    df['event_category'] = categories
    return df

# --- 4. Visualizações ---
def plot_event_categories(df):
    plt.figure(figsize=(8,6))
    sns.countplot(x='event_category', data=df, order=df['event_category'].value_counts().index)
    plt.title('Quantidade de Eventos por Categoria')
    plt.xlabel('Categoria de Evento')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/event_categories.png')
    plt.show()

def plot_anomalies_per_hour(df):
    anomalies_per_hour = df[df['anomaly'] == -1]['hour'].value_counts().sort_index()
    plt.figure(figsize=(8,6))
    anomalies_per_hour.plot(kind='bar')
    plt.title('Anomalias Detectadas por Hora')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Quantidade de Anomalias')
    plt.tight_layout()
    plt.savefig('output/anomalies_per_hour.png')
    plt.show()

# --- 5. Geração de Análise Interpretativa ---
def generate_interpretation(df):
    summary = {
        "total_logs": len(df),
        "anomalies_detected": sum(df['anomaly'] == -1),
        "most_common_event": df['event_category'].mode()[0],
        "peak_anomaly_hour": df[df['anomaly'] == -1]['hour'].mode()[0] if not df[df['anomaly'] == -1].empty else "N/A"
    }
    
    prompt = f"""
    Temos {summary['total_logs']} eventos no total.
    Foram detectadas {summary['anomalies_detected']} anomalias.
    O tipo de evento mais comum foi '{summary['most_common_event']}'.
    O horário com maior concentração de anomalias foi {summary['peak_anomaly_hour']}h.
    
    Gere uma interpretação em linguagem natural sobre o sistema monitorado, destacando tendências ou potenciais problemas.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        interpretation = response['choices'][0]['message']['content']
        print("\n=== Análise Interpretativa via ChatGPT ===")
        print(interpretation)
    except Exception as e:
        print("\n=== Análise Interpretativa (Fallback) ===")
        print("Baseado nos dados:")
        print(f"- O evento mais frequente foi '{summary['most_common_event']}'.")
        print(f"- Foram detectadas {summary['anomalies_detected']} anomalias.")
        print(f"- A hora com mais anomalias foi {summary['peak_anomaly_hour']}h.")
        print("Sugere-se monitorar horários de pico e focar em melhorar as conexões.")

# --- 6. Função Principal ---
def main():
    df = preprocess_logs()
    df = detect_anomalies(df)
    df = classify_events(df)
    
    # Criar pasta de output se necessário
    import os
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Gera visualizações
    plot_event_categories(df)
    plot_anomalies_per_hour(df)
    
    # Gera interpretação dos resultados
    generate_interpretation(df)

if __name__ == "__main__":
    main()