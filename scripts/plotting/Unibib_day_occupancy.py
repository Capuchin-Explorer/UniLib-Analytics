import pandas as pd
import os
import matplotlib.pyplot as plt

# === Pfad zur CSV-Datei ===
data_path = os.path.join(os.getcwd(), "Daten")
csv_file = os.path.join(data_path, "alle_messungen_mit_legende.csv")

# === CSV einlesen ===
df = pd.read_csv(csv_file)
df['recorded_at'] = pd.to_datetime(df['recorded_at'])

# === Filter für Router 1435 bis 1459 ===
df_building = df[(df['router_id'] >= 1435) & (df['router_id'] <= 1459)].copy()

# === Summe aller device_count für jede gleiche Zeit ===
summed_counts = df_building.groupby('recorded_at')['device_count'].sum().reset_index()
summed_counts.rename(columns={'device_count': 'total_device_count'}, inplace=True)

# === Datum, Wochentag und Stunde extrahieren ===
summed_counts['weekday'] = summed_counts['recorded_at'].dt.day_name()
summed_counts['hour'] = summed_counts['recorded_at'].dt.hour

# === Filter für Montag ===
monday_counts = summed_counts[summed_counts['weekday'] == 'Monday']

# === Durchschnittlicher device_count pro Stunde berechnen ===
hourly_avg = monday_counts.groupby('hour')['total_device_count'].mean().reset_index()

# === Plot erstellen ===
plt.figure(figsize=(10, 6))
plt.plot(hourly_avg['hour'], hourly_avg['total_device_count'], marker='o', linestyle='-')
plt.xticks(range(0, 24))
plt.xlabel('Hour of Day')
plt.ylabel('Average Total Device Count')
plt.title('Average Total Device Count per Hour on Mondays for Unibib')
plt.grid(True)
plt.tight_layout()
plt.show()

# === Optional: Ausgabe der Werte ===
print("\nAverage Total Device Count per Hour on Mondays for Building Routers 1435-1459:")
print(hourly_avg)
