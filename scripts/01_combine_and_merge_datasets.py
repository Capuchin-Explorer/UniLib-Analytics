import os
import glob
import pandas as pd

# === Define paths dynamically ===
# Base directory: one level up from this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data folders relative to base directory
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
LEGEND_PATH = os.path.join(BASE_DIR, "data", "raw", "legend")
INTERMEDIATE_PATH = os.path.join(BASE_DIR, "data", "intermediate")

# === Step 1: Combine all measurement CSV files ===
print(f"Step 1: Combining all measurement CSV files from {RAW_DATA_DIR}...")

if not os.path.exists(RAW_DATA_DIR):
    raise FileNotFoundError(f"Raw data folder not found: {RAW_DATA_DIR}")

csv_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No measurement CSV files found in {RAW_DATA_DIR}")

# Combine all CSV files and add a 'Quelle' column indicating the source file
df_list = []
for f in csv_files:
    df = pd.read_csv(f)
    df['quelle'] = os.path.basename(f)  # Add column with the CSV file name
    df_list.append(df)

all_measurements = pd.concat(df_list, ignore_index=True)

print(f"Combined {len(csv_files)} CSV files with {len(all_measurements)} total rows.")

# Save the combined dataset as gzip
os.makedirs(INTERMEDIATE_PATH, exist_ok=True)
combined_path = os.path.join(INTERMEDIATE_PATH, "all_measurements.csv.gz")
all_measurements.to_csv(combined_path, index=False, compression='gzip')
print(f"Saved combined dataset to {combined_path}\n")

# === Step 2: Load and match legend files ===
print("Step 2: Loading and matching legend files (with partial identifier match)...")

wifi_routers_path = os.path.join(LEGEND_PATH, "wifi_routers_rows.csv")
wifi_access_path = os.path.join(LEGEND_PATH, "wifi_access_locations_rows.csv")

wifi_routers = pd.read_csv(wifi_routers_path)
wifi_access = pd.read_csv(wifi_access_path)

print(f"Loaded wifi_routers_rows.csv – {len(wifi_routers)} rows")
print(f"Loaded wifi_access_locations_rows.csv – {len(wifi_access)} rows")

# Rename 'id' in wifi_access to avoid conflicts
if "id" in wifi_access.columns:
    wifi_access.rename(columns={"id": "further_id"}, inplace=True)

# === Build partial match mapping ===
access_identifiers = wifi_access["identifier"].astype(str).tolist()

def find_access_identifier(router_identifier: str):
    """Return the index of the matching access entry if its identifier is contained in the router identifier."""
    if pd.isna(router_identifier):
        return None
    for idx, acc_id in enumerate(access_identifiers):
        if acc_id in router_identifier:  # partial match
            return idx
    return None

wifi_routers["access_idx"] = wifi_routers["identifier"].astype(str).apply(find_access_identifier)

# Copy all other access columns into routers if a match exists
cols_to_copy = [c for c in wifi_access.columns if c != "identifier"]
for col in cols_to_copy:
    wifi_routers[col] = wifi_routers["access_idx"].apply(
        lambda i: wifi_access.at[i, col] if i is not None else pd.NA
    )

# Clean up
wifi_routers.drop(columns=["access_idx"], inplace=True)
print(f"Partial merge completed – {wifi_routers.shape[0]} rows, {wifi_routers.shape[1]} columns")

# Save merged legend as gzip
legend_merged_path = os.path.join(INTERMEDIATE_PATH, "legend_merged.csv.gz")
wifi_routers.to_csv(legend_merged_path, index=False, compression='gzip')
print(f"Saved merged legend to: {legend_merged_path}\n")

# === Step 3: Merge measurements with merged legend ===
print("Step 3: Joining combined measurements with merged legend...")

if "router_id" not in all_measurements.columns:
    raise KeyError("'router_id' column not found in measurement dataset — join aborted.")

# Convert join keys to string
all_measurements["router_id"] = all_measurements["router_id"].astype(str)
wifi_routers["id"] = wifi_routers["id"].astype(str)

merged_full = all_measurements.merge(wifi_routers, left_on="router_id", right_on="id", how="left")

# Check for valid addresses
if "address" in merged_full.columns:
    valid_addresses = merged_full.loc[
        merged_full["address"].notna() & (merged_full["address"] != 0)
    ].shape[0]
    if valid_addresses == 0:
        print("Warning: No valid addresses found after join (check identifiers).")
    else:
        print(f"{valid_addresses} valid addresses found after join.")
else:
    print("Column 'address' not found in merged legend.")

print(f"Final merged dataset shape: {merged_full.shape[0]} rows, {merged_full.shape[1]} columns")

# === Step 4: Save final merged dataset ===
final_output_path = os.path.join(INTERMEDIATE_PATH, "all_measurements_with_legend.csv.gz")
merged_full.to_csv(final_output_path, index=False, compression='gzip')
print(f"\nFinal merged dataset saved to: {final_output_path}")
print("\nAll steps completed successfully.")
