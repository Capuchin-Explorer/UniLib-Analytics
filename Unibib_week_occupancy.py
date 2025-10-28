import pandas as pd
import os
import matplotlib.pyplot as plt

# === Pfad zur CSV-Datei ===
data_path = os.path.join(os.getcwd(), "Daten")
csv_file = os.path.join(data_path, "alle_messungen_mit_legende.csv")

# === CSV einlesen ===
df = pd.read_csv(csv_file)
df['recorded_at'] = pd.to_datetime(df['recorded_at'])

# === Filter für Router IDs 1435 bis 1459 ===
df_building = df[(df['router_id'] >= 1435) & (df['router_id'] <= 1459)].copy()

# === Summe aller device_count für jede gleiche Zeit ===
summed_counts = df_building.groupby('recorded_at')['device_count'].sum().reset_index()
summed_counts.rename(columns={'device_count': 'total_device_count'}, inplace=True)

# === Datum extrahieren ===
summed_counts['date'] = summed_counts['recorded_at'].dt.date

# === Höchstwert pro Tag berechnen ===
daily_max = summed_counts.groupby('date')['total_device_count'].max().reset_index()
daily_max.rename(columns={'total_device_count': 'daily_max_device_count'}, inplace=True)

# === Wochentag ermitteln ===
daily_max['weekday'] = pd.to_datetime(daily_max['date']).dt.day_name()

# === Median der täglichen Höchstwerte pro Wochentag berechnen ===
weekday_median = daily_max.groupby('weekday')['daily_max_device_count'].median().reindex([
    'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
]).reset_index()

# === Plot erstellen ===
plt.figure(figsize=(10, 6))
plt.bar(weekday_median['weekday'], weekday_median['daily_max_device_count'], color='skyblue')
plt.xlabel('Weekday')
plt.ylabel('Median of Daily High Scores')
plt.title('Median of Daily High Scores per Weekday for Unibib')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# === Optional: Ausgabe des DataFrames ===
print("\nDaily Max Device Count with Weekday for Building Routers 1435-1459:")
print(daily_max)
