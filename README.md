Our exciting Data Literacy project 🥳 \
You find the processed dataset in "\data\processed\dataset_unilib.csv.gz". \
All python scripts including the data processing scripts can be found under \scripts. \
I would also recommend to take a look at "scripts\df_basics.py" to refresh your data frame handling knowledge. 

That's the project structure:
```text
UniLib-Analytics/
│
├── data/
│ ├── raw/
│ │ ├── oldest_router_logs_rows (1).csv
│ │ ├── oldest_router_logs_rows (2).csv
│ │ ├── oldest_router_logs_rows (3).csv
│ │ ├── oldest_router_logs_rows (4).csv
│ │ ├── oldest_router_logs_rows.csv
│ │ ├── oldest_router_logs_rows_04_10_24_until_08_10_24.csv
│ │ ├── oldest_router_logs_rows_08_10_24_until_12_10_24.csv
│ │ └── oldest_router_logs_rows_09_23_24_until_04_10_24.csv
│ │
│ │ └── legend/
│ │ ├── wifi_routers_rows.csv
│ │ └── wifi_access_locations_rows.csv
│ │
│ ├── intermediate/
│ │ ├── all_measurements.csv.gz
│ │ ├── legend_merged.csv.gz
│ │ └── all_measurements_with_legend.csv.gz
│ │
│ └── processed/
│ └── dataset_unilib.csv.gz
│
├── scripts/
│ ├── 01_combine_and_merge_datasets.py
│ ├── 02_clean_final_dataset.py
│ ├── df_basics.py
│ │
│ └── plotting/
│ │ ├── Unibib_day_occupancy.py
│ │ └── Unibib_week_occupancy.py
│
├── .gitignore
│
└── README.md
```
