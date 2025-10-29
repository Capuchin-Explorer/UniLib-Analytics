import pandas as pd
import os

# === Paths ===
data_path = os.path.join(os.getcwd(), "data")
input_path = os.path.join(data_path, "intermediate", "all_measurements_with_legend.csv")
output_path = os.path.join(data_path, "processed", "UniLib_cleaned.csv")

# === Load merged dataset ===
df = pd.read_csv(input_path)
print(f"Loaded merged dataset: {df.shape[0]} rows, {df.shape[1]} columns")

# === Drop redundant ID column ===
if 'id_y' in df.columns:
    df.drop(columns=['id_y'], inplace=True)

# === Rename columns for clarity ===
df.rename(columns={
    'id_x': 'query_id',
    'router_id': 'router_id',
    'identifier': 'router_name',
    'quelle': 'source',
    'recorded_at': 'timestamp'
}, inplace=True)

# === Reorder columns for readability ===
df = df[[
    'query_id', 'router_id', 'device_count', 'timestamp',
    'router_name', 'address', 'max_recorded_devices', 'min_recorded_devices',
    'wifi_access_location_id', 'further_id', 'latitude', 'longitude',
    'spot_id', 'internal_notes', 'source'
]]

print(f"Dataset cleaned. Shape: {df.shape}")
print("Columns:", df.columns.tolist())

# === Save cleaned dataset ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"Cleaned dataset saved to: {output_path}")
