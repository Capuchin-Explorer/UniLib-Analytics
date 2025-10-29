import pandas as pd
import os
from glob import glob

# === Paths ===
base_path = os.getcwd()
data_path = os.path.join(base_path, "data")
raw_path = os.path.join(data_path, "raw")
legend_path = os.path.join(raw_path, "legend")

# === Step 1: Combine all measurement CSV files ===
print("🔹 Step 1: Combining all measurement CSV files...")

# Find all CSV files in the raw folder (excluding legend subfolder)
csv_files = glob(os.path.join(raw_path, "*.csv"))

if len(csv_files) == 0:
    raise FileNotFoundError("No measurement CSV files found in /data/raw/.")
else:
    print(f"Found {len(csv_files)} CSV files to merge:")
    for f in csv_files:
        print("  -", os.path.basename(f))

# Read and concatenate all CSV files
all_dfs = [pd.read_csv(f) for f in csv_files]
all_measurements = pd.concat(all_dfs, ignore_index=True)
print(f"Combined dataset: {all_measurements.shape[0]} rows, {all_measurements.shape[1]} columns")

# Save intermediate combined dataset
combined_path = os.path.join(data_path, "intermediate", "all_measurements.csv")
os.makedirs(os.path.dirname(combined_path), exist_ok=True)
all_measurements.to_csv(combined_path, index=False)
print(f"Saved combined dataset to: {combined_path}\n")

# === Step 2: Load legend files ===
print("🔹 Step 2: Loading and merging legend files...")

wifi_routers_path = os.path.join(legend_path, "wifi_routers_rows.csv")
wifi_access_path = os.path.join(legend_path, "wifi_access_locations_rows.csv")

wifi_routers = pd.read_csv(wifi_routers_path)
wifi_access = pd.read_csv(wifi_access_path)

print(f"Loaded wifi_routers_rows.csv – {len(wifi_routers)} rows")
print(f"Loaded wifi_access_locations_rows.csv – {len(wifi_access)} rows")

# Rename 'id' in wifi_access to avoid column conflicts
if "id" in wifi_access.columns:
    wifi_access.rename(columns={"id": "further_id"}, inplace=True)

# Merge legends on 'identifier'
legend_merged = pd.merge(
    wifi_routers,
    wifi_access,
    on="identifier",
    how="left",
    suffixes=("_router", "_access")
)

print(f"Legends merged: {legend_merged.shape[0]} rows, {legend_merged.shape[1]} columns")

# === Step 3: Merge min/max recorded devices ===
def merge_min_max(row, col):
    """Use access value if available and non-zero, otherwise use router value."""
    access_val = row.get(f"{col}_access")
    router_val = row.get(f"{col}_router")
    if pd.notna(access_val) and access_val != 0:
        return access_val
    else:
        return router_val

for col in ["min_recorded_devices", "max_recorded_devices"]:
    legend_merged[col] = legend_merged.apply(lambda r: merge_min_max(r, col), axis=1)

print("min/max recorded devices merged")

# === Step 4: Merge combined measurements with merged legends ===
print("\n🔹 Step 4: Joining combined measurements with legend data...")

if "router_id" not in all_measurements.columns:
    raise KeyError("'router_id' not found in measurement dataset — join aborted.")

merged_full = all_measurements.merge(legend_merged, left_on="router_id", right_on="id", how="left")

# Check that valid addresses exist after join
valid_addresses = merged_full.loc[merged_full['address'].notna() & (merged_full['address'] != 0)].shape[0]
if valid_addresses == 0:
    raise ValueError("After join: No valid addresses found in merged data.")
print(f"After join: {valid_addresses} valid addresses found.")
print(f"Final merged dataset shape: {merged_full.shape[0]} rows, {merged_full.shape[1]} columns")

# === Step 5: Save final merged dataset ===
output_path = os.path.join(data_path, "intermediate", "all_measurements_with_legend.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged_full.to_csv(output_path, index=False)
print(f"Final merged dataset saved to: {output_path}")
