import pandas as pd

import sqlite3

conn = sqlite3.connect('data/metrics.db')
df = pd.read_sql_query("SELECT * FROM metrics", conn)

"SELECT * FROM metrics"

print(f"LOADED: {df.shape[0]} rows from metrics table")


sort_values = df.sort_values(by='timestamp', ascending=False)
print(f"Most recent metrics: {sort_values.shape[0]}")
print(sort_values.head())

reset_index = sort_values.reset_index(drop=True)
print(f"Reset index metrics: {reset_index.shape[0]}")
print(reset_index.head())

df['timestamp'] = pd.to_datetime(df['timestamp'])
print(f"Converted timestamp column to datetime: {df['timestamp'].dtype}")

df["cpu_roll_avg"] = df["cpu_percent"].rolling(window=12).mean()
print(f"Calculated rolling average for CPU percentage: {df['cpu_roll_avg'].shape[0]}")

df["ram_roll_avg"] = df["ram_percent"].rolling(window=12).mean()
print(f"Calculated rolling average for RAM percentage: {df['ram_roll_avg'].shape[0]}")

df["cpu_delta"] = df["cpu_percent"].diff()
print(f"Calculated CPU percentage delta: {df['cpu_delta'].shape[0]}")
df["cpu_delta"] = df["cpu_delta"].fillna(0)

df["hour_of_day"] = df["timestamp"].dt.hour
print(f"Extracted hour of day from timestamp: {df['hour_of_day'].shape[0]}")

df["is_weekend"] = (df["timestamp"].dt.dayofweek >= 5).astype(int)
print(f"Calculated is_weekend from timestamp: {df['is_weekend'].shape[0]}")

df.dropna(inplace=True)
print(f"rows after feature engineering: {df.shape[0]}")

df.to_sql('features', conn, if_exists='replace', index=False)
print(f"Features saved to database: {df.shape[0]} rows")

conn.close()
print("Feature engineering complete.Table 'features' created. ")
