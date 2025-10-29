import pandas as pd

df = pd.read_csv("dataset_unilib.csv.gz", compression='gzip')
#df = pd.read_csv("dataset_unilib.csv")

# Some basic methods to get used to pandas

# show the first ten rows
print(df.head(10))

# show specific columns
print(df[["router_id", "device_count"]])

# filtering rows
print (df[df["device_count"] > 0])

# deleting columns and save the data frame
df.drop(columns=["internal_notes"], inplace=True)
print(df.head)
#df.to_csv("data_cleaned.csv", index=False)

# adding a column after the last column
df["day_of_week"] = pd.to_datetime(df["recorded_at"]).dt.day_name()
print(df.head())

# rename column
#df.rename(columns={"router_id": "id_router"}, inplace=True)
#print(df.head())

# change the displayed columns and their order
df = df[["router_id", "device_count", "recorded_at"]]
print(df.head())

# are there missing rows?
missing_rows = df[df.isna().any(axis=1)]

if not missing_rows.empty:
    for idx in missing_rows.index:
        print(f"⚠️ row {idx} has missing values.")
else:
    print("✅ No missing values found.")

# group and filter
# Find the entry with the highest device_count at a specific time
# .idxmax() returns the index label of the row with the highest value.
idx_max = df.groupby('router_id')['device_count'].idxmax()
df_router_max = df.loc[idx_max, ['router_id', 'device_count', 'recorded_at']]\
                  .sort_values('device_count', ascending=False)

print(df_router_max.head())
# 17.10.24, a thursday, seems to have been the most crowed day

# analyse
# size of the data frame
print(df.shape)

# test data types
print(df.dtypes)

# some basic statistic
print(df.describe())

# display column names
print(df.columns.tolist())


# test if there are duplicat rows
has_duplicates = df.duplicated().any()
print("Are there duplicates", has_duplicates)

# Delete duplicates
#df.drop_duplicates(inplace=True)








