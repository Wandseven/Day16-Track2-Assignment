import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
import time
import json
import os

def run_benchmark():
    print("--- LightGBM Benchmark on r5.2xlarge ---")
    
    # 1. Load Data
    start_time = time.time()
    if not os.path.exists('creditcard.csv'):
        print("Error: creditcard.csv not found. Please download it using kaggle API first.")
        return
    
    df = pd.read_csv('creditcard.csv')
    load_time = time.time() - start_time
    print(f"Data load time: {load_time:.4f}s")

    # 2. Preprocess
    X = df.drop('Class', axis=1)
    y = df['Class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Training
    print("Starting training...")
    train_data = lgb.Dataset(X_train, label=y_train)
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'learning_rate': 0.1,
        'num_leaves': 31,
        'verbose': -1,
        'n_jobs': 8 # Utilizing 8 vCPUs of r5.2xlarge
    }

    start_train = time.time()
    gbm = lgb.train(params, train_data, num_boost_round=100)
    train_time = time.time() - start_train
    print(f"Training time: {train_time:.4f}s")

    # 4. Inference Latency (1 row)
    start_inf = time.time()
    _ = gbm.predict(X_test.iloc[[0]])
    inf_latency = (time.time() - start_inf) * 1000 # ms
    print(f"Inference latency (1 row): {inf_latency:.4f} ms")

    # 5. Inference Throughput (full test set)
    start_tp = time.time()
    y_pred_prob = gbm.predict(X_test)
    inf_throughput_time = time.time() - start_tp
    rows_per_sec = len(X_test) / inf_throughput_time
    print(f"Inference throughput: {rows_per_sec:.2f} rows/s")

    # 6. Evaluation Metrics
    y_pred = (y_pred_prob > 0.5).astype(int)
    results = {
        "load_time_sec": round(load_time, 4),
        "training_time_sec": round(train_time, 4),
        "auc_roc": round(roc_auc_score(y_test, y_pred_prob), 4),
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "inference_latency_ms": round(inf_latency, 4),
        "inference_throughput_rows_per_sec": round(rows_per_sec, 2)
    }

    print("\nBenchmark Results:")
    print(json.dumps(results, indent=4))

    # Save to file
    with open('benchmark_result.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("\nResults saved to benchmark_result.json")

if __name__ == "__main__":
    run_benchmark()
