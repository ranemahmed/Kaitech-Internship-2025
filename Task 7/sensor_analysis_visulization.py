import pandas as pd
import matplotlib.pyplot as plt

sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]

df = pd.DataFrame(sensor_data, columns=["SensorID", "Timestamp", "Temperature", "Stress", "Displacement"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

avg_data = df.groupby("SensorID")[["Temperature", "Stress", "Displacement"]].mean()
highest_temp_sensor = avg_data["Temperature"].idxmax()

print("Average values per sensor:\n", avg_data)
print("\nSensor with highest average temperature:", highest_temp_sensor)

plt.figure(1)
for sensor in df["SensorID"].unique():
    subset = df[df["SensorID"] == sensor]
    plt.plot(subset["Timestamp"], subset["Temperature"], marker='o', label=sensor)

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Over Time for Each Sensor")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.figure(2)
plt.scatter(df["Stress"], df["Displacement"], c='red', marker='x')
plt.xlabel("Stress")
plt.ylabel("Displacement")
plt.title("Stress vs. Displacement")
plt.grid(True)
plt.tight_layout()

plt.show()

